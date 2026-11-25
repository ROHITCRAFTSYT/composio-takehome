"""Build the single-file case study: site/template.html + aggregated data -> site/index.html.

    python -m agent.build_site
"""

from __future__ import annotations

import json
import logging

from .aggregate import SITE, build, write

log = logging.getLogger("build_site")
REPO = "ROHITCRAFTSYT/composio-toolkit-research"
# Flip to True only after a person has gone through data/gold/REVIEW.md against the cited pages.
GOLD_HUMAN_REVIEWED = False

HUMAN_STEPS = [
    "<b>Writing the rubric.</b> Deciding what counts as \"self-serve\", \"official MCP\" or \"blocked\" is a product call, not a lookup; the agents only apply it.",
    "<b>Reviewing the gold sample.</b> The 20 reference labels were drafted blind from vendor docs; a person checks each one against its cited page (data/gold/REVIEW.md).",
    "<b>Judgement calls the rubric leaves open</b> (e.g. a free sandbox but paid production; an MCP that only searches docs). These are listed as misses rather than hidden.",
    "<b>Network access.</b> Some vendor doc hosts refuse automated clients from this network (Meta, Salesforce developer docs); a reader-proxy fallback was added after seeing it.",
    "<b>Accounts.</b> Composio login and model access; no vendor accounts were created, so \"gated\" findings come from docs and pricing pages, not from trying to sign up.",
]
GOLD_NOTE = (
    "<b>How the gold sample was made.</b> 20 apps, 2 per category, drawn with a fixed seed (<code>agent/sample.py</code>) so they "
    "were not cherry-picked. Labels were drafted by separate Claude agents (Opus) that ran before the pipeline and never saw its "
    "output, using different tools (plain web search/fetch), with a verbatim vendor-doc quote for every field; 130/135 quotes were then re-found on the live pages by "
    "the same evidence checker (the 5 misses are one single-page-app docs site). "
    + ("Then every label was reviewed by hand against its cited page (data/gold/REVIEW.md). " if GOLD_HUMAN_REVIEWED
       else "<b>Human review of these labels is still pending.</b> ")
    + "Caveat: the gold drafts also come from a Claude model, so agents and gold can share blind spots; the human "
    "review is what guards against that. "
    + "Accuracy here means agreement with RUBRIC.md, so a strict rubric makes some misses arguable; they are shown, not dropped."
)
FOOTER = (
    f"Built for the Composio AI Product Ops take-home · Rohit · source and data: "
    f"<a href=\"https://github.com/{REPO}\">github.com/{REPO}</a> · research run with Composio (search) + Claude agents · "
    "every record carries its evidence and tool-call log."
)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    out = build()
    out.update(human_steps=HUMAN_STEPS, gold_note=GOLD_NOTE, footer=FOOTER)
    write(out)
    template = (SITE / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(out, ensure_ascii=False).replace("</", "<\\/")  # keep </script> out of the JSON block
    html = template.replace("/*__DATA__*/", payload).replace("__REPONAME__", REPO.split("/")[1]).replace("__REPO__", REPO).replace(
        "__GOLD_REVIEW__", "reviewed by hand" if GOLD_HUMAN_REVIEWED else "human review pending")
    (SITE / "index.html").write_text(html, encoding="utf-8")
    log.info("site/index.html written (%d KB)", len(html) // 1024)


if __name__ == "__main__":
    main()
