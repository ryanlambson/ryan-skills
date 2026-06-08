#!/usr/bin/env python3
"""
scrape_dynamic.py — Heavy scraper for JS-rendered pages.

Used by skill-builder Phase 2 (Research) Tier 3 when scrape_static.py returns empty
or under-populated content (a strong signal the page is JS-rendered). Slower than
scrape_static (~5-10s cold start) but handles single-page apps, lazy-loaded content,
and content behind client-side routing.

Inputs:
    --url URL                   The URL to scrape (required, can repeat)
    --output FILE               Output JSON path (default: stdout)
    --selector CSS_SELECTOR     Optional CSS selector to wait for and extract
    --wait-ms MILLISECONDS      Extra wait after load (default: 1500)
    --text-only                 Return plain text only (default: structured JSON)
    --timeout SECONDS           Page load timeout (default: 60)

Output (JSON): same shape as scrape_static.py.

Exit codes:
    0   Success
    1   Network / load error
    2   Parse error
    3   Invalid arguments / missing dependency
    4   Playwright not installed (run: playwright install chromium)

Dependencies:
    pip install playwright beautifulsoup4 lxml
    playwright install chromium

Usage:
    python scrape_dynamic.py --url https://example-spa.com/docs
    python scrape_dynamic.py --url https://app.example.com --selector "main" --wait-ms 3000
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from urllib.parse import urljoin

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    sys.stderr.write(
        "Missing dependency: playwright.\n"
        "Run: pip install playwright && playwright install chromium\n"
    )
    sys.exit(4)

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write("Missing dependency: beautifulsoup4. Run: pip install beautifulsoup4 lxml\n")
    sys.exit(3)


USER_AGENT = "skill-builder/1.0 (+https://greenholmes.com.au)"


def scrape_url(playwright_ctx, url: str, selector: str = None, wait_ms: int = 1500,
               text_only: bool = False, timeout: int = 60) -> dict:
    """Fetch a JS-rendered URL via headless Chromium."""
    result = {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "status": None,
    }

    browser = playwright_ctx.chromium.launch(headless=True)
    try:
        ctx = browser.new_context(user_agent=USER_AGENT)
        page = ctx.new_page()

        try:
            resp = page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        except PlaywrightTimeout:
            result["error"] = "Page load timeout"
            return result

        if resp:
            result["status"] = resp.status

        if selector:
            try:
                page.wait_for_selector(selector, timeout=timeout * 1000)
            except PlaywrightTimeout:
                result["error"] = f"Selector '{selector}' never appeared"
                return result

        # Soft wait for late-rendering content
        page.wait_for_timeout(wait_ms)

        html = page.content()
    finally:
        browser.close()

    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    if selector:
        nodes = soup.select(selector)
        if not nodes:
            result["error"] = f"Selector '{selector}' not in final HTML"
            return result
        narrowed = BeautifulSoup("<div></div>", "html.parser")
        for node in nodes:
            narrowed.div.append(node)
        soup = narrowed

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title_tag = soup.find("title")
    result["title"] = title_tag.get_text(strip=True) if title_tag else ""

    if text_only:
        result["text"] = soup.get_text(separator="\n", strip=True)
        return result

    result["headings"] = [
        {"level": int(h.name[1]), "text": h.get_text(strip=True)}
        for h in soup.find_all(["h1", "h2", "h3", "h4"])
    ]

    main = soup.find("article") or soup.find("main") or soup.find("body") or soup
    result["main_text"] = main.get_text(separator="\n", strip=True) if main else ""

    result["links"] = [
        {"href": urljoin(url, a.get("href", "")), "text": a.get_text(strip=True)[:200]}
        for a in soup.find_all("a", href=True)
        if a.get_text(strip=True)
    ][:200]

    result["code_blocks"] = [
        code.get_text() for code in soup.find_all(["pre", "code"])
        if len(code.get_text(strip=True)) > 10
    ][:50]

    return result


def main():
    parser = argparse.ArgumentParser(description="Dynamic page scraper for skill-builder Phase 2.")
    parser.add_argument("--url", action="append", required=True, help="URL to scrape (repeatable)")
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")
    parser.add_argument("--selector", default=None, help="CSS selector to wait for")
    parser.add_argument("--wait-ms", type=int, default=1500, help="Extra wait after load")
    parser.add_argument("--text-only", action="store_true", help="Return plain text only")
    parser.add_argument("--timeout", type=int, default=60, help="Page load timeout in seconds")
    args = parser.parse_args()

    with sync_playwright() as p:
        results = [
            scrape_url(p, url, selector=args.selector, wait_ms=args.wait_ms,
                       text_only=args.text_only, timeout=args.timeout)
            for url in args.url
        ]

    payload = results[0] if len(results) == 1 else results
    output = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(output)

    if any(r.get("error") for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
