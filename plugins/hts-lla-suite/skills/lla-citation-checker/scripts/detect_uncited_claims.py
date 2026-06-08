#!/usr/bin/env python3
"""
detect_uncited_claims.py

Heuristic detector for factual claims appearing without a nearby citation marker.
Looks for sentences containing numeric values, named authorities, regulator names,
Act/section references, or statistical claims, and flags any that have no citation
within the same paragraph.

Inputs:
    --input PATH        Path to the draft (.md or .docx)
    --output PATH       Where to write the JSON (default: stdout)

Outputs:
    JSON list of uncited claims (each becomes a WARN in the audit report).

Exit codes:
    0   OK
    1   Input issue
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Triggers — phrases or patterns that indicate a factual claim is being made
CLAIM_TRIGGERS = [
    re.compile(r"\b\d+(?:\.\d+)?\s*(?:%|per\s*cent|percent)\b", re.IGNORECASE),  # percentages
    re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"),  # large numbers with commas
    re.compile(r"\bsection\s+\d+[A-Z]?", re.IGNORECASE),  # section references
    re.compile(r"\bs\.\s*\d+[A-Z]?(?:\(\d+\))?", re.IGNORECASE),  # s.NN
    re.compile(r"\bclause\s+\d+", re.IGNORECASE),  # clauses
    re.compile(r"\bILGA\b"),  # named authority
    re.compile(r"\bBOCSAR\b"),  # named authority
    re.compile(r"\bL&GNSW\b|\bLiquor\s*&\s*Gaming\s*NSW\b"),  # named authority
    re.compile(r"\bABS\b|\bAustralian\s+Bureau\s+of\s+Statistics\b"),  # named authority
    re.compile(r"\bGuideline\s+\d+", re.IGNORECASE),  # ILGA Guideline reference
    re.compile(r"\bCarnegies\b"),  # WA case name
    re.compile(r"\bNCAT\b"),  # NSW tribunal
    re.compile(r"\bbetween\s+\d{4}\s+and\s+\d{4}\b", re.IGNORECASE),  # year ranges
]

# Citation markers — if any of these are in the same paragraph, the claim is considered cited
CITATION_MARKERS = [
    re.compile(r"\(Source:", re.IGNORECASE),
    re.compile(r"\*[A-Z][A-Za-z ]+(?:Act|Regulations?|Code)\s+\d{4}\*"),  # statute marker
    re.compile(r"ILGA\s+Guideline\s+\d+", re.IGNORECASE),
    re.compile(r"BOCSAR.*\b\d{4}\b", re.IGNORECASE),
    re.compile(r"ABS.*\b\d{4}\b", re.IGNORECASE),
    re.compile(r"https?://\S+"),
    re.compile(r"\bdecision[s]?\s+of\b", re.IGNORECASE),  # ILGA decision references
]

# Sentences inside these constructs are exempt
EXEMPT_PATTERNS = [
    re.compile(r"^\s*[-*•]\s+", re.MULTILINE),  # bullet headers (lists of factors)
    re.compile(r"^\s*\|", re.MULTILINE),  # table rows
    re.compile(r"^#{1,6}\s+", re.MULTILINE),  # headings
]


def read_input(path: Path) -> list[str]:
    """Return paragraphs from the document."""
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
        paragraphs = [p.text for p in doc.paragraphs]
    else:
        text = path.read_text(encoding="utf-8")
        # Paragraphs separated by blank lines (markdown convention)
        paragraphs = re.split(r"\n\s*\n", text)
    return paragraphs


def is_exempt(paragraph: str) -> bool:
    """Check if the whole paragraph is exempt from claim detection."""
    if not paragraph.strip():
        return True
    if any(p.search(paragraph) for p in EXEMPT_PATTERNS):
        # Check if the WHOLE paragraph is one of the exempt structures
        # (i.e., heading-only or single-bullet paragraphs are exempt)
        if paragraph.lstrip().startswith(("#", "-", "*", "•", "|")):
            return True
    return False


def has_citation(paragraph: str) -> bool:
    """Check if the paragraph contains at least one citation marker."""
    return any(p.search(paragraph) for p in CITATION_MARKERS)


def detect(paragraphs: list[str]) -> list[dict]:
    uncited = []
    counter = 0
    for line_idx, para in enumerate(paragraphs, start=1):
        if is_exempt(para):
            continue
        # Identify claim triggers in this paragraph
        triggers_found = []
        for pat in CLAIM_TRIGGERS:
            for match in pat.finditer(para):
                triggers_found.append(match.group(0))
        if not triggers_found:
            continue
        if has_citation(para):
            continue
        # Uncited claim
        counter += 1
        uncited.append(
            {
                "claim_id": f"u-{counter:03d}",
                "location": {"paragraph_index": line_idx},
                "verdict": "WARN",
                "source_basis": "detect_uncited_claims: factual claim without nearby citation",
                "triggers": triggers_found[:3],  # cap at 3 for readability
                "excerpt": para[:200] + ("..." if len(para) > 200 else ""),
                "suggested_fix": "Add a citation in HTS format, or move this claim to a bulleted list (exempt)",
            }
        )
    return uncited


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    paragraphs = read_input(args.input)
    results = detect(paragraphs)

    out = json.dumps(
        {"check": "detect_uncited_claims", "results": results}, indent=2
    )
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
