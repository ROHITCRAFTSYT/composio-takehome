"""Verification loops that need no LLM.

L1 lint      - rubric consistency rules (e.g. verdict "ready" on a gated app).
L2 evidence  - re-fetch every cited URL and confirm the quote is really on the page
               (plain HTTP first, headless browser if the quote is missing), and flag
               evidence that comes from a non-vendor domain.

    python -m agent.checks --stage pass1
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

from .fetch import fetch
from .runner import ROOT
from .schema import GRADED_FIELDS, SELF_SERVE, AppRecord

log = logging.getLogger("checks")
APPS = {a["n"]: a for a in json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))}
NEAR_MATCH = 0.85
FETCH_WORKERS = 8
# Hosts that are neutral code/package hosts: count as primary only for the vendor's own org/repo.
SHARED_HOSTS = {"github.com", "raw.githubusercontent.com", "npmjs.com", "www.npmjs.com", "pypi.org"}


def lint(rec: AppRecord) -> list[str]:
    issues: list[str] = []
    gated = rec.access not in SELF_SERVE
    if rec.verdict == "ready" and gated:
        issues.append(f"verdict 'ready' but access is '{rec.access}'")
    if rec.verdict == "ready" and rec.api_style == "none":
        issues.append("verdict 'ready' but no public API")
    if rec.verdict == "blocked" and rec.main_blocker == "none":
        issues.append("verdict 'blocked' with main_blocker 'none'")
    if rec.verdict != "blocked" and rec.main_blocker in {"paid_plan", "contact_sales", "no_public_api"}:
        issues.append(f"main_blocker '{rec.main_blocker}' but verdict '{rec.verdict}'")
    if rec.access == "approval_required" and rec.verdict == "ready":
        issues.append("approval_required should be 'ready_with_review' (or blocked)")
    if rec.mcp == "official" and not rec.mcp_url:
        issues.append("mcp 'official' without mcp_url")
    if not rec.auth_methods and rec.api_style != "none":
        issues.append("no auth method for an app with an API")
    cited = {e.field for e in rec.evidence}
    issues += [f"no evidence for '{f}'" for f in GRADED_FIELDS if f not in cited]
    if rec.confidence == "low":
        issues.append("agent reported low confidence")
    return issues


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[`*_#>|]", " ", text)  # markdown noise differs between renderers
    return re.sub(r"\s+", " ", text).strip()


def quote_score(quote: str, page_text: str) -> float:
    """1.0 if the quote is on the page verbatim (after normalising), else best partial overlap."""
    q, t = _norm(quote), _norm(page_text)
    if not q:
        return 0.0
    if q in t:
        return 1.0
    anchor = q[: min(40, len(q))]
    starts = [m.start() for m in re.finditer(re.escape(anchor[:12]), t)] or [0]
    best = 0.0
    for s in starts[:50]:
        window = t[max(0, s - 20): s + len(q) + 40]
        match = SequenceMatcher(None, q, window, autojunk=False).find_longest_match(0, len(q), 0, len(window))
        best = max(best, match.size / len(q))
    return best


def _vendor_roots(rec: AppRecord) -> set[str]:
    hint = APPS[rec.n]["hint"].split()[0]
    roots = {_root(hint), _root(rec.docs_url)} if rec.docs_url else {_root(hint)}
    return {r for r in roots if r and r not in SHARED_HOSTS}


def _root(url_or_host: str) -> str:
    host = urlparse(url_or_host if "//" in url_or_host else "//" + url_or_host).netloc.lower()
    host = host.removeprefix("www.")
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def _is_primary(url: str, rec: AppRecord, roots: set[str]) -> bool:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    if _root(url) in roots:
        return True
    if host in SHARED_HOSTS:  # github.com/<vendor-org>/... counts when the org name matches the app
        org = urlparse(url).path.strip("/").split("/")[0].lower()
        app_key = re.sub(r"[^a-z0-9]", "", rec.app.lower())[:6]
        return bool(org) and (app_key in org or org in app_key)
    return False


def check_evidence(rec: AppRecord) -> dict:
    roots = _vendor_roots(rec)
    items = []
    for ev in rec.evidence:
        page = fetch(ev.url)
        score = quote_score(ev.quote, page.text) if page.text else 0.0
        via = page.via
        if score < NEAR_MATCH and page.via != "browser":  # maybe JS-rendered: try the real browser
            rendered = fetch(ev.url, force_browser=True)
            rscore = quote_score(ev.quote, rendered.text) if rendered.text else 0.0
            if rscore > score:
                score, via = rscore, "browser"
        status = "verified" if score >= 0.999 else "near" if score >= NEAR_MATCH else (
            "unreachable" if page.via == "error" and via == "error" else "not_found")
        items.append({"field": ev.field, "url": ev.url, "status": status, "score": round(score, 3),
                      "via": via, "primary": _is_primary(ev.url, rec, roots)})
    supported = {f: any(i["field"] == f and i["status"] in ("verified", "near") for i in items) for f in GRADED_FIELDS}
    primary = {f: any(i["field"] == f and i["status"] in ("verified", "near") and i["primary"] for i in items)
               for f in GRADED_FIELDS}
    return {"items": items, "supported": supported, "primary_supported": primary}


def run_checks(stage: str) -> dict:
    src = ROOT / "data" / stage
    rows = {}
    files = sorted(src.glob("*.json"))
    records = []
    for path in files:
        body = json.loads(path.read_text(encoding="utf-8"))
        if body.get("record"):
            records.append(AppRecord.model_validate(body["record"]))
        else:
            rows[path.stem] = {"error": body.get("error", "no record")}
    with ThreadPoolExecutor(FETCH_WORKERS) as pool:
        results = list(pool.map(check_evidence, records))
    for rec, ev in zip(records, results):
        unsupported = [f for f, ok in ev["supported"].items() if not ok]
        rows[f"{rec.n:03d}"] = {"lint": lint(rec), "evidence": ev, "unsupported_fields": unsupported}
    for n in APPS:  # an app with no record at all is flagged too
        rows.setdefault(f"{n:03d}", {"error": "no record"})
    out = ROOT / "data" / f"checks_{stage}.json"
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    flagged = sorted(int(k) for k, r in rows.items() if needs_critic(r))
    (ROOT / "data" / f"flagged_{stage}.json").write_text(json.dumps(flagged), encoding="utf-8")
    log.info("%s: %d records, %d flagged for the critic -> %s", stage, len(rows), len(flagged), out.name)
    return rows


def needs_critic(row: dict) -> bool:
    """Critic policy: re-open an app if any loop raised anything about it."""
    if row.get("error"):
        return True
    unsupported = row["unsupported_fields"]
    non_primary = [f for f, ok in row["evidence"]["primary_supported"].items() if not ok]
    return bool(row["lint"] or unsupported or non_primary)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", default="pass1")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    run_checks(args.stage)


if __name__ == "__main__":
    main()
