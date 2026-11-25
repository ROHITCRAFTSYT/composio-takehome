"""Write data/gold/REVIEW.md: one checklist block per gold app, for the human reviewer.

    python -m agent.gold_review
"""

from __future__ import annotations

import json

from .runner import ROOT
from .schema import GRADED_FIELDS

GOLD = ROOT / "data" / "gold"


def main() -> None:
    lines = ["# Gold sample review", "",
             "For each app: open each link, confirm the quote is there and the label follows RUBRIC.md.",
             "Tick the box, or write the corrected value next to it. Then set GOLD_HUMAN_REVIEWED = True in agent/build_site.py.", ""]
    for path in sorted(GOLD.glob("[0-9]*.json")):
        g = json.loads(path.read_text(encoding="utf-8"))
        lines += [f"## {g['n']}. {g['app']}", "", f"_{g.get('notes', '')}_", ""]
        for f in GRADED_FIELDS:
            lines.append(f"- [ ] **{f}**: `{g[f]}`")
            for e in (e for e in g["evidence"] if e["field"] == f):
                lines.append(f"  - \"{e['quote']}\" <{e['url']}>")
        lines.append("")
    (GOLD / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {GOLD / 'REVIEW.md'}")


if __name__ == "__main__":
    main()
