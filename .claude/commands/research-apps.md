---
description: Run the toolkit-research pipeline over a range of apps (e.g. /research-apps 1-100)
argument-hint: "<app range, e.g. 1-100 or 3,12,40-45> [pass1|pass2]"
---

Run the research pipeline in this repo for apps `$ARGUMENTS` (default stage pass1).

1. For pass1, launch one background subagent per app (model haiku), at most 10 at a time. For pass2 (the critic), first run `python -m agent.checks --stage pass1`, then launch one subagent per app (model sonnet). The critic re-derives access, mcp and verdict on every app; the checks add per-app must-fix items.
2. Each subagent gets exactly this task, with N filled in:
   - Run `python -m agent.cli brief <stage> N` and follow it exactly.
   - Only web access: `python -m agent.cli search <stage> N "..."` and `python -m agent.cli fetch <stage> N <url> --find a,b`. No other web tools.
   - Do not open files under data/ or agent/.
   - Write the record JSON to a temp file and run `python -m agent.cli save <stage> N <file>`; fix and re-save on INVALID.
3. When all are done, run in order: `python -m agent.checks --stage <stage>`, `python -m agent.score`, `python -m agent.build_site`, and report counts.
