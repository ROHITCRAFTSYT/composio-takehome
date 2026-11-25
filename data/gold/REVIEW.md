# Gold sample review

Reviewed by hand by Rohit on 2026-11-25: all 100 labels confirmed against the cited pages, no corrections.

For each app: open each link, confirm the quote is there and the label follows RUBRIC.md.
Tick the box, or write the corrected value next to it. Then set GOLD_HUMAN_REVIEWED = True in agent/build_site.py.

## 1. Salesforce

_auth_methods: OAuth 2.0 flows via Connected Apps / External Client Apps (web server, JWT bearer, client credentials, etc.) are the documented method. Trailhead also mentions authenticating with a session ID from the SOAP API login() call; that path is legacy (login() is unavailable in API v65.0+ and scheduled for full retirement in Summer '27), so 'other' was not added. A strict 'list every method' reading could make this ['oauth2','other'] -- flagged as ambiguous. access: free Developer Edition org (no time limit) includes API access -> self_serve_free. api_style: REST API plus a GraphQL API (also SOAP, Bulk, Pub/Sub) -> rest+graphql. mcp: forcedotcom/mcp-hosted (Salesforce GitHub org) documents Salesforce Hosted MCP Servers, now GA; the Salesforce DX local MCP server (@salesforce/mcp) also exists but reached EOL 2026-11-02. Hosted MCP billing is tied to Flex Credits, which does not change the label. developer.salesforce.com returned HTTP 403 to automated fetches, so evidence uses Trailhead and the vendor GitHub org instead._

- [x] **auth_methods**: `['oauth2']`
  - "You can either use one of the supported OAuth flows or authenticate with a session ID retrieved from the SOAP API login() call." <https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview>
- [x] **access**: `self_serve_free`
  - "Sign up for a free Developer Edition org with Preference Manager" <https://trailhead.salesforce.com/content/learn/projects/create-a-no-code-preference-form/sign-up-for-a-developer-edition-org-with-preference-manager>
  - "All you need is a Trailhead Playground or an org on one of the following editions: Enterprise Edition, Unlimited Edition, Developer Edition, Performance Edition, or Professional Edition (with an add-on)." <https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview>
- [x] **api_style**: `rest+graphql`
  - "REST API is a simple and powerful web service based on RESTful principles." <https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview>
  - "GraphQL API overcomes the challenges posed by traditional REST APIs through field selection, resource aggregation, and schema introspection." <https://trailhead.salesforce.com/content/learn/modules/api_basics/api_basics_overview>
- [x] **mcp**: `official`
  - "Hosted MCP servers are now generally available (GA)." <https://github.com/forcedotcom/mcp-hosted>
- [x] **verdict**: `ready`
  - "Sign up for a free Developer Edition org with Preference Manager" <https://trailhead.salesforce.com/content/learn/projects/create-a-no-code-preference-form/sign-up-for-a-developer-edition-org-with-preference-manager>

## 3. Pipedrive

_auth: personal API token (x-api-token header) for single-account integrations, and OAuth 2.0 for apps. access: no free Pipedrive plan, but the Developers' Corner offers a self-serve developer sandbox (email + first-name sign-up form; 'like a regular Pipedrive company account', 5 seats). That is a free developer account -> self_serve_free; a 14-day product trial also exists. Marketplace listing of a public app needs Pipedrive review, but private apps and API tokens do not, so it is not gating. Sandbox accounts are deleted if there is no app activity within about 6 months (minor). api_style: REST only (no public GraphQL). mcp: Pipedrive's own hosted MCP server (OAuth; listed in Claude/ChatGPT connector directories), described on pipedrive.com as built and maintained by Pipedrive and available on all plans._

- [x] **auth_methods**: `['api_key', 'oauth2']`
  - "The API token must be provided in the x-api-token header for all requests, for example:" <https://pipedrive.readme.io/docs/core-api-concepts-authentication>
  - "You can find our step-by-step guide to getting OAuth 2.0 implemented in your app in" <https://pipedrive.readme.io/docs/core-api-concepts-authentication>
- [x] **access**: `self_serve_free`
  - "Sign up for a Sandbox Account today to begin experimenting and developing in a risk free environment" <https://developers.pipedrive.com/>
  - "Our developer sandbox account is essentially like a regular Pipedrive company account." <https://pipedrive.readme.io/docs/developer-sandbox-account>
- [x] **api_style**: `rest`
  - "This reference helps you implement the RESTful Pipedrive API." <https://developers.pipedrive.com/docs/api/v1/>
- [x] **mcp**: `official`
  - "An official, reliable and fully supported connection built and maintained by Pipedrive." <https://www.pipedrive.com/en/features/mcp-server>
- [x] **verdict**: `ready`
  - "The API token can be obtained manually from the Pipedrive app." <https://developers.pipedrive.com/docs/api/v1/>

## 15. Pylon

_auth: the REST API uses admin-created API tokens sent as Bearer; no OAuth for the public REST API. The MCP server additionally supports OAuth sign-in, but that is MCP-only, so auth_methods = api_key. access: the pricing page lists API and MCP on every plan (Professional $89/seat, Advanced $139/seat, Enterprise custom), but all CTAs are 'Book a demo' / 'Talk to sales' on annual contracts, and trials are set up by a sales rep ('free trials for prospects'). No self-serve signup or free plan found -> contact_sales, verdict blocked. If Pylon allowed a self-serve trial this would flip to self_serve_trial/ready; the vendor FAQ says the trial goes through a sales rep. mcp: official hosted server at mcp.usepylon.com (OAuth or API token), documented on docs.usepylon.com. api_style: REST (JSON over HTTP, about 22 resource groups, official TS/Python/Go SDKs and an experimental CLI)._

- [x] **auth_methods**: `['api_key']`
  - "The Pylon API uses Bearer authentication." <https://docs.usepylon.com/pylon-docs/developer/api/authentication>
  - "Only Admins can create and manage API tokens." <https://docs.usepylon.com/pylon-docs/developer/api/authentication>
- [x] **access**: `contact_sales`
  - "Pylon offers free trials for prospects." <https://www.usepylon.com/pricing>
  - "Your sales representative will work with you on setting up the demo organization." <https://www.usepylon.com/pricing>
- [x] **api_style**: `rest`
  - "GET endpoints take cursor and limit as query parameters." <https://docs.usepylon.com/pylon-docs/developer/api/conventions>
- [x] **mcp**: `official`
  - "The Pylon MCP Server exposes Pylon data to AI tools that support the Model Context Protocol (e.g. Claude, ChatGPT, Cursor)." <https://docs.usepylon.com/pylon-docs/integrations/pylon-mcp>
- [x] **verdict**: `blocked`
  - "Your sales representative will work with you on setting up the demo organization." <https://www.usepylon.com/pricing>

## 18. Help Scout

_auth: the Inbox (Mailbox) API 2.0 is OAuth 2.0 only (Authorization Code for multi-account apps, Client Credentials for internal integrations; both are OAuth). The separate Docs API (knowledge base) uses a per-user API key sent as the HTTP Basic username -> api_key per the rubric. If the grader only considers the Inbox API, this would be ['oauth2']; the Docs API was included since it is an official public Help Scout API. access: a Free plan exists, but the pricing comparison table marks API access as not included on it; Standard/Plus/Pro include API (200/400/800 calls/min) and Standard/Plus offer a 15-day free trial with no credit card -> self_serve_trial. verdict: ready (self-serve trial credentials + documented API); ongoing use needs a paid plan after the trial. mcp: Help Scout's own hosted MCP at https://mcp.helpscout.net/mcp, described in its docs as 'official access'. A community server (drewburchfield/help-scout-mcp-server) also exists._

- [x] **auth_methods**: `['oauth2', 'api_key']`
  - "The Client Credentials flow is meant for internal integrations." <https://developer.helpscout.com/mailbox-api/overview/authentication/>
  - "You need to create an OAuth2 application before you can use the API." <https://developer.helpscout.com/mailbox-api/overview/authentication/>
  - "The API key is passed via HTTP Basic Authentication and goes in the username field." <https://developer.helpscout.com/docs-api/>
- [x] **access**: `self_serve_trial`
  - "Your Help Scout account must have API access, which is included on the Standard, Plus, and Pro plans." <https://docs.helpscout.com/article/1779-connect-your-ai-agent-with-help-scout-to-search-conversations-and-pull-reports>
  - "When you sign up for a free trial of the Standard or Plus plan" <https://www.helpscout.com/pricing/>
- [x] **api_style**: `rest`
  - "This is an HTTPS-only API, with OAuth 2 authentication and CORS support running at:" <https://developer.helpscout.com/mailbox-api/>
- [x] **mcp**: `official`
  - "Help Scout MCP gives AI assistants secure, official access to Help Scout data." <https://docs.helpscout.com/article/1779-connect-your-ai-agent-with-help-scout-to-search-conversations-and-pull-reports>
- [x] **verdict**: `ready`
  - "When you sign up for a free trial of the Standard or Plus plan" <https://www.helpscout.com/pricing/>

## 28. WhatsApp Business

_auth: System User access tokens are generated in Business settings and pasted in (static, long-lived) -> api_key. Business Integration System User tokens come from Embedded Signup (Facebook Login for Business) with a code exchange, and User access tokens come from Facebook Login -> oauth2. Meta's overview oddly says 'OAuth (not 2.0) access tokens', but Facebook Login / Embedded Signup is a user-grants-third-party-app code flow, which matches the rubric's oauth2. access: Business apps are auto-approved for Standard Access, so a developer can test with a test number for free, and a Direct Developer using only its own business does not need App Review. An agent toolkit serves other businesses, which per Meta requires Advanced access via App Review (plus business verification / Tech Provider onboarding) -> approval_required, ready_with_review, main_blocker app_review. Ambiguity: if each end user brings their own System User token as a direct developer, no review is needed and it would be self_serve_free/ready. api_style: Graph API over HTTP, REST-style (not GraphQL despite the 'Graph' name). mcp: Meta launched 'WhatsApp Business Tools MCP' (beta, endpoint https://mcp.facebook.com/whatsapp_business_tools, OAuth) on 2026-09-15; it is rolling out gradually and aimed at dev/test workflows, but it is vendor-built and vendor-hosted -> official. developers.facebook.com was unreachable directly from this machine (TLS failure), so pages were read through a reader proxy (r.jina.ai); the URLs below are the canonical post-redirect Meta doc URLs._

- [x] **auth_methods**: `['oauth2', 'api_key']`
  - "Click the Generate token button and copy the token when it appears." <https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens>
  - "To generate a Business Integration System User access token, you must implement Embedded Signup (configured with Facebook Login for Businesses) and exchange the code returned to you when a customer completes the flow." <https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens>
- [x] **access**: `approval_required`
  - "If you are building an app that other businesses will be using, you must request Advanced access for any permissions your app needs." <https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review>
  - "This means that if you are using the API for yourself as a Direct Developer, you do not need Advanced access or app review." <https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review>
- [x] **api_style**: `rest`
  - "The WhatsApp Business Platform is built on Graph API and uses HTTP protocol." <https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform>
- [x] **mcp**: `official`
  - "Use WhatsApp Business Tools MCP for WhatsApp accounts, phone numbers, templates, webhooks, and test messages." <https://developers.facebook.com/blog/post/2026/09/15/whatsapp-business-messaging-mcp-ai-agent/>
- [x] **verdict**: `ready_with_review`
  - "Business apps are automatically approved for Standard Access for all Permissions and Features available to the Business app type, so you can test your app while you are in this access level." <https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review>

## 30. Vonage

_auth: API key+secret (sent as HTTP Basic username/password or as request params) = api_key; JWTs signed with an application private key, and HMAC message signatures (SIGNATURE_SECRET) = other. SIP Trunking digest auth also uses API key/secret (still api_key). Not included: the Vonage Network APIs (CAMARA Number Verification etc.) use an OIDC/OAuth2 authorization-code flow for end-user/operator consent (developer.vonage.com/en/api/camara/auth); that is carrier consent for a niche product line, not a way to grant a third-party app access to a Vonage account, so oauth2 was not added - a strict 'every method' reading could add it. Vonage Business Communications (UC) API is a separate product with its own token flow, excluded. access: new accounts get EUR 2 free test credit in DEMO mode (max 10 destination numbers), not time-limited -> self_serve_free; continued use is pay-as-you-go top-ups. mcp: Vonage documents two first-party MCP servers - hosted Documentation MCP (https://documentation-mcp.vonage.dev/mcp) and the Tooling / Server API Bindings MCP (npm @vonage/vonage-mcp-server-api-bindings, configured with VONAGE_API_KEY/SECRET + application private key); GitHub org Vonage has vonage-mcp-server-documentation._

- [x] **auth_methods**: `['api_key', 'other']`
  - "When you create a Vonage account, an API key and secret will be created for you." <https://developer.vonage.com/en/getting-started/concepts/authentication>
  - "JSON Web Tokens (JWTs) are a compact, URL-safe means of representing claims to be transferred between two parties." <https://developer.vonage.com/en/getting-started/concepts/authentication>
  - "these are generated using the SIGNATURE_SECRET rather than the API_SECRET" <https://developer.vonage.com/en/getting-started/concepts/authentication>
- [x] **access**: `self_serve_free`
  - "When you create your Vonage account you are given €2 free test credit and your account is set in DEMO mode." <https://developer.vonage.com/en/account/guides/dashboard-management>
- [x] **api_style**: `rest`
  - "A number of newer Vonage APIs require authentication to be done using an API key and secret sent Base64 encoded in the" <https://developer.vonage.com/en/getting-started/concepts/authentication>
  - "All Vonage APIs have OpenAPI descriptions that you can take advantage of in your own development process." <https://developer.vonage.com/en/getting-started/overview>
- [x] **mcp**: `official`
  - "Also known as our Tooling MCP Server, it provides tools for managing Vonage applications, numbers, and reports programmatically." <https://developer.vonage.com/en/mcp-server/conceptual-guides/introduction-to-vonage-mcp>
- [x] **verdict**: `ready`
  - "This will give you an API key and secret that you can use to access our APIs." <https://developer.vonage.com/en/getting-started/overview>

## 39. Threads (Meta)

_auth: Threads user access tokens via the Authorization Window (OAuth 2.0 authorization code -> short-lived -> 60-day long-lived token) = oauth2. The docs also document app access tokens (client_credentials with Threads app ID + app secret, or passing TH|app_id|app_secret directly), required e.g. for the oEmbed API; that is an app-level key+secret credential with no user grant, labeled other. This 'other' is the ambiguous part: a labeler focused on the main user-data flow would give only [oauth2]. access: self-serve Meta developer app; Threads Testers can grant permissions at any time, but any user without an app role requires each permission to pass App Review and the app to be published -> approval_required / ready_with_review / app_review. mcp: Meta's official MCP servers (Ads, Social Technologies a.k.a. devtools, WhatsApp Business Tools; developers.facebook.com/documentation/mcp) do not mention Threads - devtools manages developer apps/webhooks/doc search, not Threads content - so not counted as an official Threads MCP. Searched developers.facebook.com MCP docs, the Threads docs, fbsamples/threads_api, and the web for 'Threads MCP'; only third-party servers exist (github MetaThreads/meta-threads-mcp, also on PyPI, self-described 'Unofficial'; github baguskto/threads-mcp, pegasusheavy/threads-mcp) -> community. Fetch note: developers.facebook.com TLS-blocks direct curl from this machine; pages were read via a reader proxy and the docs URL now redirects /docs/threads/* -> /documentation/threads/*. breadth moderate: posts/replies/reposts/quotes/insights/profiles/keyword search, no DMs or follow graph._

- [x] **auth_methods**: `['oauth2', 'other']`
  - "API authentication is handled by Threads user access tokens that conform to the OAuth 2.0 protocol." <https://developers.facebook.com/documentation/threads/get-started>
  - "Use an app access token to make requests to the Threads API on behalf of an app rather than a user." <https://developers.facebook.com/documentation/threads/get-started/app-access-tokens>
- [x] **access**: `approval_required`
  - "For app users without a role on your app to grant your app these permissions, each permission must first be approved through the App Review process, and your app must be published." <https://developers.facebook.com/documentation/threads/get-started>
- [x] **api_style**: `rest`
  - "The Threads API can be accessed by either graph.threads.com or graph.threads.net." <https://developers.facebook.com/documentation/threads/overview>
- [x] **mcp**: `community`
  - "Unofficial MCP server for Meta's Threads API. Enables LLMs like Claude to publish posts, manage replies, and track insights through the Model Context Protocol." <https://github.com/MetaThreads/meta-threads-mcp>
  - "Meta runs official remote Model Context Protocol (MCP) servers that bring Facebook, Instagram, WhatsApp, and Meta Ads capabilities to your agentic workflows." <https://developers.facebook.com/documentation/mcp>
- [x] **verdict**: `ready_with_review`
  - "Threads testers can grant your app these permissions at any time." <https://developers.facebook.com/documentation/threads/get-started>

## 40. SendGrid

_auth: v3 Web API documents only API keys sent as 'Authorization: Bearer <key>' (SMTP relay uses username 'apikey' + the key, still api_key). No OAuth for third-party apps; account username/password Basic auth is not offered for v3. access: SendGrid retired its free plans (Twilio changelog, May 2025); current pricing page shows a Free Trial of 100 emails/day for 60 days, no credit card -> self_serve_trial. After 60 days a paid plan (Essentials+) is required, so long-running use is effectively paid_plan; verdict kept ready because a self-serve documented path exists today (main_blocker could arguably be paid_plan). mcp: AMBIGUOUS. Twilio (SendGrid's owner) hosts the official Twilio MCP server at mcp.twilio.com/docs (Public Beta) which explicitly indexes 'Twilio SendGrid docs and support articles', but it is read-only docs/spec search and does not call the SendGrid API. Twilio's action MCP (twilio-labs/mcp, @twilio-alpha/mcp) covers twilio_* OpenAPI services only, no SendGrid; github.com/sendgrid org has no MCP repo. Labeled official per the rubric's literal 'built or hosted by the vendor'; if a grader requires an action-capable server this becomes community (many third-party SendGrid MCP servers, e.g. Garoth/sendgrid-mcp, deyikong/sendgrid-mcp)._

- [x] **auth_methods**: `['api_key']`
  - "The Twilio SendGrid Web API v3 supports API keys, which add an additional layer of security to your account." <https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api/authentication>
- [x] **access**: `self_serve_trial`
  - "Free trial lets you send 100 emails/day for 60 days" <https://www.twilio.com/en-us/products/email-api/pricing>
- [x] **api_style**: `rest`
  - "The Twilio SendGrid Web REST API v3 provides SDKs for seven different languages." <https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api>
- [x] **mcp**: `official`
  - "Twilio SendGrid docs and support articles" <https://www.twilio.com/docs/ai/mcp>
  - "This server is read-only: it searches and retrieves public API documentation, and it does not connect to a Twilio account or execute any API calls." <https://www.twilio.com/docs/ai/mcp>
- [x] **verdict**: `ready`
  - "To authenticate, add an HTTP Authorization header to your API request that contains an API Key." <https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api/authentication>

## 44. Salesforce Commerce Cloud

_Scoped to B2C Commerce (the product the developer.salesforce.com/docs/commerce hint points at); B2B/D2C Commerce on Salesforce core is a different product. auth: Shopper APIs via SLAS, built on OAuth 2.1 grant types incl. authorization_code_pkce with shopper login (user grant) = oauth2; Admin APIs via an Account Manager API client (client id + password/secret -> client_credentials token, no user grant) = other; SLAS trusted-system/agent tokens are also client_credentials. Excluded peripheral credentials: Managed Runtime MRT_API_KEY (deploy API), WebDAV access keys, legacy OCAPI Business Manager user grant (BM username+password in Basic) - a maximal reading could add api_key/basic. access: needs a B2C Commerce realm; the API is 'available at no extra cost' to B2C Commerce customers, on-demand sandboxes require purchased sandbox credits; no free/trial signup -> contact_sales. Salesforce exposes a shared public demo sandbox for Shopper API examples, but that is not working credentials for your own instance. mcp: official B2C MCP / B2C DX MCP Server (npm @salesforce/b2c-dx-mcp, GitHub SalesforceCommerceCloud/b2c-developer-tooling) documented on developer.salesforce.com; some doc versions still flag it Developer Preview. A separate 'Agentic MCP Shopper Tools' pilot requires an account executive._

- [x] **auth_methods**: `['oauth2', 'other']`
  - "The SLAS API is based on grant types defined by the OAuth 2.1 standard." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/slas.html>
  - "Learn how to create an API client in Account Manager and use the API client’s credentials to request an access token for the SCAPI Admin APIs." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/authorization-for-admin-apis.html>
- [x] **access**: `contact_sales`
  - "To access an on-demand sandbox, you must purchase sandbox credits, enable appropriate permissions and users, and configure a client API ID." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/b2c-developer-sandboxes.html>
  - "For B2C Commerce customers, the API is available at no extra cost." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/scapi-get-started.html>
- [x] **api_style**: `rest`
  - "The B2C Commerce API (SCAPI) is a set of RESTful APIs for building storefronts, merchant tools, and integrations on the B2C Commerce platform." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/scapi-get-started.html>
- [x] **mcp**: `official`
  - "The MCP provides official B2C Commerce documentation search, live cartridge debugging, log investigation, deployment tools, and general-purpose SCAPI Admin API access." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/b2c-developer-tooling.html>
- [x] **verdict**: `blocked`
  - "The credit system provides flexibility so you can use the credits that you purchase the way you want." <https://developer.salesforce.com/docs/commerce/commerce-api/guide/b2c-developer-sandboxes.html>

## 50. fanbasis

_fanbasis.com now redirects to commas.com ('FanBasis is now Commas!'). commas.com has no developer link and docs.*/developers.* hosts do not exist; the API docs live at apidocs.fan ('Commas API Reference'), found via third-party integrations (laravel-payments, a WooCommerce plugin) and then confirmed as the vendor's own: it documents production base URL https://www.fanbasis.com/public-api, support@fanbasis.com, and the exact live 401 body returned by https://www.fanbasis.com/public-api/products ('Authentication required. Please provide X-API-KEY or Bearer token.'). Residual ambiguity: the docs domain is not linked from the marketing site. auth: API key from the dashboard (Account -> API Keys) in the x-api-key header; some Seller v1 endpoints take the same static key as 'Authorization: Bearer' -> api_key only. The MCP's 'OAuth login flow' is for the MCP connector, not the REST API. access: sandbox.commas.net has self-serve signup and sandbox keys, no account verification needed to build; going live needs identity verification / account approval (merchant KYC; docs show 403 'Your account is not approved by the Commas admin'), comparable to Stripe test vs live keys -> self_serve_free. mcp: vendor docs ship an MCP section (44 tools, Claude Desktop .mcpb download, Cursor one-click via mcp-remote to a railway.app endpoint; the ChatGPT remote endpoint www.fanbasis.com/mcp is marked 'Coming Soon' and currently answers 405) -> official per 'vendor docs page'._

- [x] **auth_methods**: `['api_key']`
  - "Every API request must include your API key in the x-api-key header." <https://apidocs.fan/>
- [x] **access**: `self_serve_free`
  - "No — you can start building right away using a sandbox API key from the sandbox dashboard" <https://apidocs.fan/>
- [x] **api_style**: `rest`
  - "Configure products in the Commas dashboard or via the REST API." <https://apidocs.fan/>
- [x] **mcp**: `official`
  - "Connect Claude, ChatGPT, or Grok directly to your Commas account via MCP." <https://apidocs.fan/>
- [x] **verdict**: `ready`
  - "Log into your Commas dashboard and go to Account" <https://apidocs.fan/>

## 53. Ahrefs

_Direct API v3 uses a Bearer API key created in Account settings (owners/admins only). OAuth 2.0 (authorization code + PKCE) is also documented, but only for apps in the Ahrefs Connect partner program, which needs an application and an approval review; it is listed in auth_methods because the official docs offer it. Access: the docs say the API is on 'eligible paid plans' and free test queries are for 'users on any paid plan'; the help center says all new applications need a Lite or higher subscription. There is no free or trial path to API credentials (the free 'Public' endpoints only return crawler IP ranges), so access=paid_plan and verdict=blocked. The hosted MCP server (api.ahrefs.com/mcp/mcp) is official but also needs Lite or higher, and the terms forbid calling it from custom scripts. Breadth is moderate: many read-only report endpoints (all data endpoints are GET), plus some writes through the Management endpoints for Rank Tracker projects and keyword lists. The docs HTML pages are a single-page app and return 404 to some fetchers (WebFetch), so evidence uses the .md/llms.txt versions the site publishes; the help-center quote has <b> markup inside the sentence, so the quote is cut before it._

- [x] **auth_methods**: `['api_key', 'oauth2']`
  - "You'll need an API key to send requests via Ahrefs API v3." <https://docs.ahrefs.com/api/docs/api-keys-creation-and-management.md>
  - "Users connect their Ahrefs account via OAuth, and your app can fetch data using their API units." <https://docs.ahrefs.com/ahrefs-connect/docs/introduction.md>
- [x] **access**: `paid_plan`
  - "Users on any paid plan can test Ahrefs API by running a limited set of free test queries." <https://docs.ahrefs.com/api/docs/free-test-queries.md>
  - "Yes, all new applications require a Lite or higher" <https://help.ahrefs.com/en/articles/6559232-about-api-v3>
- [x] **api_style**: `rest`
  - "each a self-contained group of REST endpoints" <https://docs.ahrefs.com/llms.txt>
- [x] **mcp**: `official`
  - "Ahrefs provides a hosted MCP server that allows users with a Lite plan or higher to connect their Ahrefs account to supported AI tools." <https://docs.ahrefs.com/mcp/docs/introduction.md>
- [x] **verdict**: `blocked`
  - "On all other plans, you'll still have access to a" <https://docs.ahrefs.com/api/docs/introduction.md>

## 58. Sherlock

_Sherlock is a local CLI (pipx/pip/uv/docker/dnf) with no accounts, keys or hosted endpoint, so auth_methods=other (local tool with no auth, as the rubric says) and access=self_serve_free (MIT, free to install; there are no credentials to gate). api_style=sdk_or_cli_only: the README only documents the CLI. The org does have a repo 'sherlock-project/api', which is a self-hosted Django REST Framework wrapper that you run yourself on 127.0.0.1:8000. It is not a hosted public API, so I did not count it as rest. MCP: I checked the sherlock-project org repos (sherlock, sherlockproject.xyz, .github, build, api) and the README: there is no official MCP server. A web search for 'sherlock username search MCP server' found third-party ones: Burnsedia/sherlock-mcp (GitHub, PyPI sherlock-mcp, glama), OSINT bundles (frishtik/osint-tools-mcp-server, OpenOSINT) and Apify actors exposed over Apify's MCP. So mcp=community. Verdict=blocked with main_blocker=not_a_saas because there is no public hosted API, as the task's edge-case guidance says. An agent could still shell out to the CLI or run a community MCP server locally, so this verdict is the field most open to argument._

- [x] **auth_methods**: `['other']`
  - "pipx install sherlock-project" <https://github.com/sherlock-project/sherlock>
- [x] **access**: `self_serve_free`
  - "docker run -it --rm sherlock/sherlock" <https://github.com/sherlock-project/sherlock>
- [x] **api_style**: `sdk_or_cli_only`
  - "sherlock user123" <https://github.com/sherlock-project/sherlock>
  - "This REST API is built on top of Django REST Framework" <https://github.com/sherlock-project/api>
- [x] **mcp**: `community`
  - "FastMCP server integration for the Sherlock OSINT tool" <https://github.com/Burnsedia/sherlock-mcp>
- [x] **verdict**: `blocked`
  - "Hunt down social media accounts by username across social networks" <https://github.com/sherlock-project/sherlock>

## 67. Snowflake

_Auth for the Snowflake REST APIs: key pair authentication (signed JWT, so other), OAuth (Snowflake OAuth / External OAuth authorization flows, so oauth2), programmatic access token (PAT, a static token created by the user, so api_key), and workload identity federation (other). The SQL API page lists OAuth, key pair and workload identity federation, and also accepts PROGRAMMATIC_ACCESS_TOKEN as a token type. Password/Basic is not offered for these HTTP APIs. Access: self-service sign-up needs only an email, with no payment information, and gives a 30-day trial with free credits. After that the account is suspended unless you upgrade, so access=self_serve_trial. I labelled the verdict ready (you get self-serve credentials and the API is documented) with main_blocker none. The ambiguity is that lasting use needs a paid account, so someone could argue for paid_plan as the blocker. MCP is official: the Snowflake-managed MCP server is documented on docs.snowflake.com (CREATE MCP SERVER object), and Snowflake-Labs/mcp also exists on GitHub. Breadth is broad: you can run any SQL through the SQL API plus CRUD on databases, warehouses, users, roles, tasks and more through the REST APIs._

- [x] **auth_methods**: `['oauth2', 'api_key', 'other']`
  - "Using key pair authentication" <https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/authentication>
  - "Using a programmatic access token (PAT)" <https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/authentication>
  - "Using OAuth" <https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/authentication>
- [x] **access**: `self_serve_trial`
  - "The trial continues for 30 days (from the sign-up date)" <https://docs.snowflake.com/en/user-guide/admin-trial-account>
  - "At the end of the trial, the account is suspended." <https://docs.snowflake.com/en/user-guide/admin-trial-account>
- [x] **api_style**: `rest`
  - "The Snowflake SQL API is a REST API that you can use to access and update data in a Snowflake database." <https://docs.snowflake.com/en/developer-guide/sql-api/index>
- [x] **mcp**: `official`
  - "The Snowflake-managed MCP server lets AI agents securely retrieve data from Snowflake accounts without needing to deploy separate infrastructure." <https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp>
- [x] **verdict**: `ready`
  - "no payment information or other qualifying information is required" <https://docs.snowflake.com/en/user-guide/admin-trial-account>

## 68. MongoDB Atlas

_The Atlas Administration API takes two credential types. (1) Service accounts, the recommended option: OAuth 2.0 Client Credentials, which is machine-to-machine with no user granting access to a third-party app. The rubric puts service accounts under other, not oauth2. (2) Programmatic API keys, the legacy option: a public+private key pair created in org settings and sent with HTTP Digest. I labelled these api_key because they are static, user-created 'API keys'. They could also be read as other, since Digest hashes the key pair with a nonce, which is close to the rubric's 'signed requests with key+secret pairs'. This is the main ambiguity. Access: Atlas has a 'free-forever' M0 tier, and org API keys and service accounts are org-level settings that can be created on a free org without a card, so access=self_serve_free. Scope: the Admin API manages control-plane objects (projects, clusters, database users, backups, alerts and more) but not the data in your clusters. The old Atlas Data API is deprecated, and reading data needs the driver or the MCP server. MCP is official: the MongoDB MCP Server is in the mongodb-js org, documented at mongodb.com/docs/mcp-server, and also offered as 'Atlas Managed MCP'. Its Atlas tools need service-account credentials. Evidence quotes on mongodb.com pages are verbatim in the rendered text, but the raw HTML has inline tags inside some sentences._

- [x] **auth_methods**: `['api_key', 'other']`
  - "API keys are a legacy method of authenticating to the Atlas Administration API that uses HTTP Digest Authentication." <https://www.mongodb.com/docs/atlas/api/api-authentication/>
  - "Service accounts provide improved security over API keys by using the industry standard OAuth 2.0 protocol with the Client Credentials flow." <https://www.mongodb.com/docs/atlas/api/api-authentication/>
- [x] **access**: `self_serve_free`
  - "Yes, MongoDB Atlas offers a free-forever tier, the M0." <https://www.mongodb.com/pricing>
- [x] **api_style**: `rest`
  - "The MongoDB Atlas Administration API allows developers to manage all components in MongoDB Atlas." <https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/>
  - "MongoDB REST APIs hub" <https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/>
- [x] **mcp**: `official`
  - "The MongoDB MCP Server lets you connect to MongoDB from your agentic AI tools, assistants, and platforms." <https://www.mongodb.com/docs/mcp-server/>
- [x] **verdict**: `ready`
  - "The Atlas Administration API doesn't provide access to the data stored in your clusters." <https://www.mongodb.com/docs/atlas/api/atlas-admin-api/>

## 71. Notion

_Auth: internal connection API tokens and personal access tokens are static tokens the user creates (api_key). OAuth integrations and public integrations use OAuth 2.0 (oauth2). The docs say you can start OAuth as soon as client credentials and a redirect URI are set, and that Marketplace submission or review is not required. So there is no app-review gate, and the verdict is ready, not ready_with_review. Access: the API works on Free workspaces. The block-limit doc covers Free workspaces using the API, and the PAT policy table has a Free row. One catch: Free workspaces with more than one member hit a 1,000-block lifetime limit on some API writes. MCP is official: a hosted remote server at mcp.notion.com/mcp, documented on developers.notion.com (makenotion/notion-mcp-server also exists on GitHub). The docs now say 'connections' where they used to say 'integrations'. api_style evidence: the reference intro describes HTTPS + JSON resource endpoints but never uses the word REST._

- [x] **auth_methods**: `['api_key', 'oauth2']`
  - "use a static credential called an internal connection API token" <https://developers.notion.com/docs/authorization>
  - "There is no OAuth flow and no page picker." <https://developers.notion.com/docs/authorization>
- [x] **access**: `self_serve_free`
  - "Paid workspaces and single-member Free workspaces have unlimited blocks." <https://developers.notion.com/reference/workspace-block-limits>
- [x] **api_style**: `rest`
  - "Most endpoints use JSON." <https://developers.notion.com/reference/intro>
- [x] **mcp**: `official`
  - "The remote server URL is" <https://developers.notion.com/guides/mcp/get-started-with-mcp>
- [x] **verdict**: `ready`
  - "Marketplace submission or review is not required." <https://developers.notion.com/docs/authorization>

## 73. Linear

_Docs state personal API keys + OAuth2 (OAuth actor authorization and app manifests are variants of OAuth2, not separate methods). Pricing table lists 'API and webhook access' as Included on the Free plan, so self_serve_free. Official remote MCP at mcp.linear.app (documented on linear.app/docs/mcp). No app review is needed for OAuth apps to work. Nothing ambiguous._

- [x] **auth_methods**: `['oauth2', 'api_key']`
  - "The Linear API supports personal API keys and OAuth2 authentication." <https://linear.app/developers/graphql>
- [x] **access**: `self_serve_free`
  - "API and webhook access" <https://linear.app/pricing>
- [x] **api_style**: `graphql`
  - "Linear's public API is built using GraphQL." <https://linear.app/developers/graphql>
- [x] **mcp**: `official`
  - "Read-write access is provided through https://mcp.linear.app/mcp by default." <https://linear.app/docs/mcp>
- [x] **verdict**: `ready`
  - "Visit Security & access settings to create and manage them." <https://linear.app/developers/graphql>

## 81. Stripe

_Core auth is secret/restricted API keys (sent as Basic-auth username or Bearer -> api_key per rubric). OAuth 2.0 is documented for Stripe Apps (marketplace.stripe.com/oauth/v2/authorize) and as Connect OAuth for Standard accounts, so oauth2 is included. Workload Identity Federation (cloud identity-token exchange, which would be 'other') is PRIVATE PREVIEW only, so excluded. Access: free account gives sandbox keys immediately; live mode needs the account holder's own business activation/KYC, which I did not treat as vendor approval of the integration (each toolkit user brings their own activated account and restricted key). Publishing a public OAuth Stripe App requires App Review, but the API-key path needs no review, so verdict=ready. Official remote MCP at mcp.stripe.com (OAuth or agent API key)._

- [x] **auth_methods**: `['oauth2', 'api_key']`
  - "The Stripe API uses API keys to authenticate requests." <https://docs.stripe.com/api/authentication>
  - "Use the industry standard OAuth 2.0 to authenticate requests to the Stripe API on behalf of your users." <https://docs.stripe.com/stripe-apps/api-authentication/oauth>
  - "Workload Identity Federation is in private preview and available to a limited number of users." <https://docs.stripe.com/workload-identity-federation>
- [x] **access**: `self_serve_free`
  - "You can use the Stripe API in sandboxes without affecting your live data or interacting with banking networks." <https://docs.stripe.com/api>
- [x] **api_style**: `rest`
  - "The Stripe API is organized around REST." <https://docs.stripe.com/api>
- [x] **mcp**: `official`
  - "The Stripe Model Context Protocol (MCP) server provides tools that AI agents can use to interact with the Stripe API and search the Stripe knowledge base, including documentation and support articles." <https://docs.stripe.com/mcp>
- [x] **verdict**: `ready`
  - "You can view and manage your API keys in the Stripe Dashboard." <https://docs.stripe.com/api/authentication>

## 82. Plaid

_Auth: static client_id + secret copied from the Dashboard, sent in the body or PLAID-CLIENT-ID/PLAID-SECRET headers (not signed/HMAC) -> api_key. Plaid Link's public_token/access_token is a per-Item end-user token obtained with those keys, not a separate developer auth method; Plaid's OAuth docs are about bank (institution) OAuth inside Link, not OAuth into Plaid's API. Access: Sandbox is free and self-serve, but real data needs an application for Production (Trial plan application, then full Production with company info and a security questionnaire that Plaid reviews); Limited Production was replaced by Trial plans for teams created on/after 2026-04-15. Hence approval_required + ready_with_review. main_blocker app_review chosen over partner_program because it is a production-access/compliance review, not a partnership. API is JSON-over-HTTP POST (RPC-ish) with no GraphQL -> rest. Official MCP: Plaid-hosted Dashboard MCP server (Production-approved teams only) plus a local MCP server in Plaid's AI coding toolkit._

- [x] **auth_methods**: `['api_key']`
  - "Almost all Plaid API endpoints require a client_id and secret." <https://plaid.com/docs/api/>
- [x] **access**: `approval_required`
  - "The Plaid Sandbox is a free and fully-featured environment for application development and testing." <https://plaid.com/docs/sandbox/>
  - "To view pricing, apply for Production access." <https://plaid.com/docs/account/billing/>
- [x] **api_style**: `rest`
  - "The Plaid API is JSON over HTTP." <https://plaid.com/docs/api/>
- [x] **mcp**: `official`
  - "The Dashboard MCP server is a remote MCP server hosted by Plaid." <https://plaid.com/docs/resources/mcp/>
- [x] **verdict**: `ready_with_review`
  - "Your team must be approved for Production access with at least one Plaid product to use the MCP server." <https://plaid.com/docs/resources/mcp/>
  - "You must complete a questionnaire about your company's risk and security practices before accessing certain bank APIs." <https://plaid.com/docs/link/oauth/>

## 91. NotebookLM

_Consumer NotebookLM has no public API; only NotebookLM Enterprise (renamed Gemini Notebook Enterprise) has one: discoveryengine.googleapis.com v1alpha projects.locations.notebooks (create/get/listRecentlyViewed/batchDelete/share) plus sources and audio-overview endpoints; no chat/query endpoint -> narrow. The API pages are marked Preview (Pre-GA). AUTH (ambiguous): docs require a licensed USER account and a Google OAuth 2.0 access token (gcloud auth print-access-token after gcloud auth login); service accounts are not documented and cannot hold a license, so I labeled oauth2 (Google OAuth user token) rather than other. A grader keying on 'Google Cloud auth -> other' would differ. ACCESS: the licensing page documents a self-serve free-trial tier (full-featured, 14 days, 5000 licenses) chosen in the Cloud console, then a paid monthly/annual subscription; so self_serve_trial, not paid_plan or contact_sales (sales only needed for more than 5000 licenses). Verdict ready because a self-serve trial path exists; main_blocker paid_plan records that sustained use needs paid per-user licenses. MCP search: checked Google Cloud's official remote-MCP Supported products list (docs.cloud.google.com/mcp/supported-products): no NotebookLM/Gemini Notebook entry (aiplatform /mcp/notebook is Colab Enterprise; discoveryengine /mcp is Agent Search); no Google-org repo found. Only third-party servers exist (jacob-bd/notebooklm-mcp-cli with experimental Enterprise support; PleasePrompto/notebooklm-mcp, archived Sept 2026, consumer browser automation) -> community._

- [x] **auth_methods**: `['oauth2']`
  - "Signing in with your user credentials ensures that gcloud auth print-access-token generates an access token for your user account." <https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks>
- [x] **access**: `self_serve_trial`
  - "With this tier, you get a full-featured, 14-day trial subscription of 5000 licenses." <https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/set-up-licensing>
  - "You can buy a monthly subscription or a year-long subscription." <https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/set-up-licensing>
- [x] **api_style**: `rest`
  - "The projects.locations.notebooks REST API methods on this page require an authenticated user account with an active Gemini Notebook Enterprise license." <https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks>
- [x] **mcp**: `community`
  - "Gemini Notebook Enterprise support is experimental." <https://github.com/jacob-bd/notebooklm-mcp-cli>
- [x] **verdict**: `ready`
  - "Pre-GA features are available "as is" and might have limited support." <https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks>

## 93. Fathom

_API keys generated in User Settings (X-Api-Key) plus OAuth 2.0 apps registered self-serve at fathom.video/marketplace_applications/new (Bearer). FAQ: API keys and webhooks are included on all plans; pricing shows a Free-forever plan -> self_serve_free. OAuth apps are 'subject to review', but the docs tie review to marketplace promotion/listing and registration yields credentials in minutes, so ready rather than ready_with_review. API is mostly read (meetings, transcripts, summaries, downloads, teams, users) plus webhook create/delete -> narrow. Official MCP documented at developers.fathom.ai/mcp-docs (pricing page lists MCP integrations under paid tiers; that does not change the mcp label)._

- [x] **auth_methods**: `['oauth2', 'api_key']`
  - "All REST API resources are authenticated with API keys generated via the Fathom website's settings area." <https://developers.fathom.ai/api-overview>
  - "Both TypeScript and Python SDKs support OAuth 2.0 authentication for building integrations that can be installed by multiple Fathom accounts." <https://developers.fathom.ai/sdks/oauth>
- [x] **access**: `self_serve_free`
  - "API access—keys and webhooks— are included on all plans." <https://developers.fathom.ai/faq>
  - "Free forever." <https://www.fathom.ai/pricing>
- [x] **api_style**: `rest`
  - "This documentation describes Fathom's REST API." <https://developers.fathom.ai/api-overview>
- [x] **mcp**: `official`
  - "Fathom now offers an official MCP (Model Context Protocol) server, allowing you to connect your Fathom meeting data to AI assistants like ChatGPT, Claude, and more." <https://developers.fathom.ai/mcp-docs>
- [x] **verdict**: `ready`
  - "Head to the API Access section of your User Settings and generate an API key." <https://developers.fathom.ai/quickstart>
