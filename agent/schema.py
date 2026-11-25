"""Record schema shared by every stage. Mirrors RUBRIC.md."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

AuthMethod = Literal["oauth2", "api_key", "basic", "other"]
Access = Literal["self_serve_free", "self_serve_trial", "paid_plan", "approval_required", "contact_sales"]
ApiStyle = Literal["rest", "graphql", "rest+graphql", "sdk_or_cli_only", "none"]
Breadth = Literal["broad", "moderate", "narrow"]
Mcp = Literal["official", "community", "none"]
Verdict = Literal["ready", "ready_with_review", "blocked"]
Blocker = Literal[
    "none", "paid_plan", "app_review", "partner_program", "contact_sales",
    "no_public_api", "not_a_saas", "unclear_docs",
]
Confidence = Literal["high", "medium", "low"]

GRADED_FIELDS = ("auth_methods", "access", "api_style", "mcp", "verdict")
SELF_SERVE = {"self_serve_free", "self_serve_trial"}


class Evidence(BaseModel):
    field: str = Field(description="Which field this supports, e.g. 'access'")
    url: str
    quote: str = Field(description="Short sentence copied verbatim from the page")


class AppRecord(BaseModel):
    n: int
    app: str
    category: str
    one_liner: str = Field(description="What the product does, one line")
    auth_methods: list[AuthMethod]
    auth_notes: str = ""
    access: Access
    access_notes: str = ""
    api_style: ApiStyle
    api_breadth: Breadth
    api_notes: str = ""
    docs_url: str = ""
    mcp: Mcp
    mcp_url: str = ""
    verdict: Verdict
    main_blocker: Blocker
    blocker_notes: str = ""
    confidence: Confidence
    evidence: list[Evidence]


def record_json_schema() -> dict:
    """JSON schema the researcher must return (n/app/category are filled by us)."""
    schema = AppRecord.model_json_schema()
    for key in ("n", "app", "category"):
        schema["properties"].pop(key, None)
        schema["required"].remove(key)
    return schema
