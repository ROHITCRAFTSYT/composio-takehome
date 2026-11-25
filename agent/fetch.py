"""Page fetcher shared by the researcher tools and the evidence loop.

httpx first; if the page is a JS shell (too little text) or blocks plain
clients, fall back to a headless Chromium render via Playwright. Every fetch
is cached on disk so the verifier sees the same bytes the researcher saw and
re-runs are cheap.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import threading
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx
import trafilatura

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"
MIN_USEFUL_CHARS = 600
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)
HTTP_TIMEOUT_S = 25
BROWSER_TIMEOUT_MS = 35_000
READER_PROXY = "https://r.jina.ai/"


@dataclass(frozen=True)
class Page:
    url: str
    final_url: str
    status: int
    text: str
    via: str  # "http" | "browser" | "reader" | "error"
    error: str = ""


def _cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")


def _html_to_text(html: str) -> str:
    text = trafilatura.extract(html, include_tables=True, include_links=False, favor_recall=True) or ""
    if len(text) < MIN_USEFUL_CHARS:  # trafilatura drops nav-heavy docs; keep raw text too
        raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
        raw = re.sub(r"(?s)<[^>]+>", " ", raw)
        raw = re.sub(r"\s+", " ", raw)
        text = text + "\n" + raw if text else raw
    return text.strip()


def _fetch_http(url: str) -> Page:
    with httpx.Client(follow_redirects=True, timeout=HTTP_TIMEOUT_S, headers={"User-Agent": USER_AGENT}) as client:
        resp = client.get(url)
    ctype = resp.headers.get("content-type", "")
    body = resp.text if ("html" in ctype or "text" in ctype or "json" in ctype) else ""
    text = _html_to_text(body) if "html" in ctype else body
    return Page(url, str(resp.url), resp.status_code, text, "http")


def _fetch_browser(url: str) -> Page:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=USER_AGENT)
            resp = page.goto(url, wait_until="domcontentloaded", timeout=BROWSER_TIMEOUT_MS)
            try:
                page.wait_for_load_state("networkidle", timeout=8_000)
            except Exception:  # noqa: BLE001 - long-polling pages never go idle; content is usually there
                pass
            text = page.inner_text("body")
            return Page(url, page.url, resp.status if resp else 0, re.sub(r"\s+\n", "\n", text), "browser")
        finally:
            browser.close()


def fetch(url: str, *, force_browser: bool = False, use_cache: bool = True) -> Page:
    """Fetch a URL as readable text, with cache and browser fallback."""
    cache = _cache_path(url + ("#browser" if force_browser else ""))
    if use_cache and cache.exists():
        try:
            return Page(**json.loads(cache.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, TypeError):
            pass  # corrupt or old-format cache entry: refetch

    page: Page | None = None
    errors: list[str] = []
    if not force_browser:
        try:
            page = _fetch_http(url)
            if page.status >= 400 or len(page.text) < MIN_USEFUL_CHARS:
                errors.append(f"http {page.status}, {len(page.text)} chars")
                page = None
        except Exception as exc:  # noqa: BLE001 - recorded and retried in the browser
            errors.append(f"http error: {exc!r}"[:300])
    if page is None:
        try:
            page = _fetch_browser(url)
            if page.status >= 400 or len(page.text) < MIN_USEFUL_CHARS:
                errors.append(f"browser {page.status}, {len(page.text)} chars")
                page = None
        except Exception as exc:  # noqa: BLE001 - recorded and retried through the reader
            errors.append(f"browser error: {exc!r}"[:300])
    if page is None:
        # Some vendor doc hosts (developers.facebook.com, developer.salesforce.com) refuse
        # connections from this network; a public reader proxy returns the same page text.
        try:
            proxied = _fetch_http(READER_PROXY + url)
            if proxied.status < 400 and len(proxied.text) >= MIN_USEFUL_CHARS:
                page = Page(url, url, proxied.status, proxied.text, "reader")
            else:
                errors.append(f"reader {proxied.status}")
        except Exception as exc:  # noqa: BLE001 - surfaced to caller as an error page
            errors.append(f"reader error: {exc!r}"[:300])
    if page is None:
        page = Page(url, url, 0, "", "error", "; ".join(errors))

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if page.via != "error":  # never cache failures; a retry should hit the network again
        tmp = cache.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(asdict(page)), encoding="utf-8")
        os.replace(tmp, cache)  # atomic, so parallel readers never see a half-written file
    return page
