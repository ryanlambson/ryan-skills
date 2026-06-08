#!/usr/bin/env python3
"""
verify_internal_refs.py

Cross-checks project knowledge file references (type 5.1 citations) — verifies
the cited file exists in the project knowledge folder and (if a section is
named) the file contains a heading matching the section reference.

Inputs:
    --citations JSON_PATH   Output of extract_citations.py
    --project-path PATH     Project knowledge folder path
                            (default: <citations.document_dir>/knowledge/)
    --output PATH           Where to write the JSON (default: stdout)

Outputs:
    JSON with per-citation verdict (PASS / FAIL).

Exit codes:
    0   OK
    1   Path issue
"""

import argparse
import json
import re
import sys
from pathlib import Path


def find_headings(file_path: Path) -> set[str]:
    """Return a set of all heading texts in a markdown file (case-insensitive normalised)."""
    headings = set()
    pattern = re.compile(r"^#{1,6}\s+(.*?)\s*$")
    try:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            m = pattern.match(line)
            if m:
                headings.add(_normalise(m.group(1)))
    except (OSError, UnicodeDecodeError):
        pass
    return headings


def _normalise(s: str) -> str:
    """Normalise a heading or section reference for matching."""
    # Lowercase, strip punctuation, collapse whitespace, drop leading numbering
    s = s.lower()
    s = re.sub(r"^\d+\.\s*", "", s)  # leading section number
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def heading_matches(section_ref: str, headings: set[str]) -> bool:
    """True if any heading in the file matches the section reference."""
    target = _normalise(section_ref)
    if target in headings:
        return True
    # Looser match: target is contained in a heading
    for h in headings:
        if target and target in h:
            return True
    return False


def verify(citations: list[dict], project_path: Path) -> list[dict]:
    results = []
    for c in citations:
        if c["type"] != "5.1":
            continue
        file_ref = c["details"].get("file")
        section_ref = c["details"].get("section")
        verdict = {
            "citation_id": c["citation_id"],
            "type": c["type"],
            "raw": c["raw"],
            "location": c["location"],
        }
        if not file_ref:
            verdict.update(
                {
                    "verdict": "FAIL",
                    "source_basis": "verify_internal_refs: no file reference",
                    "suggested_fix": "Citation type 5.1 must include a file name",
                }
            )
            results.append(verdict)
            continue
        target_path = project_path / file_ref
        if not target_path.exists():
            verdict.update(
                {
                    "verdict": "FAIL",
                    "source_basis": f"verify_internal_refs: file not found at {target_path}",
                    "suggested_fix": f"Upload {file_ref} to the project knowledge folder, or correct the citation",
                }
            )
            results.append(verdict)
            continue
        if section_ref:
            headings = find_headings(target_path)
            if not heading_matches(section_ref, headings):
                verdict.update(
                    {
                        "verdict": "FAIL",
                        "source_basis": f"verify_internal_refs: section '{section_ref}' not found in {file_ref}",
                        "suggested_fix": f"Verify the section name; available headings: {sorted(headings)[:5]}...",
                    }
                )
                results.append(verdict)
                continue
        verdict.update(
            {
                "verdict": "PASS",
                "source_basis": "verify_internal_refs: file and section confirmed",
                "suggested_fix": None,
            }
        )
        results.append(verdict)
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--citations", required=True, type=Path)
    p.add_argument("--project-path", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    if not args.citations.exists():
        print(f"ERROR: Citations file not found: {args.citations}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(args.citations.read_text(encoding="utf-8"))
    citations = data["citations"]

    # Default project_path: <document_dir>/knowledge/
    if args.project_path is None:
        document = Path(data.get("document", "."))
        args.project_path = document.parent / "knowledge"

    if not args.project_path.exists():
        print(
            f"WARNING: Project knowledge path not found: {args.project_path}",
            file=sys.stderr,
        )
        # Mark all 5.1 citations as FAIL due to missing project folder
        results = [
            {
                "citation_id": c["citation_id"],
                "type": c["type"],
                "raw": c["raw"],
                "location": c["location"],
                "verdict": "FAIL",
                "source_basis": f"verify_internal_refs: project knowledge folder missing at {args.project_path}",
                "suggested_fix": "Upload the project knowledge bundle",
            }
            for c in citations
            if c["type"] == "5.1"
        ]
    else:
        results = verify(citations, args.project_path)

    out = json.dumps(
        {"check": "verify_internal_refs", "results": results}, indent=2
    )
    if args.output:
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
