#!/usr/bin/env python3
"""generate_md_patch.py - Phase E (default output) of regulatory-fact-refresh.

Produce a side-by-side before/after review patch for STALE and
CHANGED-CONDITIONAL claims. Never rewrites the source; emits a review document
only. Per the no-scalar-swap rule, CHANGED-CONDITIONAL items show the verified
statement WITH its condition, never a bare value substitution.

Usage:
    python generate_md_patch.py --claims verified.json [--output PATH]
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()

    claims = json.loads(Path(args.claims).read_text(encoding="utf-8"))
    actionable = [c for c in claims
                  if c.get("status") in ("STALE", "CHANGED-CONDITIONAL")]

    lines = ["# Proposed corrections (for review - nothing applied)", ""]
    if not actionable:
        lines.append("No STALE or CHANGED-CONDITIONAL items. Nothing to patch.")
    for c in actionable:
        loc = c.get("location", {})
        lines.append(f"## {c['text']}  ({c.get('status')})")
        lines.append(f"- Location: line {loc.get('line', '?')}")
        lines.append(f"- Before: {c['text']}")
        if c.get("status") == "STALE":
            lines.append(f"- After (suggested): {c.get('new_value', '?')}")
        else:  # CHANGED-CONDITIONAL: statement with condition, never a swap
            condition = " ".join((c.get("condition") or "?").split())
            lines.append(f"- After (suggested statement): {condition}")
        source = " ".join((c.get("primary_source") or "").split())
        lines.append(f"- Source: {source}")
        lines.append("")

    payload = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
