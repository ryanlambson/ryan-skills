#!/usr/bin/env python3
"""generate_freshness_report.py - Phase D of regulatory-fact-refresh.

Turn a verified claims register into a Markdown freshness report, grouped by
status (CHANGED-CONDITIONAL and STALE first, since they need attention).

Usage:
    python generate_freshness_report.py --claims verified.json \\
        [--document NAME] [--output PATH]
"""
import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

ORDER = ["CHANGED-CONDITIONAL", "STALE", "UNVERIFIED", "CURRENT"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--document", default="(input document)")
    ap.add_argument("--output")
    args = ap.parse_args()

    claims = json.loads(Path(args.claims).read_text(encoding="utf-8"))
    counts = Counter(c.get("status", "UNVERIFIED") for c in claims)

    lines = [
        f"# Freshness report - {args.document}",
        "",
        f"**Date:** {date.today().isoformat()}",
        f"**Claims checked:** {len(claims)}",
        "**Summary:** " + " / ".join(f"{counts.get(s, 0)} {s}" for s in ORDER),
        "",
        "| Claim | Type | Status | Current value / condition | Source |",
        "|---|---|---|---|---|",
    ]
    for status in ORDER:
        for c in claims:
            if c.get("status") != status:
                continue
            note = (c.get("condition") or c.get("new_value") or c.get("needs") or "")
            note = " ".join(note.split())
            src = " ".join((c.get("primary_source") or "").split())
            text = c["text"].replace("|", "\\|")
            lines.append(f"| {text} | {c['type']} | {status} | {note} | {src} |")

    payload = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
