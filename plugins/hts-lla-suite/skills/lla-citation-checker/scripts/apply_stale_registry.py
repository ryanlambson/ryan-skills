#!/usr/bin/env python3
"""
apply_stale_registry.py

Cross-checks extracted citations against the known-stale-citations registry.
Hits become WARN (with current section number suggested as the fix) or FAIL
(if the cited authority has been outright repealed).

Inputs:
    --citations JSON_PATH   Output of extract_citations.py
    --registry PATH         Path to references/stale-citations-registry.md
                            (default: ../references/stale-citations-registry.md)
    --output PATH           Where to write the JSON (default: stdout)

Outputs:
    JSON with per-citation flag.

Exit codes:
    0   OK
    1   Registry malformed
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_registry(registry_path: Path) -> list[dict]:
    """
    Parse the stale-citations-registry.md file.

    Expected structure: a Markdown table with columns:
        | Citation | Status | Replacement | Notes |
    Each row becomes a registry entry.
    Status is one of: STALE-RENUMBERED, STALE-REPEALED, STALE-SUPERSEDED.
    """
    entries = []
    in_table = False
    header_seen = False
    text = registry_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            if not header_seen:
                if any(c.lower().startswith("citation") for c in cols):
                    header_seen = True
                    in_table = True
                    continue
            elif in_table and cols and all(c.startswith("-") or c == "" for c in cols):
                # separator row
                continue
            elif in_table:
                if len(cols) >= 3 and cols[0]:
                    entries.append(
                        {
                            "citation": cols[0],
                            "status": cols[1],
                            "replacement": cols[2] if len(cols) > 2 else "",
                            "notes": cols[3] if len(cols) > 3 else "",
                        }
                    )
        elif in_table and not stripped:
            in_table = False
            header_seen = False
    return entries


def matches(citation_raw: str, registry_pattern: str) -> bool:
    """Check whether a citation matches a registry pattern (case-insensitive substring)."""
    return registry_pattern.lower() in citation_raw.lower()


def apply(citations: list[dict], registry: list[dict]) -> list[dict]:
    results = []
    for c in citations:
        for entry in registry:
            if matches(c["raw"], entry["citation"]):
                verdict = "WARN" if "REPEALED" not in entry["status"].upper() else "FAIL"
                results.append(
                    {
                        "citation_id": c["citation_id"],
                        "type": c["type"],
                        "raw": c["raw"],
                        "location": c["location"],
                        "verdict": verdict,
                        "source_basis": f"apply_stale_registry: matched '{entry['citation']}' — status {entry['status']}",
                        "suggested_fix": entry["replacement"] or entry["notes"] or "Check current consolidation",
                    }
                )
                break
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--citations", required=True, type=Path)
    p.add_argument("--registry", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    if not args.citations.exists():
        print(f"ERROR: Citations file not found: {args.citations}", file=sys.stderr)
        sys.exit(1)

    if args.registry is None:
        # Default to references/stale-citations-registry.md relative to this script
        args.registry = Path(__file__).parent.parent / "references" / "stale-citations-registry.md"

    if not args.registry.exists():
        print(f"ERROR: Registry file not found: {args.registry}", file=sys.stderr)
        sys.exit(1)

    try:
        registry = parse_registry(args.registry)
    except Exception as e:
        print(f"ERROR: Registry malformed: {e}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(args.citations.read_text(encoding="utf-8"))
    results = apply(data["citations"], registry)

    out = json.dumps(
        {"check": "apply_stale_registry", "registry_entries": len(registry), "results": results},
        indent=2,
    )
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
