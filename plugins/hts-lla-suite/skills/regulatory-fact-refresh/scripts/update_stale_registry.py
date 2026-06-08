#!/usr/bin/env python3
"""update_stale_registry.py - append a verified entry to the master registry.

Adds one new entry to references/stale-citations.yaml in the promotable schema.
Enforces the verify-before-seed rule: refuses an entry without a primary_source
and verified_on, and refuses a CHANGED-CONDITIONAL entry without a condition.

Usage:
    python update_stale_registry.py \\
        --registry references/stale-citations.yaml --entry entry.json

NOTE: writes to the working copy of the registry. To persist beyond the session
and reach LLA outputs, fold the updated file back into the canonical bundle and
re-distribute the set skill (see the propagation-reminder skill). Runtime never
reads the registry from Google Drive.
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["id", "jurisdiction", "domain", "instrument", "old_value",
            "new_value", "status", "primary_source", "verified_on"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--entry", required=True, help="JSON file describing one entry")
    args = ap.parse_args()

    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required")

    entry = json.loads(Path(args.entry).read_text(encoding="utf-8"))

    missing = [k for k in REQUIRED if not entry.get(k)]
    if missing:
        sys.exit(f"refusing to add: missing required fields {missing}")
    if entry["status"] == "CHANGED-CONDITIONAL" and not entry.get("condition"):
        sys.exit("refusing to add: CHANGED-CONDITIONAL entry needs a condition")

    data = yaml.safe_load(Path(args.registry).read_text(encoding="utf-8")) or {}
    entries = data.setdefault("entries", [])
    if any(e.get("id") == entry["id"] for e in entries):
        sys.exit(f"entry id '{entry['id']}' already exists; edit it manually")

    entries.append(entry)
    Path(args.registry).write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"added entry '{entry['id']}' ({entry['status']})")


if __name__ == "__main__":
    main()
