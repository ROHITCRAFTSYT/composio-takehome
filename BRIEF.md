# Composio — AI Product Ops Intern take-home (captured 2026-11-24)

Source: https://composio.notion.site/AI-Product-Ops-Intern-The-take-home-assignment-391f261a6dfe80e9946bee899d3a3762
Received: 2026-11-23 09:31 UTC via Ashby. Submit: Google Form linked in the Ashby email.
Timing: "Budget 6-8 hours ... better to submit as early as possible (<8 hrs after receiving)".

## Task
For each of the 100 apps in apps.json, capture:
- Category + one-line description
- Auth method(s): OAuth2, API key, Basic, token, other
- Self-serve vs gated (free/trial creds vs paid plan / admin approval / partnership / contact-sales)
- API surface: public REST / GraphQL, rough breadth, any existing MCP
- Buildability verdict: agent toolkit today? main blocker if not
- Evidence: docs URL behind each answer
- "and more.."

The actual point:
- Find patterns: cluster results (dominant auth, which categories self-serve vs gated, most common blocker, easy wins vs needs outreach). Insight over raw table.
- Do it with an agent/script/pipeline, not by hand. Using Composio's own SDK and MCP is "in the spirit of the role". Say what it does and where it needed a human.
- Verify accuracy: sample, cross-check against real docs by hand, report right/wrong. Real verification loops (agent, browser-use, others) + human checks; show accuracy moving from a lower first pass to a higher one. "Accuracy is what matters most."

## Deliverable
One self-explanatory HTML page / slideshow, understandable in ~2 minutes with no narration:
findings (skimmable table/matrix), patterns (headline, up top), the agent (what + where a human was needed),
proof (live link or runnable trigger), verification (sample accuracy, hits and misses honestly).
Show final output and the process; easy for both an agent and a human to consume.

## Constraints
- Use AI tooling freely, but understand and be able to explain everything; the interview will probe it.
- If the agent got things wrong or an app defeated you, say so on the page.
- No paid accounts needed; "gated behind payment or partnership" with evidence is a correct finding.

## Submit
1. Live link to the deployed HTML page / case study.
2. Link to the source repo with a short README on how to run the research agent.
