#!/usr/bin/env python3
"""
extract_citations.py

Regex-based citation extractor for the lla-citation-checker skill.

Reads an HTS LLA draft (Markdown or .docx) and emits a structured JSON list
of every citation it can identify, with its type and location.

Inputs:
    --input PATH        Path to the draft (.md or .docx)
    --output PATH       Where to write the JSON (default: stdout)

Outputs:
    JSON array of citation objects. Each object:
        {
            "citation_id": "c-001",
            "type": "5.1..5.10",          # Per SKILL.md Section 5
            "raw": "the exact citation text",
            "location": {"line": N, "heading": "<text>"},
            "details": {...}              # type-specific extracted fields
        }

Exit codes:
    0   OK
    1   Input file unreadable
    2   Parse error
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Citation type patterns. Each pattern is keyed by the SKILL.md Section 5 subtype.
PATTERNS = {
    # 5.1 — Project knowledge file reference: (Source: FILE.md, Section X) or (Source: FILE.md)
    "5.1": re.compile(
        r"\(Source:\s*(?P<file>[A-Z][A-Za-z0-9_]+\.md)"
        r"(?:,\s*Section\s+(?P<section>[^)]+))?\)"
    ),
    # 5.2 — Legislation: *Act Name Year* (STATE), s.N(M)
    "5.2": re.compile(
        r"\*(?P<act>[A-Za-z][A-Za-z0-9 ]+?(?:Act|Code)\s+\d{4})\*\s*"
        r"\((?P<state>NSW|WA|VIC|QLD|SA|TAS|ACT|NT|Cth)\)"
        r"(?:,\s*(?:s\.?|section\s*)(?P<section>\d+[A-Z]?(?:\(\d+\))?(?:\([a-z]\))?))?"
    ),
    # 5.3 — Regulations: *Regulation Name Year* (STATE), cl.N or reg.N
    "5.3": re.compile(
        r"\*(?P<reg>[A-Za-z][A-Za-z0-9 ]+?Regulations?\s+\d{4})\*\s*"
        r"\((?P<state>NSW|WA|VIC|QLD|SA|TAS|ACT|NT|Cth)\)"
        r"(?:,\s*(?:cl\.?|clause\s*|reg\.?|regulation\s*)(?P<section>\d+[A-Z]?))?"
    ),
    # 5.4 — ILGA Guidelines: ILGA Guideline N [— Title] (DD Month YYYY)[, paragraph X]
    "5.4": re.compile(
        r"ILGA\s+Guideline\s+(?P<number>\d+)"
        r"(?:\s*[—-]\s*(?P<title>[^(]+?))?"
        r"\s*\((?P<date>\d{1,2}\s+\w+\s+\d{4})\)"
        r"(?:,\s*paragraph\s+(?P<paragraph>[\d.]+))?",
        re.IGNORECASE,
    ),
    # 5.5 — Director's Policies (WA only): Director's Policy ...
    "5.5": re.compile(
        r"Director(?:'|')s\s+Policy"
        r"(?:\s*\(Guidance\))?"
        r"(?:\s*[—-]\s*(?P<title>[^,]+?))?"
        r"(?:,\s*paragraph\s+(?P<paragraph>[\d.]+))?",
        re.IGNORECASE,
    ),
    # 5.6 — L&GNSW operational guidance: L&GNSW, [Page Title] (nsw.gov.au)
    "5.6": re.compile(
        r"L&GNSW,\s*(?P<page>[^(]+?)\s*\(nsw\.gov\.au\)"
        r"(?:,\s*(?P<element>[^)]+))?",
        re.IGNORECASE,
    ),
    # 5.7 — Case law: Common patterns
    "5.7-wa": re.compile(
        r"(?P<case>Carnegies|Sand Volley|Pilbara s\.64|Liquorland Karrinyup)"
        r"(?:\s*\((?P<cite>[^)]+)\))?",
        re.IGNORECASE,
    ),
    "5.7-nsw": re.compile(
        r"(?:ILGA Decision|NCAT|NSW Supreme Court)"
        r"(?:[: ]+)(?P<case>[A-Z][A-Za-z0-9 &]+?)"
        r"\s*\((?P<date>[^)]+)\)",
        re.IGNORECASE,
    ),
    # 5.8 — Planning instruments
    "5.8": re.compile(
        r"(?P<lga>[A-Z][A-Za-z]+(?:\s+of\s+[A-Z][A-Za-z]+)?(?:\s+[A-Z][A-Za-z]+)?)"
        r"\s+(?P<instrument>LEP|DCP|LPS|LPP|Local\s+Planning\s+Strategy)"
        r"(?:\s+(?P<year>\d{4}))?"
        r"(?:,\s*(?:clause\s+|cl\.?\s*|s\.?\s*)(?P<section>[\d.]+))?",
    ),
    # 5.9 — Data citations
    "5.9-bocsar": re.compile(
        r"BOCSAR(?:\s+Crime\s+Tool)?,?\s*"
        r"(?P<area>[A-Z][A-Za-z ]+?)(?:\s+LGA)?,?\s*"
        r"(?P<metric>[A-Za-z][A-Za-z0-9 -]+?)"
        r"\s*(?P<period>\d{4}(?:[–-]\d{2,4})?)?",
        re.IGNORECASE,
    ),
    "5.9-abs": re.compile(
        r"ABS\s+(?P<dataset>Census\s+\d{4}|SEIFA\s+\d{4}|Quickstats)"
        r"(?:,\s*(?P<area>[^,]+?))?"
        r"(?:,\s*(?P<element>[^,]+?))?",
        re.IGNORECASE,
    ),
    "5.9-health": re.compile(
        r"NSW\s+Health(?:\s+HealthStats|\s+Surveillance\s+Report)?"
        r"(?:,\s*(?P<area>[^,]+?))?",
        re.IGNORECASE,
    ),
    # 5.10 — Web URLs
    "5.10": re.compile(r"https?://[^\s)>\]]+"),
}


def read_input(path: Path) -> tuple[list[str], list[str]]:
    """Return (lines, headings) where headings is a list of current-heading-per-line."""
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError:
            print(
                "ERROR: python-docx not installed. Install with: pip install python-docx",
                file=sys.stderr,
            )
            sys.exit(1)
        doc = Document(str(path))
        lines = []
        for para in doc.paragraphs:
            lines.append(para.text)
    elif path.suffix.lower() in (".md", ".txt"):
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        print(f"ERROR: Unsupported file type: {path.suffix}", file=sys.stderr)
        sys.exit(1)

    # Track the current heading for each line
    headings = []
    current = ""
    heading_pattern = re.compile(r"^#{1,6}\s+(.*)$")
    for line in lines:
        m = heading_pattern.match(line)
        if m:
            current = m.group(1).strip()
        headings.append(current)
    return lines, headings


def extract(lines: list[str], headings: list[str]) -> list[dict]:
    citations = []
    citation_id_counter = 0
    for i, line in enumerate(lines, start=1):
        for type_code, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                citation_id_counter += 1
                citations.append(
                    {
                        "citation_id": f"c-{citation_id_counter:03d}",
                        "type": type_code,
                        "raw": match.group(0),
                        "location": {"line": i, "heading": headings[i - 1]},
                        "details": {
                            k: v for k, v in match.groupdict().items() if v is not None
                        },
                    }
                )
    return citations


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Draft document path")
    p.add_argument("--output", type=Path, help="Output JSON path (default: stdout)")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        lines, headings = read_input(args.input)
        citations = extract(lines, headings)
    except Exception as e:
        print(f"ERROR: Parse failure: {e}", file=sys.stderr)
        sys.exit(2)

    out = json.dumps({"document": str(args.input), "citations": citations}, indent=2)
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
