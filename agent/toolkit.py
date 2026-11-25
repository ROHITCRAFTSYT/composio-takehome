"""Plain research tools (no agent-framework dependency), shared by every agent backend.

- composio_search: web search through Composio (Tavily toolkit via `composio execute`).
- fetch_page: our own fetcher (httpx, headless-browser fallback, disk cache), so
  quotes the agent cites can be re-checked byte-for-byte by the evidence loop.

Built-in WebFetch is deliberately not given to the agents: it returns a model
summary, not page text, so "verbatim" quotes from it cannot be verified.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from .fetch import fetch

COMPOSIO_BIN = os.environ.get("COMPOSIO_BIN") or shutil.which("composio") or str(
    Path.home() / ".composio" / ("composio.exe" if os.name == "nt" else "composio")
)
SEARCH_RESULTS = 6
SNIPPET_CHARS = 400
PAGE_CHARS = 7_000
WINDOW_CHARS = 500
MAX_WINDOWS = 6
COMPOSIO_TIMEOUT_S = 90


def composio_search(query: str, include_domains: list[str] | None = None) -> list[dict[str, str]]:
    """Run TAVILY_SEARCH through the Composio CLI and return url/title/snippet rows."""
    payload = {
        "query": query,
        "max_results": SEARCH_RESULTS,
        "search_depth": "basic",  # managed Tavily on Composio allows basic only
        "include_answer": False,
        "include_domains": include_domains or [],
    }
    proc = subprocess.run(
        [COMPOSIO_BIN, "execute", "TAVILY_SEARCH", "-d", json.dumps(payload)],
        capture_output=True, text=True, encoding="utf-8", timeout=COMPOSIO_TIMEOUT_S,
    )
    try:
        body = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"composio execute failed: {proc.stderr.strip()[:300]}") from exc
    if not body.get("successful"):
        raise RuntimeError(f"composio search error: {str(body.get('error'))[:300]}")
    return [
        {"url": r.get("url", ""), "title": r.get("title", ""), "snippet": (r.get("content") or "")[:SNIPPET_CHARS]}
        for r in body["data"].get("results", [])
    ]


def page_excerpt(url: str, find: list[str] | None = None) -> str:
    """Page text for the agent: keyword windows when `find` is given, else the head."""
    page = fetch(url)
    if page.via == "error" or not page.text:
        return f"FETCH FAILED for {url}: {page.error or 'empty page'}"
    header = f"URL: {page.final_url} (status {page.status}, via {page.via}, {len(page.text)} chars)\n"
    text = page.text
    if not find:
        return header + text[:PAGE_CHARS]
    windows: list[str] = []
    for term in find:
        for match in re.finditer(re.escape(term), text, flags=re.IGNORECASE):
            start = max(0, match.start() - WINDOW_CHARS // 2)
            windows.append(f"...{text[start:start + WINDOW_CHARS]}...")
            if len(windows) >= MAX_WINDOWS:
                break
        if len(windows) >= MAX_WINDOWS:
            break
    if not windows:
        return header + f"No matches for {find}. Page head:\n" + text[:PAGE_CHARS // 2]
    return header + "\n\n".join(windows)
