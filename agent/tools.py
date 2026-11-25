"""Claude Agent SDK wrappers around agent.toolkit (in-process MCP server)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

from .toolkit import composio_search, page_excerpt


def _text(result: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": result}]}


@tool(
    "composio_search",
    "Web search via Composio (Tavily). Use for finding official docs pages. "
    "Optionally restrict to domains, e.g. ['developers.hubspot.com'].",
    {"query": str, "include_domains": list},
)
async def search_tool(args: dict[str, Any]) -> dict[str, Any]:
    try:
        rows = await asyncio.to_thread(composio_search, args["query"], args.get("include_domains") or None)
    except Exception as exc:  # noqa: BLE001 - reported to the agent so it can rephrase
        return _text(f"SEARCH FAILED: {exc}")
    return _text(json.dumps(rows, ensure_ascii=False, indent=1))


@tool(
    "fetch_page",
    "Fetch a web page as plain text (renders JS pages in a headless browser if needed). "
    "Pass `find` (list of keywords) to get only the passages around those words. "
    "Quotes you cite as evidence must be copied from this tool's output.",
    {"url": str, "find": list},
)
async def fetch_tool(args: dict[str, Any]) -> dict[str, Any]:
    result = await asyncio.to_thread(page_excerpt, args["url"], args.get("find") or None)
    return _text(result)


TOOL_SERVER = create_sdk_mcp_server(name="research", version="1.0.0", tools=[search_tool, fetch_tool])
TOOL_NAMES = ["mcp__research__composio_search", "mcp__research__fetch_page"]
