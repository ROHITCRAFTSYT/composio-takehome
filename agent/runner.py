"""Thin wrapper around the Claude Agent SDK: run one agent, get one validated record."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock, query
from pydantic import ValidationError

from .schema import AppRecord, record_json_schema
from .tools import TOOL_NAMES, TOOL_SERVER

ROOT = Path(__file__).resolve().parent.parent
RUBRIC = (ROOT / "RUBRIC.md").read_text(encoding="utf-8")
PROMPT_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(name: str) -> str:
    """System prompt = role instructions (agent/prompts/<name>.md) + the shared rubric."""
    return (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8") + "\n" + RUBRIC


DEFAULT_MODEL = "sonnet"
MAX_TURNS = 30


@dataclass
class AgentRun:
    record: AppRecord | None
    error: str = ""
    turns: int = 0
    seconds: float = 0.0
    cost_usd: float = 0.0
    tool_calls: list[dict[str, Any]] = field(default_factory=list)


async def run_agent(app: dict[str, Any], system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL) -> AgentRun:
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model,
        mcp_servers={"research": TOOL_SERVER},
        tools=[],  # no built-in tools: only our two research tools
        allowed_tools=TOOL_NAMES,
        max_turns=MAX_TURNS,
        permission_mode="bypassPermissions",
        output_format={"type": "json_schema", "schema": record_json_schema()},
        setting_sources=[],  # ignore user/project settings, hooks and CLAUDE.md
        cwd=str(ROOT),
    )
    started = time.monotonic()
    tool_calls: list[dict[str, Any]] = []
    result: ResultMessage | None = None
    try:
        async for message in query(prompt=user_prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        tool_calls.append({"tool": block.name.split("__")[-1], "input": block.input})
            elif isinstance(message, ResultMessage):
                result = message
    except Exception as exc:  # noqa: BLE001 - one app failing must not stop the batch
        return AgentRun(None, f"agent crashed: {exc!r}"[:500], seconds=time.monotonic() - started, tool_calls=tool_calls)

    run = AgentRun(None, seconds=time.monotonic() - started, tool_calls=tool_calls)
    if result is None:
        run.error = "no result message"
        return run
    run.turns, run.cost_usd = result.num_turns, result.total_cost_usd or 0.0
    payload = result.structured_output
    if payload is None and result.result:
        try:
            payload = json.loads(result.result)
        except json.JSONDecodeError:
            payload = None
    if payload is None:
        run.error = f"no structured output ({result.subtype}, {result.terminal_reason})"
        return run
    try:
        run.record = AppRecord.model_validate({**payload, "n": app["n"], "app": app["app"], "category": app["category"]})
    except ValidationError as exc:
        run.error = f"schema validation failed: {exc}"[:800]
    return run


def save_run(run: AgentRun, path: Path, stage: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "stage": stage,
        "record": run.record.model_dump() if run.record else None,
        "error": run.error,
        "meta": {"turns": run.turns, "seconds": round(run.seconds, 1), "cost_usd": round(run.cost_usd, 4),
                 "tool_calls": run.tool_calls},
    }
    path.write_text(json.dumps(body, indent=1, ensure_ascii=False), encoding="utf-8")
