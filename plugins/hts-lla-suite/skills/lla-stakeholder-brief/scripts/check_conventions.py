#!/usr/bin/env python3
"""check_conventions.py — deterministic pre-delivery check for HTS stakeholder briefs.

Purpose : Screen a drafted email (text/markdown) for HTS writing-convention breaches
          before it is presented for review.
Inputs  : Path(s) to one or more draft files (UTF-8 text or markdown).
Outputs : Line-numbered findings on stdout. Exit 0 = pass, 1 = findings, 2 = usage error.
Depends : Python 3 standard library only. No network access. Reads only the files given.

Checks
  1. Banned terms  : "sits" (flag for locational review), "food-led"/"food led",
                     "need"/"needs" (word), "community"/"communities" (word)
  2. Punctuation   : em-dash (U+2014) anywhere; spaced en-dash " – " used as
                     sentence punctuation
  3. CCTV scope    : phrases implying whole-of-premises coverage
  4. Placeholders  : [INSERT..., (TO DO), {{slot}}, bare "XX" tokens

Protected strings (statutory or proper-noun phrases) are excluded from the
banned-term checks. Extend PROTECTED as required.
"""
import re
import sys

PROTECTED = [
    "community or cultural matters",          # s.38(4)(ca) LCA 1988 (WA)
    "community and cultural matters",
    "Community Development",                  # department names
    "Health and Community Services",
    "Community Consultation",                 # PIA section title when quoted
]

CHECKS = [
    ("BANNED sits (review: locational use?)", re.compile(r"\bsits\b", re.I)),
    ("BANNED food-led", re.compile(r"\bfood[- ]led\b", re.I)),
    ("BANNED need/needs", re.compile(r"\bneeds?\b", re.I)),
    ("BANNED community/communities", re.compile(r"\bcommunit(?:y|ies)\b", re.I)),
    ("EM-DASH in text", re.compile(r"—")),
    ("SPACED EN-DASH as punctuation", re.compile(r"\s–\s")),
    ("CCTV scope breach", re.compile(
        r"CCTV[^.\n]{0,80}?(throughout|internal and external|all internal|"
        r"whole premises|full coverage|encompassing)|"
        r"(throughout|internal and external)[^.\n]{0,40}?CCTV", re.I)),
    ("PLACEHOLDER", re.compile(r"\[INSERT[^\]]*\]|\(TO DO\)|\{\{[^}]*\}\}|(?<![A-Za-z0-9])XX(?![A-Za-z0-9])")),
]


def mask_protected(line: str) -> str:
    for phrase in PROTECTED:
        line = re.sub(re.escape(phrase), "#" * len(phrase), line, flags=re.I)
    return line


def check_file(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"ERROR cannot read {path}: {exc}")
        return 2
    findings = 0
    for lineno, raw in enumerate(lines, start=1):
        masked = mask_protected(raw)
        for label, rx in CHECKS:
            for m in rx.finditer(masked):
                findings += 1
                snippet = raw.strip()[:90]
                print(f"{path}:{lineno}: {label}: ...{snippet}...")
    return 1 if findings else 0


def main(argv):
    if len(argv) < 2:
        print("usage: check_conventions.py <draft-file> [<draft-file> ...]")
        return 2
    worst = 0
    for path in argv[1:]:
        rc = check_file(path)
        worst = max(worst, rc)
    if worst == 0:
        print("PASS: no convention breaches found.")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
