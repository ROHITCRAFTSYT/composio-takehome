"""Turn records + checks + coverage + accuracy into the page's data and machine-readable exports.

    python -m agent.aggregate        # writes site/data.json, site/results.csv, site/results.json
"""

from __future__ import annotations

import csv
import json
import logging
from collections import Counter, defaultdict

from .runner import ROOT
from .schema import GRADED_FIELDS, SELF_SERVE

log = logging.getLogger("aggregate")
SITE = ROOT / "site"
DATA = ROOT / "data"
APPS = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
CSV_FIELDS = ("n", "app", "category", "one_liner", "auth_methods", "access", "api_style", "api_breadth", "mcp",
              "verdict", "main_blocker", "composio", "docs_url", "mcp_url", "confidence", "evidence_verified",
              "changed_by_critic", "notes")


def _read(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _records(stage: str) -> dict[int, dict]:
    out = {}
    for path in sorted((DATA / stage).glob("[0-9]*.json")):
        body = _read(path)
        if body and body.get("record"):
            out[body["record"]["n"]] = body
    return out


def _changed_fields(a: dict, b: dict) -> list[str]:
    fields = [*GRADED_FIELDS, "main_blocker"]
    return [f for f in fields if (set(a[f]) if f == "auth_methods" else a[f]) != (set(b[f]) if f == "auth_methods" else b[f])]


def _loop_stats(stage: str, records: dict[int, dict]) -> dict:
    checks = _read(DATA / f"checks_{stage}.json") or {}
    rows = [checks.get(f"{n:03d}") for n in records]
    rows = [r for r in rows if r and "lint" in r]
    items = [i for r in rows for i in r["evidence"]["items"]]
    field_total = len(rows) * len(GRADED_FIELDS)
    supported = sum(v for r in rows for v in r["evidence"]["supported"].values())
    primary = sum(v for r in rows for v in r["evidence"]["primary_supported"].values())
    return {
        "records": len(records),
        "apps_with_lint_issues": sum(1 for r in rows if r["lint"]),
        "lint_issues": sum(len(r["lint"]) for r in rows),
        "quotes": len(items),
        "quotes_verified": sum(1 for i in items if i["status"] in ("verified", "near")),
        "quotes_not_found": sum(1 for i in items if i["status"] == "not_found"),
        "quotes_unreachable": sum(1 for i in items if i["status"] == "unreachable"),
        "quotes_via_browser": sum(1 for i in items if i["via"] == "browser"),
        "fields_supported_pct": round(100 * supported / field_total, 1) if field_total else 0,
        "fields_primary_supported_pct": round(100 * primary / field_total, 1) if field_total else 0,
        "lint_examples": [x for r in rows for x in r["lint"]][:200],
    }


def build() -> dict:
    p1, p2 = _records("pass1"), _records("pass2")
    final = {n: (p2.get(n) or p1.get(n)) for n in range(1, 101) if (p2.get(n) or p1.get(n))}
    coverage = {c["n"]: c for c in _read(DATA / "composio_coverage.json") or []}
    checks_final = _read(DATA / "checks_pass2.json") or _read(DATA / "checks_pass1.json") or {}
    accuracy = _read(DATA / "accuracy.json") or {}
    gold = {g["n"]: g for g in (_read(p) for p in sorted((DATA / "gold").glob("[0-9]*.json")))}

    rows = []
    for app in APPS:
        body = final.get(app["n"])
        if not body:
            rows.append({**app, "missing": True})
            continue
        rec = body["record"]
        chk = checks_final.get(f"{app['n']:03d}", {})
        ev_items = {(i["field"], i["url"]): i for i in chk.get("evidence", {}).get("items", [])}
        cov = coverage.get(app["n"], {"status": "none", "slug": ""})
        before = p1.get(app["n"], {}).get("record")
        rows.append({
            **{k: rec[k] for k in ("n", "app", "category", "one_liner", "auth_methods", "access", "api_style",
                                   "api_breadth", "mcp", "mcp_url", "verdict", "main_blocker", "docs_url",
                                   "confidence")},
            "hint": app["hint"],
            "notes": " | ".join(x for x in (rec["auth_notes"], rec["access_notes"], rec["api_notes"],
                                            rec["blocker_notes"]) if x),
            "composio": cov["status"], "composio_slug": cov.get("slug", ""),
            "evidence": [{**e, **{k: ev_items.get((e["field"], e["url"]), {}).get(k) for k in ("status", "primary")}}
                         for e in rec["evidence"]],
            "evidence_verified": sum(1 for v in chk.get("evidence", {}).get("supported", {}).values() if v),
            "changed_by_critic": _changed_fields(before, rec) if before and app["n"] in p2 else [],
            "pass1": {f: before[f] for f in (*GRADED_FIELDS, "main_blocker")} if before else None,
            "in_gold": app["n"] in gold,
            "tool_calls": sum(len((src.get(app["n"]) or {}).get("meta", {}).get("tool_calls", [])) for src in (p1, p2)),
        })
    present = [r for r in rows if not r.get("missing")]

    cats = sorted({r["category"] for r in present}, key=lambda c: min(r["n"] for r in present if r["category"] == c))
    by_cat = defaultdict(list)
    for r in present:
        by_cat[r["category"]].append(r)
    auth_counter = Counter(m for r in present for m in r["auth_methods"])
    patterns = {
        "n": len(present),
        "auth": dict(auth_counter.most_common()),
        "auth_combo": dict(Counter("+".join(sorted(r["auth_methods"])) for r in present).most_common()),
        "access": dict(Counter(r["access"] for r in present).most_common()),
        "verdict": dict(Counter(r["verdict"] for r in present).most_common()),
        "blocker": dict(Counter(r["main_blocker"] for r in present if r["main_blocker"] != "none").most_common()),
        "mcp": dict(Counter(r["mcp"] for r in present).most_common()),
        "api_style": dict(Counter(r["api_style"] for r in present).most_common()),
        "composio": dict(Counter(r["composio"] for r in present).most_common()),
        "by_category": [{
            "category": c,
            "self_serve": sum(r["access"] in SELF_SERVE for r in by_cat[c]),
            "access": dict(Counter(r["access"] for r in by_cat[c])),
            "verdict": dict(Counter(r["verdict"] for r in by_cat[c])),
            "mcp_official": sum(r["mcp"] == "official" for r in by_cat[c]),
            "oauth2": sum("oauth2" in r["auth_methods"] for r in by_cat[c]),
            "total": len(by_cat[c]),
        } for c in cats],
        "easy_wins": [r["app"] for r in present if r["composio"] == "none" and r["verdict"] == "ready"],
        "needs_review": [r["app"] for r in present if r["composio"] == "none" and r["verdict"] == "ready_with_review"],
        "needs_outreach": [r["app"] for r in present if r["verdict"] == "blocked"
                           and r["main_blocker"] in ("contact_sales", "partner_program", "paid_plan")],
        "not_buildable": [r["app"] for r in present if r["main_blocker"] in ("no_public_api", "not_a_saas")],
    }
    critic = Counter(f for r in present for f in r["changed_by_critic"])
    out = {
        "generated_from": {"pass1": len(p1), "pass2": len(p2), "gold": len(gold)},
        "rows": rows, "patterns": patterns, "accuracy": accuracy,
        "loops": {"pass1": _loop_stats("pass1", p1), "pass2": _loop_stats("pass2", p2) if p2 else None,
                  "critic_changed_fields": dict(critic.most_common()),
                  "critic_changed_apps": sum(1 for r in present if r["changed_by_critic"])},
        "gold": list(gold.values()),
    }
    return out


def write(out: dict) -> None:
    SITE.mkdir(exist_ok=True)
    (SITE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    slim = [{k: r.get(k) for k in (*CSV_FIELDS, "evidence")} for r in out["rows"]]
    (SITE / "results.json").write_text(json.dumps(slim, indent=1, ensure_ascii=False), encoding="utf-8")
    with (SITE / "results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in out["rows"]:
            writer.writerow({**r, "auth_methods": "+".join(r.get("auth_methods", [])),
                             "changed_by_critic": "+".join(r.get("changed_by_critic", []))})
    log.info("wrote site/data.json, results.json, results.csv (%d rows)", len(out["rows"]))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    write(build())


if __name__ == "__main__":
    main()
