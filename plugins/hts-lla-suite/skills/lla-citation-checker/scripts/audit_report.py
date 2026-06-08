#!/usr/bin/env python3
"""
audit_report.py

Composes the final structured audit report from upstream JSON outputs of the
other lla-citation-checker scripts.

Inputs:
    --extracted JSON_PATH       Output of extract_citations.py (the full list)
    --internal JSON_PATH        Output of verify_internal_refs.py
    --stale JSON_PATH           Output of apply_stale_registry.py
    --uncited JSON_PATH         Output of detect_uncited_claims.py
    --live JSON_PATH            (Optional) Output of verify_legislation_live.py
    --format md|json            Audit report format (default: md)
    --jurisdiction WA|NSW       Recorded in the report (default: auto-detect from extracted)
    --output PATH               Where to write the report (default: stdout)

Outputs:
    Markdown or JSON audit report per Section 7 of SKILL.md.

Exit codes:
    0   OK (regardless of audit verdict — the verdict is in the report)
    1   Input issue
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_results(extracted: list[dict], *result_sets: list[dict]) -> list[dict]:
    """
    Merge all per-check results onto the extracted-citations baseline.
    Each citation gets the most severe verdict across all checks
    (FAIL > WARN > PASS), and the source_basis aggregates from the
    contributing checks.
    """
    severity = {"FAIL": 3, "WARN": 2, "PASS": 1, None: 0}
    by_id = {c["citation_id"]: {**c, "verdict": None, "source_basis": [], "suggested_fix": []} for c in extracted}

    for results in result_sets:
        for r in results:
            cid = r.get("citation_id")
            if cid and cid in by_id:
                existing_verdict = by_id[cid]["verdict"]
                new_verdict = r.get("verdict")
                if severity.get(new_verdict, 0) > severity.get(existing_verdict, 0):
                    by_id[cid]["verdict"] = new_verdict
                if r.get("source_basis"):
                    by_id[cid]["source_basis"].append(r["source_basis"])
                if r.get("suggested_fix"):
                    by_id[cid]["suggested_fix"].append(r["suggested_fix"])

    # Default any citation with no checks run to PASS
    for c in by_id.values():
        if c["verdict"] is None:
            c["verdict"] = "PASS"
            c["source_basis"] = ["audit_report: no checks applied to this type"]
            c["suggested_fix"] = []
        # Flatten lists
        c["source_basis"] = "; ".join(c["source_basis"]) if c["source_basis"] else ""
        c["suggested_fix"] = "; ".join(c["suggested_fix"]) if c["suggested_fix"] else None

    return list(by_id.values())


def compose_md(merged: list[dict], uncited: list[dict], document: str, jurisdiction: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    pass_count = sum(1 for c in merged if c["verdict"] == "PASS")
    warn_count = sum(1 for c in merged if c["verdict"] == "WARN")
    fail_count = sum(1 for c in merged if c["verdict"] == "FAIL")
    disposition = "Blocked — fix FAILs and re-run" if fail_count > 0 else "Cleared for Stage 2"

    lines = []
    lines.append(f"# Citation Audit Report — {Path(document).name}")
    lines.append("")
    lines.append(f"**Jurisdiction:** {jurisdiction}")
    lines.append(f"**Document:** {document}")
    lines.append(f"**Date:** {timestamp}")
    lines.append(f"**Total citations extracted:** {len(merged)}")
    lines.append(f"**Uncited claims detected:** {len(uncited)}")
    lines.append(f"**Verdict summary:** {pass_count} PASS / {warn_count} WARN / {fail_count} FAIL")
    lines.append(f"**Disposition:** {disposition}")
    lines.append("")

    fails = [c for c in merged if c["verdict"] == "FAIL"]
    if fails:
        lines.append("## FAILs (must fix before delivery)")
        for c in fails:
            loc = c["location"]
            loc_str = f"line {loc.get('line', '?')}"
            if loc.get("heading"):
                loc_str += f" ({loc['heading']})"
            lines.append(f"- [{loc_str}] `{c['raw']}` — {c['source_basis']}")
            if c.get("suggested_fix"):
                lines.append(f"  - Suggested fix: {c['suggested_fix']}")
        lines.append("")

    warns = [c for c in merged if c["verdict"] == "WARN"]
    if warns:
        lines.append("## WARNs (review before delivery)")
        for c in warns:
            loc = c["location"]
            loc_str = f"line {loc.get('line', '?')}"
            if loc.get("heading"):
                loc_str += f" ({loc['heading']})"
            lines.append(f"- [{loc_str}] `{c['raw']}` — {c['source_basis']}")
            if c.get("suggested_fix"):
                lines.append(f"  - Suggested action: {c['suggested_fix']}")
        lines.append("")

    if uncited:
        lines.append("## Uncited assertions detected")
        for u in uncited:
            lines.append(f"- [para {u['location']['paragraph_index']}] {u['excerpt']}")
            if u.get("triggers"):
                lines.append(f"  - Triggers: {', '.join(u['triggers'])}")
            if u.get("suggested_fix"):
                lines.append(f"  - Suggested fix: {u['suggested_fix']}")
        lines.append("")

    manual_type_4 = [c for c in merged if "manual" in (c.get("source_basis") or "").lower() or c["type"] in ("5.4", "5.5", "5.6")]
    if manual_type_4:
        lines.append("## Manual Type-4 verification recommended")
        lines.append("Confirm the cited source actually says what the document claims:")
        for c in manual_type_4[:10]:  # cap to top 10 for readability
            loc = c["location"]
            lines.append(f"- {c['raw']} (line {loc.get('line', '?')})")
        if len(manual_type_4) > 10:
            lines.append(f"- … and {len(manual_type_4) - 10} more")
        lines.append("")

    if pass_count:
        lines.append("## PASSes (silent — for the record)")
        lines.append(f"{pass_count} citation(s) passed all automated checks.")
        lines.append("")

    return "\n".join(lines)


def compose_json(merged: list[dict], uncited: list[dict], document: str, jurisdiction: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    pass_count = sum(1 for c in merged if c["verdict"] == "PASS")
    warn_count = sum(1 for c in merged if c["verdict"] == "WARN")
    fail_count = sum(1 for c in merged if c["verdict"] == "FAIL")
    disposition = "blocked" if fail_count > 0 else "cleared_for_stage_2"

    report = {
        "document": document,
        "jurisdiction": jurisdiction,
        "timestamp": timestamp,
        "summary": {
            "total": len(merged),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "uncited_claims": len(uncited),
        },
        "disposition": disposition,
        "citations": merged,
        "uncited_claims": uncited,
    }
    return json.dumps(report, indent=2)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--extracted", required=True, type=Path)
    p.add_argument("--internal", type=Path)
    p.add_argument("--stale", type=Path)
    p.add_argument("--uncited", type=Path)
    p.add_argument("--live", type=Path)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--jurisdiction", default="unknown")
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    if not args.extracted.exists():
        print(f"ERROR: Extracted file not found: {args.extracted}", file=sys.stderr)
        sys.exit(1)

    extracted_data = load(args.extracted)
    extracted = extracted_data["citations"]
    document = extracted_data.get("document", "")

    result_sets = []
    for path in (args.internal, args.stale, args.live):
        if path and path.exists():
            result_sets.append(load(path).get("results", []))

    uncited = []
    if args.uncited and args.uncited.exists():
        uncited = load(args.uncited).get("results", [])

    merged = merge_results(extracted, *result_sets)

    if args.format == "md":
        out = compose_md(merged, uncited, document, args.jurisdiction)
    else:
        out = compose_json(merged, uncited, document, args.jurisdiction)

    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
