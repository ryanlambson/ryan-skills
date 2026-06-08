#!/usr/bin/env python3
"""
verify_legislation_live.py

(--live mode only) Live-fetches legislation portals to verify that the cited
section actually exists in the current consolidation. Adds ~1-3 seconds per
citation. Reserve for immediately-before-lodgement runs.

Inputs:
    --citations JSON_PATH       Output of extract_citations.py
    --jurisdiction WA|NSW       Force jurisdiction (else inferred per citation)
    --output PATH               Where to write the JSON (default: stdout)

Outputs:
    JSON with per-citation verdict (PASS / WARN / FAIL) for type 5.2 and 5.3.

Exit codes:
    0   OK
    1   Network error (all live checks failed)
    2   Partial (some live checks failed)

NOTE: This script uses urllib from the standard library — no extra dependencies.
It does NOT perform full HTML parsing; it does a lightweight check for the
presence of the section anchor or the section label in the fetched page text.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


# Legislation portal endpoints. These may change; verify the URL pattern at first use.
NSW_LIQUOR_ACT_URL = (
    "https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-2007-090"
)
NSW_LIQUOR_REG_URL = (
    "https://legislation.nsw.gov.au/view/html/inforce/current/sl-2018-0473"
)
WA_LIQUOR_ACT_URL = (
    "https://www.legislation.wa.gov.au/legislation/statutes.nsf/main_mrtitle_564_homepage.html"
)


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "lla-citation-checker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def section_present(page_text: str, section: str) -> bool:
    """
    Check whether a section reference (e.g., '48(3)', '11A', '15') appears
    in the fetched page text. Looks for the literal section number, the
    'Section N' phrase, and anchor-style markers.
    """
    if not section:
        return False
    section_num = re.split(r"[(.]", section)[0].strip()  # e.g., '48' from '48(3)'
    patterns = [
        re.compile(rf"\bSection\s+{re.escape(section_num)}\b", re.IGNORECASE),
        re.compile(rf"\bs\.?\s*{re.escape(section_num)}\b", re.IGNORECASE),
        re.compile(rf"#sec[._]{re.escape(section_num)}\b", re.IGNORECASE),
        re.compile(rf"<a[^>]*name=\"?[^\"]*{re.escape(section_num)}[^\"]*\"?", re.IGNORECASE),
    ]
    return any(p.search(page_text) for p in patterns)


def verify(citations: list[dict], jurisdiction: str | None) -> list[dict]:
    results = []
    pages_cache = {}

    for c in citations:
        if c["type"] not in ("5.2", "5.3"):
            continue
        state = c["details"].get("state") or jurisdiction
        section = c["details"].get("section")
        if not state or not section:
            continue

        # Determine the portal URL
        if state == "NSW" and "Liquor Act" in c["raw"]:
            url = NSW_LIQUOR_ACT_URL
        elif state == "NSW" and "Liquor Regulation" in c["raw"]:
            url = NSW_LIQUOR_REG_URL
        elif state == "WA" and "Liquor Control Act" in c["raw"]:
            url = WA_LIQUOR_ACT_URL
        else:
            # Unknown legislation — skip live verification, mark for manual
            results.append(
                {
                    "citation_id": c["citation_id"],
                    "type": c["type"],
                    "raw": c["raw"],
                    "location": c["location"],
                    "verdict": "WARN",
                    "source_basis": "verify_legislation_live: no live endpoint configured",
                    "suggested_fix": "Manual verification required",
                }
            )
            continue

        try:
            if url not in pages_cache:
                pages_cache[url] = fetch(url)
            page_text = pages_cache[url]
        except urllib.error.URLError as e:
            results.append(
                {
                    "citation_id": c["citation_id"],
                    "type": c["type"],
                    "raw": c["raw"],
                    "location": c["location"],
                    "verdict": "WARN",
                    "source_basis": f"verify_legislation_live: network error — {e.reason}",
                    "suggested_fix": "Re-run --live when network is stable, or verify manually",
                }
            )
            continue
        except Exception as e:
            results.append(
                {
                    "citation_id": c["citation_id"],
                    "type": c["type"],
                    "raw": c["raw"],
                    "location": c["location"],
                    "verdict": "WARN",
                    "source_basis": f"verify_legislation_live: fetch failed — {e}",
                    "suggested_fix": "Manual verification required",
                }
            )
            continue

        if section_present(page_text, section):
            results.append(
                {
                    "citation_id": c["citation_id"],
                    "type": c["type"],
                    "raw": c["raw"],
                    "location": c["location"],
                    "verdict": "PASS",
                    "source_basis": f"verify_legislation_live: section {section} present in {url}",
                    "suggested_fix": None,
                }
            )
        else:
            results.append(
                {
                    "citation_id": c["citation_id"],
                    "type": c["type"],
                    "raw": c["raw"],
                    "location": c["location"],
                    "verdict": "FAIL",
                    "source_basis": f"verify_legislation_live: section {section} NOT found in {url}",
                    "suggested_fix": f"Verify the current section number for this provision (note: NSW Vibrancy Reforms have renumbered some sections; e.g., possibly s.48 → s.72I)",
                }
            )

    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--citations", required=True, type=Path)
    p.add_argument("--jurisdiction", choices=["WA", "NSW"])
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    if not args.citations.exists():
        print(f"ERROR: Citations file not found: {args.citations}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(args.citations.read_text(encoding="utf-8"))
    results = verify(data["citations"], args.jurisdiction)

    out = json.dumps(
        {"check": "verify_legislation_live", "results": results}, indent=2
    )
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)

    # Exit code logic
    if not results:
        sys.exit(0)
    fail_count = sum(1 for r in results if r["verdict"] == "FAIL")
    warn_count = sum(1 for r in results if r["verdict"] == "WARN")
    if fail_count == len(results):
        sys.exit(1)  # all failed
    if warn_count + fail_count > 0:
        sys.exit(2)  # partial
    sys.exit(0)


if __name__ == "__main__":
    main()
