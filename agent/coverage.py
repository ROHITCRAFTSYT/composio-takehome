"""Which of the 100 apps does Composio already ship a toolkit for?

Queries the live Composio catalog (`composio dev toolkits list --query <app>`) per app and
accepts a match only when the toolkit name/slug equals the app name after normalising.

    python -m agent.coverage
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

from .runner import ROOT
from .toolkit import COMPOSIO_BIN, COMPOSIO_TIMEOUT_S

log = logging.getLogger("coverage")
APPS = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "composio_coverage.json"
# Catalog names that differ from the list's names (checked by hand against the catalog).
ALIASES = {
    "Zoho CRM": ["zoho"], "Close": ["close"], "Lark (Larksuite)": ["lark", "larksuite"],
    "WhatsApp Business": ["whatsapp"], "Meta Ads": ["metaads", "facebookads"], "Threads (Meta)": ["threads"],
    "Magento (Adobe Commerce)": ["magento", "adobecommerce"], "Amazon Selling Partner": ["amazonsellingpartner", "amazon"], "Otter AI": ["otterai", "otter"],
    "Monday.com": ["monday"], "GoHighLevel": ["highlevel", "highlevelagency", "highlevellocation"], "Jira": ["jira"],
    "YouTube Transcript": ["youtubetranscript", "transcriptapi"], "Waterfall.io": ["waterfall", "waterfallio"],
    "Salesforce Commerce Cloud": ["salesforcecommercecloud"], "MongoDB Atlas": ["mongodbatlas", "mongodb"],
    "Paygent Connect": ["paygent", "paygentconnect"], "Mermaid CLI": ["mermaid", "mermaidcli"],
}


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _query(term: str) -> list[dict]:
    proc = subprocess.run([COMPOSIO_BIN, "dev", "toolkits", "list", "--query", term, "--limit", "25"],
                          capture_output=True, text=True, encoding="utf-8", timeout=COMPOSIO_TIMEOUT_S)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        log.warning("catalog query failed for %s: %s", term, proc.stderr.strip()[:200])
        return []


def lookup(app: dict) -> dict:
    """native = regular toolkit, mcp = MCP-backed toolkit, listed_empty = catalog entry with 0 tools."""
    wanted = {_key(app["app"]), *ALIASES.get(app["app"], [])}
    terms = {re.sub(r"\s*\(.*\)", "", app["app"]), *ALIASES.get(app["app"], [])[:1]}
    hits: list[dict] = []
    for term in terms:
        for tk in _query(term):
            base = _key(re.sub(r"_mcp$", "", tk["slug"]))
            if _key(tk["name"]) in wanted or _key(tk["slug"]) in wanted or base in wanted:
                hits.append(tk)
    if not hits:
        return {"n": app["n"], "status": "none", "slug": "", "tools": 0}
    best = max(hits, key=lambda t: (not t["slug"].endswith("_mcp"), t.get("tools_count", 0)))
    tools = best.get("tools_count", 0)
    status = "listed_empty" if tools == 0 else ("mcp" if best["slug"].endswith("_mcp") else "native")
    return {"n": app["n"], "status": status, "slug": best["slug"], "tools": tools}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    with ThreadPoolExecutor(8) as pool:
        rows = list(pool.map(lookup, APPS))
    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    counts = {k: sum(r["status"] == k for r in rows) for k in ("native", "mcp", "listed_empty", "none")}
    log.info("Composio coverage %s -> %s", counts, OUT.name)


if __name__ == "__main__":
    main()
