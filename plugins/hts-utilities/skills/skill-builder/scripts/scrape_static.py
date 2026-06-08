#!/usr/bin/env python3
"""
scrape_static.py — Default scraper for static HTML pages.

Used by skill-builder Phase 2 (Research) Tier 3 to check live web sources against
internal knowledge. Fast, no browser required. Use scrape_dynamic.py for JS-rendered
pages.

Inputs:
    --url URL                   The URL to scrape (required, can repeat)
    --output FILE               Output JSON path (default: stdout)
    --selector CSS_SELECTOR     Optional CSS selector to extract specific content
    --text-only                 Return plain text only (default: structured JSON)
    --timeout SECONDS           Request timeout (default: 30)

Output (JSON):
    {
      "url": "...",
      "fetched_at": "ISO timestamp",
      "status": 200,
      "title": "...",
      "headings": [{"level": 2, "text": "..."}],
      "main_text": "...",
      "links": [{"href": "...", "text": "..."}],
      "code_blocks": ["..."]
    }

Exit codes:
    0   Success
    1   Network error
    2   Parse error
    3   Invalid arguments

Dependencies:
    pip install requests beautifulsoup4 lxml

Usage:
    python scrape_static.py --url https://agentskills.io/specification
    python scrape_static.py --url https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview --output spec.json
    python scrape_static.py --url https://github.com/anthropics/skills --selector "article" --text-only
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    sys.stderr.write(f"Missing dependency: {e.name}. Run: pip install requests beautifulsoup4 lxml\n")
    sys.exit(3)


USER_AGENT = "skill-builder/1.0 (+https://greenholmes.com.au)"


def scrape_url(url: str, selector: str = None, text_only: bool = False, timeout: int = 30) -> dict:
    """Fetch a URL and return structured content."""
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        return {
            "url": url,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "status": None,
            "error": str(e),
        }

    result = {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "status": resp.status_code,
    }

    if resp.status_code != 200:
        result["error"] = f"HTTP {resp.status_code}"
        return result

    try:
        soup = BeautifulSoup(resp.text, "lxml")
    except Exception:
        # lxml not available, fall back to html.parser
        soup = BeautifulSoup(resp.text, "html.parser")

    # If a CSS selector is provided, narrow the soup down
    if selector:
        nodes = soup.select(selector)
        if not nodes:
            result["error"] = f"Selector '{selector}' matched nothing"
            return result
        # Wrap in a temporary div for consistent extraction
        narrowed = BeautifulSoup("<div></div>", "html.parser")
        for node in nodes:
            narrowed.div.append(node)
        soup = narrowed

    # Strip script and style noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Title
    title_tag = soup.find("title")
    result["title"] = title_tag.get_text(strip=True) if title_tag else ""

    if text_only:
        result["text"] = soup.get_text(separator="\n", strip=True)
        return result

    # Structured extraction
    result["headings"] = [
        {"level": int(h.name[1]), "text": h.get_text(strip=True)}
        for h in soup.find_all(["h1", "h2", "h3", "h4"])
    ]

    # Main text — try <article>, <main>, then body
    main = soup.find("article") or soup.find("main") or soup.find("body") or soup
    result["main_text"] = main.get_text(separator="\n", strip=True) if main else ""

    # Links (resolved against base URL)
    result["links"] = [
        {"href": urljoin(url, a.get("href", "")), "text": a.get_text(strip=True)[:200]}
        for a in soup.find_all("a", href=True)
        if a.get_text(strip=True)
    ][:200]  # cap to prevent huge payloads

    # Code blocks (often the meat of technical docs)
    result["code_blocks"] = [
        code.get_text() for code in soup.find_all(["pre", "code"])
        if len(code.get_text(strip=True)) > 10
    ][:50]

    return result


def main():
    parser = argparse.ArgumentParser(description="Static page scraper for skill-builder Phase 2.")
    parser.add_argument("--url", action="append", required=True, help="URL to scrape (repeatable)")
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")
    parser.add_argument("--selector", default=None, help="Optional CSS selector to narrow scope")
    parser.add_argument("--text-only", action="store_true", help="Return plain text only")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    args = parser.parse_args()

    results = [
        scrape_url(url, selector=args.selector, text_only=args.text_only, timeout=args.timeout)
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

    # Exit non-zero if any URL errored
    if any(r.get("error") for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
