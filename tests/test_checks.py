"""Unit tests for the deterministic verification pieces (no network, no LLM)."""

from agent.checks import _is_primary, _root, lint, quote_score
from agent.schema import AppRecord, Evidence
from agent.score import field_match

FIELDS = ("auth_methods", "access", "api_style", "mcp", "verdict")


def make_record(**overrides) -> AppRecord:
    base = dict(
        n=3, app="Pipedrive", category="CRM and Sales", one_liner="CRM", auth_methods=["api_key"],
        access="self_serve_free", api_style="rest", api_breadth="broad", mcp="official",
        mcp_url="https://example.com/mcp", verdict="ready", main_blocker="none", confidence="high",
        evidence=[Evidence(field=f, url="https://developers.pipedrive.com/docs", quote="x") for f in FIELDS],
    )
    return AppRecord(**{**base, **overrides})


def test_quote_found_verbatim_after_normalising_whitespace_and_case():
    page = "Intro.\n\nAll   requests must include an API   token.\nMore text."
    assert quote_score("all requests must include an API token.", page) == 1.0


def test_quote_with_curly_quotes_matches_straight_quotes():
    assert quote_score("it's free", "Yes, it’s free for developers") == 1.0


def test_missing_quote_scores_low():
    assert quote_score("Enterprise plan required for API access", "Totally unrelated page text") < 0.85


def test_clean_record_has_no_lint_issues():
    assert lint(make_record()) == []


def test_lint_flags_ready_verdict_on_gated_app():
    issues = lint(make_record(access="contact_sales"))
    assert any("verdict 'ready'" in i for i in issues)


def test_lint_flags_blocked_without_blocker_and_missing_evidence():
    rec = make_record(verdict="blocked", main_blocker="none", evidence=[])
    issues = lint(rec)
    assert any("main_blocker 'none'" in i for i in issues)
    assert sum("no evidence" in i for i in issues) == len(FIELDS)


def test_root_domain_and_vendor_detection():
    assert _root("https://developers.pipedrive.com/docs/api") == "pipedrive.com"
    rec = make_record()
    roots = {"pipedrive.com"}
    assert _is_primary("https://www.pipedrive.com/en/pricing", rec, roots)
    assert not _is_primary("https://someblog.io/pipedrive-review", rec, roots)
    assert _is_primary("https://github.com/pipedrive/mcp-server", rec, roots)


def test_auth_methods_scored_as_set_and_scalars_exactly():
    assert field_match("auth_methods", ["oauth2", "api_key"], ["api_key", "oauth2"])
    assert not field_match("auth_methods", ["oauth2"], ["oauth2", "other"])
    assert not field_match("access", "self_serve_trial", "self_serve_free")
