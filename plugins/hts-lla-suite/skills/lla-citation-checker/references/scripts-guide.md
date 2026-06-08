# Scripts Guide — lla-citation-checker

**Status:** Operational reference
**Last updated:** 21 May 2026

This file documents the full invocation pattern, inputs, outputs and exit codes for each bundled script in the lla-citation-checker skill. The cognitive layer in SKILL.md orchestrates these scripts; this guide is the operational reference for debugging or invoking individual scripts ad hoc.

All scripts are Python 3, standard library + `python-docx` for `.docx` ingestion. All begin with `#!/usr/bin/env python3` and are executable.

---

## Running the full pipeline end-to-end

```bash
DRAFT="path/to/draft.md"        # or .docx
PROJECT="path/to/project_root"
JURIS="NSW"                     # or WA — auto-detect can also be left to the skill

python -m scripts.extract_citations \
  --input "$DRAFT" \
  --output /tmp/extracted.json

python -m scripts.verify_internal_refs \
  --citations /tmp/extracted.json \
  --project-path "$PROJECT/knowledge" \
  --output /tmp/internal.json

python -m scripts.apply_stale_registry \
  --citations /tmp/extracted.json \
  --output /tmp/stale.json

python -m scripts.detect_uncited_claims \
  --input "$DRAFT" \
  --output /tmp/uncited.json

# Optional: live legislation verification
python -m scripts.verify_legislation_live \
  --citations /tmp/extracted.json \
  --jurisdiction "$JURIS" \
  --output /tmp/live.json

python -m scripts.audit_report \
  --extracted /tmp/extracted.json \
  --internal /tmp/internal.json \
  --stale /tmp/stale.json \
  --uncited /tmp/uncited.json \
  --live /tmp/live.json \
  --jurisdiction "$JURIS" \
  --format md \
  --output /tmp/audit_report.md
```

---

## scripts/extract_citations.py

**Purpose:** Regex-based citation extractor.

**Inputs:**
- `--input PATH` (required) — draft document (.md, .txt, .docx)
- `--output PATH` (optional) — output JSON path (default: stdout)

**Outputs:**
```json
{
  "document": "path/to/draft.md",
  "citations": [
    {
      "citation_id": "c-001",
      "type": "5.2",
      "raw": "*Liquor Act 2007* (NSW), s.48(3)",
      "location": {"line": 42, "heading": "Section 7"},
      "details": {"act": "Liquor Act 2007", "state": "NSW", "section": "48(3)"}
    }
  ]
}
```

**Exit codes:**
- 0 — OK
- 1 — Input file unreadable
- 2 — Parse error

---

## scripts/verify_internal_refs.py

**Purpose:** Cross-checks project knowledge file references (type 5.1).

**Inputs:**
- `--citations PATH` (required) — extract_citations.py output
- `--project-path PATH` (optional) — project knowledge folder (default: `<document_dir>/knowledge/`)
- `--output PATH` (optional) — output JSON path (default: stdout)

**Outputs:**
```json
{
  "check": "verify_internal_refs",
  "results": [
    {
      "citation_id": "c-001",
      "type": "5.1",
      "raw": "(Source: KNOWLEDGE_INDEX_NSW.md, Section 4)",
      "location": {"line": 12, "heading": "Authority Hierarchy"},
      "verdict": "PASS",
      "source_basis": "verify_internal_refs: file and section confirmed",
      "suggested_fix": null
    }
  ]
}
```

**Exit codes:**
- 0 — OK
- 1 — Path issue (citations file or project folder not found)

---

## scripts/apply_stale_registry.py

**Purpose:** Cross-checks citations against the known-stale registry.

**Inputs:**
- `--citations PATH` (required) — extract_citations.py output
- `--registry PATH` (optional) — defaults to `references/stale-citations-registry.md` relative to the script
- `--output PATH` (optional)

**Outputs:**
Per-citation flag JSON — WARN for STALE-RENUMBERED/SUPERSEDED, FAIL for STALE-REPEALED.

**Exit codes:**
- 0 — OK
- 1 — Registry malformed (parse failure)

---

## scripts/verify_legislation_live.py

**Purpose:** Live legislation portal verification (`--live` mode only).

**Inputs:**
- `--citations PATH` (required)
- `--jurisdiction WA|NSW` (optional — else inferred per citation)
- `--output PATH` (optional)

**Network endpoints:**
- NSW: `https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-2007-090`
- NSW Reg: `https://legislation.nsw.gov.au/view/html/inforce/current/sl-2018-0473`
- WA: `https://www.legislation.wa.gov.au/legislation/statutes.nsf/main_mrtitle_564_homepage.html`

**Exit codes:**
- 0 — OK (all live checks succeeded)
- 1 — Network error (all live checks failed)
- 2 — Partial (some live checks failed or returned WARN)

**Latency:** ~1–3 seconds per unique legislation URL (responses are cached within the run).

---

## scripts/detect_uncited_claims.py

**Purpose:** Heuristic detector for factual claims appearing without a nearby citation marker.

**Inputs:**
- `--input PATH` (required)
- `--output PATH` (optional)

**Heuristics applied:**
The script flags paragraphs containing any of these claim triggers AND lacking any citation marker:
- Percentages (`19%`, `19 per cent`)
- Large numbers (`1,300+`, `54857`)
- Section references (`section 48`, `s.48(3)`, `clause 27`)
- Named authorities (ILGA, BOCSAR, L&GNSW, ABS, NCAT, Carnegies)
- Guideline references (`Guideline 6`)
- Year ranges (`between 2008 and 2018`)

Citation markers that count:
- `(Source:` (any HTS internal reference)
- `*[Statute] Year* (STATE)` (legislation citation)
- `ILGA Guideline N`
- `BOCSAR [...] [year]`
- `ABS [...] [year]`
- URLs

Exempt structures:
- Headings (start with `#`)
- Single-bullet paragraphs (start with `-`, `*`, `•`)
- Table rows (start with `|`)

**Exit codes:**
- 0 — OK
- 1 — Input issue

---

## scripts/audit_report.py

**Purpose:** Composes the final audit report from upstream JSON.

**Inputs:**
- `--extracted PATH` (required) — extract_citations.py output (the citation baseline)
- `--internal PATH` (optional) — verify_internal_refs.py output
- `--stale PATH` (optional) — apply_stale_registry.py output
- `--uncited PATH` (optional) — detect_uncited_claims.py output
- `--live PATH` (optional) — verify_legislation_live.py output
- `--format md|json` (optional, default: md)
- `--jurisdiction WA|NSW` (optional, default: unknown — recorded in the report)
- `--output PATH` (optional)

**Verdict merging logic:**
Every citation in the extracted baseline gets the most severe verdict across all upstream checks (FAIL > WARN > PASS). If no checks applied to a given citation, the verdict defaults to PASS with a note "no checks applied to this type".

**Disposition:**
- `cleared_for_stage_2` if no FAILs
- `blocked` if any FAILs

**Exit codes:**
- 0 — OK (regardless of audit verdict — the verdict is in the report)
- 1 — Input issue

---

## Debugging tips

- **Run scripts individually** when troubleshooting. Each script writes a clean JSON contract; you can inspect each intermediate output.
- **`extract_citations.py` is the bottleneck for new citation types.** If a citation isn't being recognised, the issue is almost always a missing or incorrect regex pattern in `PATTERNS`. Add a new pattern in `extract_citations.py` AND a row in `references/citation-format-spec.md`.
- **The stale registry is the source of truth.** If a stale citation isn't being flagged, the registry entry is missing or its pattern doesn't match the citation's natural-language form. Use a substring that appears verbatim in the citation as the registry pattern.
- **Live verification is brittle.** Legislation portals change URL patterns and HTML structure without notice. If `verify_legislation_live.py` starts returning false FAILs, check whether the portal endpoint has moved.

---

## Security notes

All scripts:
- Read only from the input file path and the bundled references/ files
- Write only to the specified `--output` path (or stdout)
- Do NOT execute shell commands, fetch remote code, or invoke `eval`/`exec`
- The only network egress is in `verify_legislation_live.py` (gated by `--live`)
- No external API keys, tokens, or credentials required
