"""Pick the gold sample: 2 apps per category, seeded so the pick is reproducible and not cherry-picked."""

from __future__ import annotations

import json
import random
from collections import defaultdict

from .runner import ROOT

SEED = 20261124
PER_CATEGORY = 2


def gold_sample() -> list[int]:
    apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
    by_cat: dict[str, list[int]] = defaultdict(list)
    for app in apps:
        by_cat[app["category"]].append(app["n"])
    rng = random.Random(SEED)
    return sorted(n for cat in sorted(by_cat) for n in rng.sample(by_cat[cat], PER_CATEGORY))


if __name__ == "__main__":
    print(gold_sample())
