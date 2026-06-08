#!/usr/bin/env python3
"""verify_claim.py - Phases B-C of regulatory-fact-refresh.

Match each extracted claim against the hard-baked stale-citations registry and,
where a cached source is supplied, against that source. Assign a status.

Usage:
    python verify_claim.py --claims claims.json \\
        --registry references/stale-citations.yaml \\
        [--sources sources.json] [--output PATH]

Deterministic assignment:
    - registry hit (CHANGED-CONDITIONAL) -> CHANGED-CONDITIONAL (+ condition)
    - registry hit (STALE)               -> STALE
    - claimed value present in a cached source -> CURRENT
    - otherwise                          -> UNVERIFIED

Live web fetching and the CHANGED-CONDITIONAL decision test for *unknown*
patterns are performed by the cognitive layer, not here. This script encodes
only what can be decided deterministically; UNVERIFIED items are explicitly
handed back for live verification.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def load_registry(path: str):
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required to read the registry")
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return data.get("entries", [])


def registry_match(claim, entries):
    """Crude match: numeric overlap with old_value, or a provision appearing in
    the claim text. Heuristic by design; confirm hits before acting."""
    ctext = claim["text"].lower()
    ctext_nospace = ctext.replace(" ", "")
    for e in entries:
        old = str(e.get("old_value", "")).lower()
        for num in re.findall(r"\d+", old):
            if num in ctext:
                return e
        for prov in e.get("provisions", []):
            if str(prov).lower().replace(" ", "") in ctext_nospace:
                return e
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--sources", help="JSON {source_id: text} or a plain text file")
    ap.add_argument("--output")
    args = ap.parse_args()

    claims = json.loads(Path(args.claims).read_text(encoding="utf-8"))
    entries = load_registry(args.registry)

    sources_text = ""
    if args.sources:
        raw = Path(args.sources).read_text(encoding="utf-8")
        try:
            sources_text = " ".join(str(v) for v in json.loads(raw).values())
        except (ValueError, AttributeError):
            sources_text = raw
    sources_lower = sources_text.lower()

    for c in claims:
        hit = registry_match(c, entries)
        if hit:
            c["status"] = hit.get("status", "STALE")
            c["new_value"] = hit.get("new_value")
            c["condition"] = hit.get("condition")
            c["primary_source"] = hit.get("primary_source")
            c["registry_id"] = hit.get("id")
        elif sources_lower and c["text"].lower() in sources_lower:
            c["status"] = "CURRENT"
        else:
            c["status"] = "UNVERIFIED"
            c["needs"] = "live verification by cognitive layer"

    payload = json.dumps(claims, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
