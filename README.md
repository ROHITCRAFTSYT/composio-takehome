# Toolkit research agent: 100 apps

Can each of 100 SaaS apps become an AI-agent toolkit today? This repo has the agent
pipeline that answers it, the verification loops that check it, and the case-study page.

- **Case study (live):** https://rohitcraftsyt.github.io/composio-toolkit-research/
- **All 100 records:** [`site/results.csv`](site/results.csv) · [`site/results.json`](site/results.json)
- **Field definitions:** [`RUBRIC.md`](RUBRIC.md)

## What the pipeline does

```
apps.json ─► Researcher agent ─► L1 lint ─► L2 evidence check ─► L3 critic agent ─► score vs gold ─► site
             (per app; Composio     (rubric     (re-fetch each quote:   (fresh agent, only
              search + page fetch)   rules)      HTTP → browser → reader)  flagged items)
```

| Stage | File | What it does |
|---|---|---|
| Tools | `agent/toolkit.py`, `agent/fetch.py` | `composio_search` runs Tavily through `composio execute`; `fetch_page` returns raw page text (httpx → headless Chromium → reader proxy), cached so the verifier sees the same bytes |
| Researcher | `agent/prompts/researcher.md` | One agent per app fills the [`schema`](agent/schema.py) with a verbatim quote per graded field |
| L1 lint | `agent/checks.py` | Rubric consistency: "ready" on a gated app, missing evidence, official MCP with no URL, low confidence... |
| L2 evidence | `agent/checks.py` | Re-fetches every cited URL and fuzzy-matches the quote; flags non-vendor sources |
| L3 critic | `agent/prompts/critic.md` | A fresh, stronger agent gets the draft + every flag; re-derives access, MCP and verdict on every app and re-researches flagged fields; logs each change |
| Composio coverage | `agent/coverage.py` | Live `composio dev toolkits list` per app: already shipped, MCP-backed, or a real gap |
| Gold + score | `agent/sample.py`, `agent/score.py` | 20 seeded-random apps (2 per category) labelled blind; per-field accuracy of pass 1 vs pass 2 |
| Page | `agent/aggregate.py`, `agent/build_site.py` | Patterns + data inlined into one self-contained `site/index.html` |

Every record in `data/pass1/` and `data/pass2/` keeps its tool-call log (`data/logs/`).

## Run it

```bash
pip install -r requirements.txt
playwright install chromium
# Composio CLI: https://docs.composio.dev (curl -fsSL https://composio.dev/install | sh), then:
composio login
```

**Option A: inside Claude Code (no API key; this is how the published run was made)**

```
claude
/research-apps 1-100          # researcher, one subagent per app (Haiku)
/research-apps 1-100 pass2    # loops, then critic on every app (Sonnet)
```

The slash command (`.claude/commands/research-apps.md`) fans out subagents that act only through
`python -m agent.cli` (`brief`, `search`, `fetch`, `save`), so they use the same tools, prompts
and schema validation as option B.

**Option B: headless with the Claude Agent SDK** (`ANTHROPIC_API_KEY` set, or a logged-in Claude Code)

```bash
python -m agent.coverage                 # Composio catalog check
python -m agent.research --apps 1-100    # pass 1
python -m agent.checks --stage pass1     # L1 + L2
python -m agent.critic --apps 1-100      # pass 2
python -m agent.checks --stage pass2
python -m agent.score                    # accuracy vs gold
python -m agent.build_site               # site/index.html
```

Option B is the same pipeline with the SDK's in-process MCP tools (`agent/tools.py`). It was not used
for the published run because the CLI login was unavailable on the build machine; option A was.

## Where a human was needed

- Writing `RUBRIC.md`: "self-serve", "official MCP" and "blocked" are product decisions.
- Reviewing the gold labels (`data/gold/REVIEW.md`) against the cited pages.
- Network: Meta and Salesforce developer docs refuse automated clients from the build network, so a reader-proxy fallback was added.
- Accounts: Composio login and model access. No vendor accounts were made; gated findings come from docs and pricing pages.

## Layout

```
agent/          pipeline code + prompts
data/pass1/     researcher records      data/pass2/   critic records
data/gold/      blind gold labels + REVIEW.md
data/logs/      per-app tool-call logs  data/cache/   fetched pages (git-ignored)
site/           template.html, index.html (built), results.csv/json
```

## Run log (honest notes)

- **Pass 1** (researcher, Haiku, one agent per app): all 100 apps. A first attempt with 5 apps per agent hit the
  Claude usage limit before saving anything; switching to one app per agent cut cost ~3x (context is re-sent each turn).
- **Pass 2** (critic, Sonnet, one agent per app): the critic prompt was frozen before pass 1 was scored against gold.
  After the first 20 apps the usage limit was hit again; for the remaining 80 the critic's tool budget was lowered
  from "5-9 calls" to "at most 5" (same instructions otherwise), and runs were throttled to 10 at a time.
- **Gold sample**: drafted blind by separate agents before pass 1 ran; human review tracked in `data/gold/REVIEW.md`.
