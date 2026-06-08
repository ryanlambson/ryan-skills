#!/usr/bin/env python3
"""extract_claims.py - Phase A of regulatory-fact-refresh.

Scan an input document (.md, .txt, .docx, .pdf) for verifiable regulatory facts
and emit a categorised JSON claims register on stdout (or to --output).

Usage:
    python extract_claims.py --input PATH [--output PATH]

Deterministic, no network. Categorisation is heuristic (regex); review the
register before relying on it. The cognitive layer maps and verifies the claims
in later phases.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# (regex, claim type). Evaluated per line; a (line, col, text) span is recorded
# once. Order is roughly most-specific first.
PATTERNS = [
    (r"\[\d{4}\]\s*[A-Z]{2,6}\s*\d+", "case_citation"),              # [2021] WASC 366
    (r"\bs\.?\s?\d+[A-Za-z]*(?:\(\d+\))?(?:\([a-z]+\))?", "section_ref"),  # s.41A, s.38(4)(a)
    (r"\b[Rr]eg(?:ulation)?\.?\s?\d+[A-Za-z]*", "regulation_ref"),   # Regulation 9AAA
    (r"\b[Cc]l(?:ause)?\.?\s?\d+(?:\.\d+)*", "clause_ref"),          # cl 4.25
    (r"\bLPS\s*No\.?\s*\d+(?:\s*AMD\s*\d+)?", "planning_instrument"),# LPS No. 1 AMD 76
    (r"\b\d+\s?(?:patrons?|persons?|people)\b", "patron_threshold"),
    (r"\b\d+(?:\.\d+)?\s?(?:m2|m\u00b2|sqm|square\smetres?)\b", "area_threshold"),
    (r"\b\d+(?:\.\d+)?\s?km\b", "distance_threshold"),
    (r"\$\s?\d[\d,]*(?:\.\d{2})?", "fee"),
    (r"\b(?:[01]?\d|2[0-3])(?:[:.][0-5]\d)?\s?(?:am|pm)\b", "trading_hour"),
]


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        try:
            import docx  # python-docx
        except ImportError:
            sys.exit("python-docx is required to read .docx files")
        return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
    if suffix == ".pdf":
        try:
            from pdfminer.high_level import extract_text
        except ImportError:
            sys.exit("pdfminer.six is required to read .pdf files")
        return extract_text(str(path))
    sys.exit(f"unsupported input type: {suffix}")


def extract(text: str):
    claims = []
    seen = set()
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, ctype in PATTERNS:
            for m in re.finditer(pattern, line):
                key = (lineno, m.start(), m.group(0))
                if key in seen:
                    continue
                seen.add(key)
                claims.append({
                    "id": f"c-{len(claims) + 1:04d}",
                    "type": ctype,
                    "text": m.group(0).strip(),
                    "value": m.group(0).strip(),
                    "location": {"line": lineno, "col": m.start()},
                })
    return claims


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()
    claims = extract(read_text(Path(args.input)))
    payload = json.dumps(claims, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
