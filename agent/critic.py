"""Stage 3 - critic agent (L3). A fresh agent that did not do the research gets the pass-1
record plus everything L1/L2 flagged, re-checks against primary docs and returns a
corrected record (pass 2). Every app is re-checked; flagged fields get a forced re-research.

    python -m agent.critic --apps 1-100 --workers 6
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging

from .research import APPS, parse_range
from .runner import ROOT, load_prompt, run_agent, save_run

log = logging.getLogger("critic")
IN_DIR, OUT_DIR = ROOT / "data" / "pass1", ROOT / "data" / "pass2"

SYSTEM_PROMPT = load_prompt("critic")


def critic_prompt(app: dict, draft: dict | None, checks: dict) -> str:
    if draft is None:
        return (f"App #{app['n']}: {app['app']} (hint {app['hint']}). The first agent failed to produce a record "
                f"({checks.get('error', 'unknown')}). Research it from scratch and return the record.")
    must = sorted(set(checks.get("unsupported_fields", [])))
    items = checks.get("evidence", {}).get("items", [])
    bad_ev = [f"- {i['field']}: {i['url']} -> {i['status']}{'' if i['primary'] else ' (non-vendor source)'}"
              for i in items if i["status"] not in ("verified", "near") or not i["primary"]]
    lint = checks.get("lint", [])
    return "\n".join([
        f"App #{app['n']}: {app['app']} (hint {app['hint']}, category {app['category']})",
        "DRAFT RECORD:", json.dumps(draft, indent=1, ensure_ascii=False),
        "CONSISTENCY ISSUES (L1):", *(f"- {x}" for x in lint or ["none"]),
        "EVIDENCE PROBLEMS (L2, quote not found on page or non-vendor source):", *(bad_ev or ["- none"]),
        "MUST RE-CHECK (in addition to access, mcp, verdict): " + (", ".join(must) if must else "nothing else flagged"),
        "Return the corrected record.",
    ])


async def critique_all(numbers: list[int], workers: int, model: str, overwrite: bool) -> None:
    checks = json.loads((ROOT / "data" / "checks_pass1.json").read_text(encoding="utf-8"))
    sem = asyncio.Semaphore(workers)

    async def one(app: dict) -> None:
        out = OUT_DIR / f"{app['n']:03d}.json"
        if out.exists() and not overwrite and json.loads(out.read_text(encoding="utf-8")).get("record"):
            return
        src = IN_DIR / f"{app['n']:03d}.json"
        draft = json.loads(src.read_text(encoding="utf-8")).get("record") if src.exists() else None
        prompt = critic_prompt(app, draft, checks.get(f"{app['n']:03d}", {}))
        async with sem:
            run = await run_agent(app, SYSTEM_PROMPT, prompt, model=model)
        save_run(run, out, "pass2")
        log.info("#%03d %-28s %s  %d turns %.0fs", app["n"], app["app"],
                 "ok" if run.record else f"FAIL {run.error[:100]}", run.turns, run.seconds)

    await asyncio.gather(*(one(a) for a in APPS if a["n"] in numbers))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apps", default="1-100")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    asyncio.run(critique_all(parse_range(args.apps), args.workers, args.model, args.overwrite))


if __name__ == "__main__":
    main()
