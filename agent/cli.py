"""Command-line face of the pipeline, for agents that act through a shell (Claude Code
subagents, or any coding agent). Same tools, prompts and schema as the SDK runner.

    python -m agent.cli brief  pass1 12                      # full instructions for app 12
    python -m agent.cli search pass1 12 "Intercom API auth" --domains developers.intercom.com
    python -m agent.cli fetch  pass1 12 https://developers.intercom.com/... --find OAuth,token
    python -m agent.cli save   pass1 12 draft.json           # validate + store the record

Every search/fetch is appended to data/logs/<stage>/<n>.jsonl, so the tool trace of each
record is kept next to it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")  # urllib3 SOCKS notice pulled in by trafilatura; noise for agents

from pydantic import ValidationError

from .runner import ROOT, load_prompt
from .schema import AppRecord, record_json_schema
from .toolkit import composio_search, page_excerpt

APPS = {a["n"]: a for a in json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))}
STAGES = ("pass1", "pass2")
TOOL_MAP = """
HOW TO CALL YOUR TOOLS (shell commands, run from the repo root):
- composio_search: python -m agent.cli search {stage} {n} "<query>" [--domains a.com,b.com]
- fetch_page:      python -m agent.cli fetch {stage} {n} <url> [--find word1,word2]
Do not use any other web tool. When done, write the record JSON (fields below, without n/app/category)
to a temp file and run: python -m agent.cli save {stage} {n} <file>. Fix and re-save if it reports errors.
Record JSON schema:
{schema}
"""


def _log(stage: str, n: int, entry: dict) -> None:
    path = ROOT / "data" / "logs" / stage / f"{n:03d}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": round(time.time(), 1), **entry}, ensure_ascii=False) + "\n")


def brief(stage: str, n: int) -> str:
    app = APPS[n]
    schema = json.dumps(record_json_schema(), separators=(",", ":"))
    tools = TOOL_MAP.format(stage=stage, n=n, schema=schema)
    if stage == "pass1":
        from .research import user_prompt
        return load_prompt("researcher") + tools + "\nTASK:\n" + user_prompt(app)
    from .critic import IN_DIR, critic_prompt
    checks = json.loads((ROOT / "data" / "checks_pass1.json").read_text(encoding="utf-8"))
    src = IN_DIR / f"{n:03d}.json"
    draft = json.loads(src.read_text(encoding="utf-8")).get("record") if src.exists() else None
    return load_prompt("critic") + tools + "\nTASK:\n" + critic_prompt(app, draft, checks.get(f"{n:03d}", {}))


def save(stage: str, n: int, file: Path) -> int:
    app = APPS[n]
    try:
        payload = json.loads(file.read_text(encoding="utf-8"))
        payload = {k: v for k, v in payload.items() if k not in ("n", "app", "category")}
        record = AppRecord.model_validate({**payload, "n": n, "app": app["app"], "category": app["category"]})
    except (json.JSONDecodeError, ValidationError) as exc:
        print(f"INVALID, fix and re-save:\n{exc}")
        return 1
    log_path = ROOT / "data" / "logs" / stage / f"{n:03d}.jsonl"
    calls = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()] if log_path.exists() else []
    out = ROOT / "data" / stage / f"{n:03d}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    body = {"stage": stage, "backend": "claude-code-subagent", "record": record.model_dump(), "error": "",
            "meta": {"tool_calls": [{"tool": c["tool"], "input": c["input"]} for c in calls]}}
    out.write_text(json.dumps(body, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"saved {out.relative_to(ROOT)} ({len(record.evidence)} evidence items)")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("brief", "search", "fetch", "save"):
        p = sub.add_parser(name)
        p.add_argument("stage", choices=STAGES)
        p.add_argument("n", type=int)
        if name == "search":
            p.add_argument("query")
            p.add_argument("--domains", default="")
        elif name == "fetch":
            p.add_argument("url")
            p.add_argument("--find", default="")
        elif name == "save":
            p.add_argument("file", type=Path)
    args = parser.parse_args()

    if args.cmd == "brief":
        print(brief(args.stage, args.n))
    elif args.cmd == "search":
        domains = [d for d in args.domains.split(",") if d]
        _log(args.stage, args.n, {"tool": "composio_search", "input": {"query": args.query, "domains": domains}})
        try:
            print(json.dumps(composio_search(args.query, domains or None), ensure_ascii=False, indent=1))
        except RuntimeError as exc:
            print(f"SEARCH FAILED: {exc}")
    elif args.cmd == "fetch":
        find = [w for w in args.find.split(",") if w]
        _log(args.stage, args.n, {"tool": "fetch_page", "input": {"url": args.url, "find": find}})
        print(page_excerpt(args.url, find or None))
    else:
        return save(args.stage, args.n, args.file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
