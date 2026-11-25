"""Score each pass against the gold sample (see data/gold/REVIEW.md for human-review status), field by field.

    python -m agent.score
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .runner import ROOT
from .schema import GRADED_FIELDS, SELF_SERVE

log = logging.getLogger("score")
GOLD_DIR = ROOT / "data" / "gold"
OUT = ROOT / "data" / "accuracy.json"
PASSES = ("pass1", "pass2")


def _load(stage: str, n: int) -> dict | None:
    path = ROOT / "data" / stage / f"{n:03d}.json"
    return json.loads(path.read_text(encoding="utf-8")).get("record") if path.exists() else None


def field_match(field: str, got: object, want: object) -> bool:
    if field == "auth_methods":
        return set(got or []) == set(want or [])
    return got == want


def score_pass(stage: str, gold: list[dict]) -> dict:
    per_field = {f: {"right": 0, "total": 0} for f in (*GRADED_FIELDS, "self_serve_binary")}
    misses = []
    for g in gold:
        rec = _load(stage, g["n"])
        for f in GRADED_FIELDS:
            per_field[f]["total"] += 1
            got = rec.get(f) if rec else None
            if rec and field_match(f, got, g[f]):
                per_field[f]["right"] += 1
            else:
                misses.append({"n": g["n"], "app": g["app"], "field": f, "got": got, "gold": g[f]})
        per_field["self_serve_binary"]["total"] += 1
        if rec and (rec["access"] in SELF_SERVE) == (g["access"] in SELF_SERVE):
            per_field["self_serve_binary"]["right"] += 1
    graded = [per_field[f] for f in GRADED_FIELDS]
    right, total = sum(x["right"] for x in graded), sum(x["total"] for x in graded)
    apps_perfect = len({g["n"] for g in gold}) - len({m["n"] for m in misses})
    return {
        "field_accuracy": round(right / total, 3) if total else 0.0,
        "right": right, "total": total, "apps_all_fields_right": apps_perfect, "apps": len(gold),
        "per_field": {f: {**v, "acc": round(v["right"] / v["total"], 3) if v["total"] else 0.0}
                      for f, v in per_field.items()},
        "misses": misses,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    gold = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(GOLD_DIR.glob("[0-9]*.json"))]
    result = {"gold_apps": [g["n"] for g in gold]}
    for stage in PASSES:
        if any((ROOT / "data" / stage).glob("[0-9]*.json")):
            result[stage] = score_pass(stage, gold)
            log.info("%s: %.1f%% field accuracy (%d/%d), %d/%d apps fully right", stage,
                     100 * result[stage]["field_accuracy"], result[stage]["right"], result[stage]["total"],
                     result[stage]["apps_all_fields_right"], len(gold))
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
