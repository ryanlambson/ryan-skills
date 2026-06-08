---
name: lla-citation-checker
description: >
  HTS pre-delivery citation and reference verification. Use this skill
  whenever Ryan or the HTS team needs to audit citations in any LLA draft
  before output is presented — SoRPEs, PIAs, LPoMs, ETAs, condition
  variation submissions, objection responses, NCAT reviews. Stage 1 of the
  two-stage pre-delivery gate (Stage 2 is lla-compliance-checker). Verifies
  every legislative citation (Liquor Act 2007 NSW, Liquor Control Act 1988
  WA), regulation, ILGA Guideline, Director's Policy, case citation,
  planning instrument (LEP/DCP/LPS/LPP) and data citation against its
  source. Flags uncited assertions. Applies the stale-citations registry
  (e.g., NSW s.48 → s.72I). Trigger phrases: "check the citations",
  "audit references", "citation gate", "run the citation checker", "Stage
  1 pre-delivery check", "verify references". Jurisdiction-agnostic —
  works for both WA and NSW. Do NOT trigger for non-LLA documents, style
  or formatting checks (route to lla-compliance-checker), plagiarism
  detection, or legal advice.
license: Proprietary. HTS internal use only.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: "1.0"
  role: pre-delivery-stage-1
  jurisdiction: agnostic
  set_skill: true
---

# LLA Citation Checker — HTS Pre-Delivery Stage 1

This is a **set skill** — a permanent member of the HTS LLA toolkit, included in every LLA project regardless of jurisdiction. It exists for one reason: every HTS work product that lodges with a regulator must have every citation verified against its source before it ships. Doing that by hand is slow and error-prone. This skill does it deterministically.

## Authoring Entity Lock

Outputs of this skill — the audit reports it produces — feed back into the calling LLA drafter (or to the HTS team member running the audit). The skill itself does not modify drafts. It reports findings.

All work this skill supports is on behalf of:

**Hospitality Total Services (Aus) Pty Ltd (HTS)**
Planning & Liquor Licensing Consultancy — Office 2, 48 Kishorn Road, Applecross WA 6153

---

## 1. Purpose and Position in the LLA Family

`lla-citation-checker` is **Stage 1 of the two-stage pre-delivery gate**. Every drafting skill in the LLA family routes its output through this skill before it goes to Stage 2 (`lla-compliance-checker`) for broader pre-delivery checks. Only after both stages pass does the output reach formatting (`lla-document-builder`) and delivery.

**Position in the pipeline:**

```
LLA drafter (lla-gpt, lla-gpt-nsw, lla-pia-drafter, lla-harm-minimisation, lla-precedent-advisor)
    │
    ▼ produces draft
    │
Stage 1: lla-citation-checker  ← this skill
    │
    ▼ if all PASS or WARN-only
    │
Stage 2: lla-compliance-checker
    │
    ▼ if all PASS
    │
lla-document-builder → final docx → deliver
```

**Why "set skill":** Citation discipline is jurisdiction-agnostic. The same verification logic applies to a WA PIA citing the Liquor Control Act 1988 and a NSW SoRPE citing the Liquor Act 2007. Building this once, installing it once, and routing all LLA drafters through it is the right architecture.

---

## 2. MANDATORY FIRST STEPS

Before processing any draft, read these three reference files in order. They are the source of truth for what a valid citation looks like, which citations are known stale, and which authorities are valid for which jurisdiction.

```bash
cat references/citation-format-spec.md
cat references/stale-citations-registry.md
cat references/jurisdiction-citation-map.md
```

Then confirm:

- Input document path and format (`.md` or `.docx`)
- Jurisdiction of the draft (auto-detect from project context if possible: a project whose knowledge bundle contains `LEGISLATION_LiquorAct2007_NSW_HOTEL.md` is NSW; a project containing `LEGISLATION_LCA1988_MASTER_INDEXED.md` is WA)
- The active project's knowledge folder path (default: `<project_root>/knowledge/`)

---

## 3. Inputs

| Input | Required | Default | Purpose |
|---|---|---|---|
| `--input PATH` | Yes | — | Path to the draft (.md or .docx) |
| `--jurisdiction WA\|NSW` | No | Auto-detect from project context | Forces jurisdiction for cross-state checks |
| `--project-knowledge-path PATH` | No | `<project_root>/knowledge/` | Override the default project knowledge folder |
| `--live` | No | Off | Enables live web verification against legislation portals (slow; opt-in) |
| `--format md\|json` | No | `md` | Audit report format. `md` for in-chat use; `json` for skill-to-skill hand-off |
| `--output PATH` | No | stdout | Where to write the audit report |

---

## 4. Workflow (six steps)

Run the six steps in order. Each step is implemented as a bundled script. The cognitive layer (this SKILL.md) orchestrates them.

### Step 1 — Ingest and extract citations

```bash
python -m scripts.extract_citations --input <PATH> > extracted.json
```

Reads the draft, extracts every citation, and emits a JSON list. Each entry: citation text, type, line number / heading location, and (where applicable) inferred source identifier.

### Step 2 — Verify internal project knowledge references

```bash
python -m scripts.verify_internal_refs --citations extracted.json \
  --project-path <PROJECT_KNOWLEDGE_PATH> > internal_refs.json
```

For each citation in the form `(Source: FILE.md, Section X)`, checks that the file exists and contains the cited section heading. FAIL if missing.

### Step 3 — Apply the stale-citations registry

```bash
python -m scripts.apply_stale_registry --citations extracted.json \
  --registry references/stale-citations-registry.md > stale_flags.json
```

Cross-checks every citation against the known-stale registry. Hits become WARN (with the current section number suggested as the fix) or FAIL (if the cited authority has been outright repealed).

### Step 4 — Detect uncited assertions

```bash
python -m scripts.detect_uncited_claims --input <PATH> > uncited.json
```

Heuristic detector for factual claims — numeric values, named authorities, regulator names, Act and section references — appearing without a nearby citation marker. Each detection becomes a WARN.

### Step 5 — (Optional) Live verification

```bash
python -m scripts.verify_legislation_live --citations extracted.json \
  --jurisdiction <WA|NSW> > live_verify.json
```

Only runs if `--live` was passed. Web-fetches the relevant legislation portal (`legislation.nsw.gov.au` or `legislation.wa.gov.au`) and confirms the cited section exists. Slow (~1-3 seconds per citation). Reserve for immediately before lodgement.

### Step 6 — Compose the audit report

```bash
python -m scripts.audit_report \
  --internal internal_refs.json \
  --stale stale_flags.json \
  --uncited uncited.json \
  --live live_verify.json \
  --format <md|json> > audit_report.<ext>
```

Combines all upstream JSON into a single structured audit report.

---

## 5. Citation Categories and Verification Logic

The extractor categorises every citation by type. Each type has its own verification logic. The categories below are what the skill recognises out of the box. New types can be added by extending `references/citation-format-spec.md`.

### 5.1 Project knowledge file references

Format: `(Source: FILE.md, Section X)` or `(Source: FILE.md)`. Verification: the file exists at `<project_knowledge_path>/FILE.md` and (if a section is named) the file contains a heading matching the section reference. Otherwise FAIL.

### 5.2 Legislation (NSW + WA)

Examples:
- `*Liquor Act 2007* (NSW), s.48(3)`
- `*Liquor Control Act 1988* (WA), s.38(4)`

Verification: format check; cross-check against stale registry (currently flags NSW s.48 → possibly s.72I); if `--live`, fetch legislation portal to confirm section exists. WARN if the section is flagged stale; FAIL if outright repealed.

### 5.3 Regulations (NSW + WA)

Examples:
- `*Liquor Regulation 2018* (NSW), cl.27`
- `*Liquor Control Regulations 1989* (WA), reg.7`

Same logic as 5.2.

### 5.4 ILGA Guidelines (NSW only)

Example: `ILGA Guideline 6 — Consideration of overall impact under section 48(3) of the Liquor Act 2007 (10 March 2025), paragraph 1.1`

Verification: format check (must include guideline number, title, and publication date); currency check (date ≤12 months old, else WARN with recommendation to refresh); jurisdiction-lock (FAIL if cited in a WA draft).

### 5.5 Director's Policies (WA only)

Example: `Director's Policy (Guidance) — Public Interest Assessment, paragraph 4.2`

Verification: format check; jurisdiction-lock (FAIL if cited in a NSW draft); ensure labelled "Guidance" — not law.

### 5.6 L&GNSW operational guidance (NSW only)

Example: `L&GNSW, Hotel licence page (nsw.gov.au), Trading hours table`

Verification: format check; jurisdiction-lock (FAIL if cited in a WA draft); flag for manual verification (these pages update without version control).

### 5.7 Case law

Examples:
- `Carnegies (LC28/2015)` — WA only
- `ILGA Decision: Bar 333 Sydney (17 September 2025)` — NSW only

Verification: format check; jurisdiction map (Carnegies = WA only, Sand Volley = WA only, Pilbara s.64 = WA only, Liquorland Karrinyup = WA only; ILGA decisions = NSW only, NCAT decisions = NSW only). FAIL if a case is cited in the wrong jurisdiction.

### 5.8 Planning instruments (LEP / DCP / LPS / LPP)

Examples:
- `Sydney LEP 2012, clause 4.3`
- `Shire of Augusta Margaret River LPS No. 1 (AMD 76)`

Verification: format check; LGA-match against the project's locked locality (FAIL if a different LGA's instrument is cited).

### 5.9 Data citations

Examples:
- `BOCSAR Crime Tool, Sydney LGA, alcohol-related assault rate 2024–25`
- `ABS Census 2021 Quickstats, Sydney SA2`

Verification: format check (must include source, geography, year/period); currency check (period within the last 5 years, else WARN).

### 5.10 Web URLs

Verification: format check (well-formed URL); if `--live`, HEAD request to confirm the URL responds.

---

## 6. Verdict Levels

Every extracted citation receives one of three verdicts.

| Verdict | Meaning | Effect on delivery |
|---|---|---|
| **PASS** | Citation verified; no issues | Silent |
| **WARN** | Citation valid but stale, low-confidence, or requires manual Type-4 verification ("does the cited source actually say what we claim?") | Recorded in the report; calling drafter may proceed at their discretion |
| **FAIL** | Citation broken — wrong jurisdiction, non-existent section, missing source, uncited assertion in a load-bearing position, repealed authority | Delivery blocked; calling drafter must fix and re-run |

**Type 4 verification is partly cognitive.** A pure script cannot judge whether a quoted passage of legislation is a faithful quotation of the source — it requires reading both texts and comparing. This skill flags Type 4 as "manual verification required" in the audit report rather than auto-PASSing. The calling drafter (or HTS reviewer) is responsible for the read-and-compare step.

---

## 7. Audit Report Format

### Default — Markdown (for in-chat audit runs)

```markdown
# Citation Audit Report — <document-name>

**Jurisdiction:** <NSW|WA>
**Document:** <path>
**Date:** <ISO timestamp>
**Total citations extracted:** <N>
**Verdict summary:** <P> PASS / <W> WARN / <F> FAIL
**Disposition:** <Cleared for Stage 2 | Blocked — fix FAILs and re-run>

## FAILs (must fix before delivery)
- [<location>] <citation text> — <reason> — Suggested fix: <fix>

## WARNs (review before delivery)
- [<location>] <citation text> — <reason> — Suggested action: <action>

## Manual verification required
- [<location>] <citation text> — Verify the cited source actually says <claim>

## PASSes (silent — for the record)
- <N> citations passed all automated checks
```

### Skill-to-skill hand-off — JSON

```json
{
  "document": "<path>",
  "jurisdiction": "<NSW|WA>",
  "timestamp": "<ISO timestamp>",
  "summary": {"pass": N, "warn": N, "fail": N},
  "disposition": "cleared_for_stage_2 | blocked",
  "citations": [
    {
      "citation_id": "c-001",
      "type": "<5.1..5.10>",
      "location": {"line": N, "heading": "<text>"},
      "verdict": "PASS|WARN|FAIL",
      "source_basis": "<which script + which check>",
      "suggested_fix": "<fix text if FAIL/WARN>"
    }
  ]
}
```

The JSON form is what `lla-compliance-checker` ingests when both gates run as part of an automated pipeline.

---

## 8. Bundled Scripts

All scripts live in `scripts/`. All are Python 3, standard library plus `python-docx`. Each begins with `#!/usr/bin/env python3` and is executable.

| Script | One-line purpose |
|---|---|
| `scripts/extract_citations.py` | Regex-based citation extractor; reads .md or .docx; emits structured JSON list |
| `scripts/verify_internal_refs.py` | Cross-checks project knowledge file references — file existence + section heading presence |
| `scripts/apply_stale_registry.py` | Cross-checks extracted citations against the stale-citations registry |
| `scripts/verify_legislation_live.py` | (`--live` mode only) Web-fetches legislation portals to verify section existence |
| `scripts/detect_uncited_claims.py` | Heuristic detector for factual claims appearing without a nearby citation marker |
| `scripts/audit_report.py` | Composes the structured audit report from upstream JSON |

Each script's full invocation pattern, inputs, outputs and exit codes are documented in `references/scripts-guide.md`.

---

## 9. Reference Files

| File | Purpose |
|---|---|
| `references/citation-format-spec.md` | The HTS citation format standard — what a valid citation looks like per type |
| `references/stale-citations-registry.md` | Known stale citations across NSW and WA (seeded with NSW s.48 → s.72I) |
| `references/jurisdiction-citation-map.md` | Authority validity matrix per jurisdiction (Carnegies = WA only; ILGA decisions = NSW only; etc.) |
| `references/scripts-guide.md` | Full invocation patterns, inputs, outputs and exit codes for the six bundled scripts |

---

## 10. Examples

### Example 1 — In-chat citation audit on a SoRPE draft

```
User: "Run the citation checker on the Waldorf SoRPE draft."

Claude (invoking lla-citation-checker):
1. Read references/citation-format-spec.md, stale-citations-registry.md, jurisdiction-citation-map.md
2. Detect jurisdiction from project context (NSW — knowledge folder contains LEGISLATION_LiquorAct2007_NSW_HOTEL.md)
3. Run the six-step pipeline
4. Emit the Markdown audit report
5. Report disposition to user: "Cleared for Stage 2" or "Blocked — N FAILs to fix"
```

### Example 2 — Stage 1 hand-off from `lla-gpt-nsw`

```
lla-gpt-nsw has produced a SoRPE draft. Its pre-delivery checklist calls Stage 1.

Internal invocation:
python -m scripts.extract_citations --input <draft> > /tmp/extracted.json
python -m scripts.verify_internal_refs --citations /tmp/extracted.json --project-path <path> > /tmp/internal.json
python -m scripts.apply_stale_registry --citations /tmp/extracted.json > /tmp/stale.json
python -m scripts.detect_uncited_claims --input <draft> > /tmp/uncited.json
python -m scripts.audit_report --internal /tmp/internal.json --stale /tmp/stale.json --uncited /tmp/uncited.json --format json > /tmp/audit.json

On clear disposition: hand /tmp/audit.json to lla-compliance-checker (Stage 2).
On blocked disposition: return to lla-gpt-nsw with the audit report; drafter must fix.
```

### Example 3 — Immediately before lodgement, with `--live`

```
User: "About to lodge the Waldorf SoRPE — run the full citation check with --live."

Same six-step pipeline, but Step 5 runs:
python -m scripts.verify_legislation_live --citations /tmp/extracted.json --jurisdiction NSW > /tmp/live.json

This adds ~30-90 seconds for a 30-citation SoRPE but confirms every cited section actually exists in the current consolidation of the Liquor Act 2007 (NSW). Catches the s.48 → s.72I question definitively.
```

---

## 11. Failure Modes and Recovery

| Failure | Recovery |
|---|---|
| Missing project knowledge file | Instruct user to upload from the canonical bundle; refuse to PASS internal references until uploaded |
| Live web check fails (network down) | Degrade to non-live mode; record an explicit warning in the audit report; do not auto-PASS items that needed live verification |
| Unrecognised citation format | WARN with a suggested HTS-format fix; do not silently ignore |
| Empty draft / no citations found | Return informational report ("No citations found — confirm this is intended"); no FAIL |
| Stale-registry file malformed | Block the run; report the malformation; the registry is the source of truth |
| Project knowledge folder not at default path | Use `--project-knowledge-path` override |

---

## 12. Quality Self-Check

Before emitting the audit report, confirm:

- [ ] All six scripts ran (or were intentionally skipped, e.g., `verify_legislation_live` without `--live`)
- [ ] Audit report has a verdict for every extracted citation
- [ ] No "TBD" or placeholder values in the report
- [ ] JSON output (if requested) validates as JSON
- [ ] Disposition is one of {cleared_for_stage_2, blocked} — never ambiguous

---

## 13. Pre-Delivery Hand-Off

- **On all-PASS or WARN-only:** Emit the audit report. If invoked by a sister LLA skill, return the JSON form with `"disposition": "cleared_for_stage_2"`. The calling skill then forwards to `lla-compliance-checker`.
- **On any FAIL:** Emit the audit report with `"disposition": "blocked"`. Return to the calling drafter. Refuse to advance to Stage 2 until FAILs are fixed and the gate re-runs cleanly.
- **Always:** Save the audit report to `<project_root>/audit-reports/<timestamp>-<doc-name>.<ext>` for the project audit trail.

---

## 14. Enforcement and Distribution

This is a **set skill** — installed permanently as part of the HTS LLA toolkit. Jurisdiction-agnostic. Every LLA project, regardless of state, inherits this gate. New jurisdiction skills (e.g., `lla-gpt-vic` if HTS expands) inherit the Stage 1 dependency by design.

All outputs prepared by Hospitality Total Services (Aus) Pty Ltd.

**System Version:** 1.0 — HTS Pre-Delivery Stage 1
**Last Updated:** 21 May 2026
**Sibling Skills:** lla-gpt (WA master), lla-gpt-nsw (NSW master), lla-pia-drafter, lla-harm-minimisation, lla-precedent-advisor, lla-document-builder (jurisdiction-agnostic formatter), lla-compliance-checker (Stage 2)
