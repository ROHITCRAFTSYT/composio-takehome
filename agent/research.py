"""Stage 1 - research agent. One Claude agent per app, Composio search + page fetch tools.

    python -m agent.research --apps 1-100 --workers 6
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging

from .runner import ROOT, load_prompt, run_agent, save_run

log = logging.getLogger("research")
APPS = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
OUT_DIR = ROOT / "data" / "pass1"

SYSTEM_PROMPT = load_prompt("researcher")


def user_prompt(app: dict) -> str:
    return (
        f"App #{app['n']}: {app['app']}\nCategory given: {app['category']}\nHint: {app['hint']}\n"
        "Research it and return the record."
    )


def parse_range(spec: str) -> list[int]:
    picked: list[int] = []
    for part in spec.split(","):
        lo, _, hi = part.partition("-")
        picked.extend(range(int(lo), int(hi or lo) + 1))
    return picked


async def research_all(numbers: list[int], workers: int, model: str, overwrite: bool) -> None:
    sem = asyncio.Semaphore(workers)
    todo = [a for a in APPS if a["n"] in numbers]

    async def one(app: dict) -> None:
        path = OUT_DIR / f"{app['n']:03d}.json"
        if path.exists() and not overwrite:
            prev = json.loads(path.read_text(encoding="utf-8"))
            if prev.get("record"):
                return
        async with sem:
            run = await run_agent(app, SYSTEM_PROMPT, user_prompt(app), model=model)
        save_run(run, path, "pass1")
        status = "ok" if run.record else f"FAIL {run.error[:120]}"
        log.info("#%03d %-28s %s  %d turns %.0fs", app["n"], app["app"], status, run.turns, run.seconds)

    await asyncio.gather(*(one(a) for a in todo))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apps", default="1-100")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    asyncio.run(research_all(parse_range(args.apps), args.workers, args.model, args.overwrite))


if __name__ == "__main__":
    main()
