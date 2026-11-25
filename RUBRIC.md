# Field rubric

One definition per field, shared by the research agent, the critic agent and the
hand-checked gold sample. A field is "right" only if it matches this rubric.

## auth_methods (set)
What a third-party developer uses to authenticate against the app's public API.
- `oauth2`: an OAuth 2.0 authorization flow where a user grants a third-party app access.
- `api_key`: a static secret the user copies from a dashboard or creates in settings.
  Includes API keys, personal access tokens, private-app tokens, integration
  tokens and bot tokens that are not obtained through an OAuth flow. A key sent
  as the Basic-auth username still counts as `api_key`.
- `basic`: real username + password (or email + password) sent as HTTP Basic.
- `other`: anything else (JWT/service account, signed requests with key+secret
  pairs like HMAC, local tool with no auth, session cookies).
List every method the official docs offer. Graded as exact set match.

## access (single value)
Can a developer get working API credentials on their own today?
- `self_serve_free`: yes, on a free plan, free developer account or sandbox.
- `self_serve_trial`: yes, but only inside a time-limited free trial.
- `paid_plan`: API access needs a paid subscription or API add-on (no free/trial path to the API).
- `approval_required`: account is self-serve, but real API use needs the vendor to
  approve something (developer token review, app review, partner program,
  marketplace listing, admin-approved scopes).
- `contact_sales`: credentials only through sales, a partnership or an enterprise contract.
Graded exact, and also as the binary self-serve (free|trial) vs gated (rest).

## api_style (single value)
`rest`, `graphql`, `rest+graphql`, `sdk_or_cli_only` (no documented HTTP API,
only a library/CLI), `none` (no public API).

## api_breadth (single value)
`broad` (most of the product's objects with read+write), `moderate`
(core objects, some gaps), `narrow` (a few endpoints or read-only). Not graded:
it is a judgement call; shown for context.

## mcp (single value)
- `official`: an MCP server built or hosted by the vendor (vendor domain, vendor GitHub org, or vendor docs page).
- `community`: no official server, but a third-party one exists.
- `none`: neither found.
Graded exact.

## verdict (single value)
Could this be an agent toolkit today?
- `ready`: self-serve credentials + documented public API. Build now.
- `ready_with_review`: buildable now for testing, but production use needs an
  app review / verification / partner approval step.
- `blocked`: no usable path without a commercial relationship, a paid plan,
  or because there is no public API.
Graded exact.

## main_blocker (single value)
`none`, `paid_plan`, `app_review`, `partner_program`, `contact_sales`,
`no_public_api`, `not_a_saas` (local tool / library), `unclear_docs`.

## Evidence
Every graded field carries at least one `{url, quote}` where `quote` is copied
verbatim from that page. The evidence loop re-fetches the page and checks the quote is there.
