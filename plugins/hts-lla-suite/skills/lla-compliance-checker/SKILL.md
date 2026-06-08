---
name: lla-compliance-checker
description: >
  HTS quality assurance and compliance checker for LLA PIA sections and
  complete documents. Stage 2 of the two-stage HTS pre-delivery gate (Stage 1
  is lla-citation-checker). Use this skill whenever the user wants to review,
  check, audit, or quality-assure any drafted PIA, SoRPE, LPoM, ETA, objection
  response, or other LLA work product before lodgement. Also trigger for
  requests to "check this section", "review before sending", "QA this",
  "is this ready to lodge", "compliance check", "pre-delivery review", or any
  instruction to verify that content meets HTS and regulatory standards.
  Jurisdiction-aware — handles both WA (Carnegies four-step, Liquor Control
  Act 1988) and NSW (Guideline 6 five-step, Liquor Act 2007) drafts. Returns
  a structured pass/fail report with specific issues flagged for correction.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: quality-assurance
---

# LLA Compliance Checker — Pre-Delivery Quality Assurance

## Purpose

This skill runs the complete HTS quality assurance protocol against drafted
PIA sections or complete documents before delivery or lodgement. It produces
a structured pass/fail report identifying every issue that must be resolved.

---

## Pre-Delivery Gate Architecture (MANDATORY)

HTS work products pass through a two-stage pre-delivery gate before any output
is presented to the client or lodged. This skill is **Stage 2**. Stage 1 must
have run cleanly first.

```
Draft → Stage 1 (lla-citation-checker) → Stage 2 (this skill) → Delivery
```

**Stage 1 — lla-citation-checker.** Verifies every citation in the draft
against its source: legislation, regulations, ILGA Guidelines, Director's
Policies, case law, planning instruments, data citations, URLs. Flags
uncited assertions and stale citations (e.g., NSW s.48 → s.72I).
Jurisdiction-agnostic.

**Stage 2 — lla-compliance-checker (this skill).** Runs the HTS quality
assurance checklists. Confirms source-of-truth discipline, authority
hierarchy, locality lock, content quality, harm assessment framework,
legislative framework completeness, drafting standards, document structure,
and common error prevention. Jurisdiction-aware.

**Order matters.** If Stage 1 reports any FAILs, Stage 2 will not produce a
"READY FOR LODGEMENT: YES" verdict regardless of compliance results — the
citation gate must clear first.

---

## How to Use

Paste or reference the section or document to be checked, then specify:
- Which section(s) to check (or "full document")
- The licence type and locked LGA for this application
- **The jurisdiction** (WA or NSW) — determines which framework applies in
  Checklists 3, 6, 7, and 10
- **The Stage 1 result** (PASS / WARN / FAIL) from lla-citation-checker. If
  not run yet, halt and run Stage 1 first.

The checker will run all applicable checklists and return a report.

---

## Checklist 1 — Source-of-Truth Compliance

```
□ All content sourced from project files only
□ No general knowledge or memory-based content present
□ No content from other LGA projects or prior applications
□ No assumptions presented as facts
□ If information was unavailable, it was flagged — not filled in
```

---

## Checklist 2 — Citation Discipline

```
□ Every factual claim cites a specific project file and section
□ Citation format: (Source: FILE_NAME.md, Section/Heading)
□ No placeholder citations (e.g., "[source]", "see above")
□ No uncited assertions
□ Statistical or data claims cite specific source document
□ All legislative quotations cite Act/Regulation section number
```

---

## Checklist 3 — Authority Hierarchy

```
□ Legislation quoted verbatim — no paraphrasing of statutory text
□ Case law cited for methodology only — not as binding authority
□ Current gazetted planning scheme used — not draft scheme
□ Draft scheme (if referenced) explicitly flagged as "DRAFT — NOT YET GAZETTED"
□ Knowledge modules cited as supporting evidence only — not as authority
□ Knowledge modules never used to override planning instruments or legislation
```

**WA drafts only:**
```
□ Director's Policies labelled as "(Guidance)" — not cited as law
□ Carnegies and other WA cases used for methodology only
```

**NSW drafts only:**
```
□ ILGA Guidelines cited with publication date — flagged WARN if >12 months old
□ L&GNSW operational pages labelled as guidance — not cited as law
□ No WA authorities cited (Carnegies, Director's Policy, WA LPS/LPP) — these
  are FAILs in NSW drafts (Stage 1 enforces this; Stage 2 reconfirms)
```

---

## Checklist 4 — Locality Lock

```
□ All planning references are from the locked LGA only
□ No planning content from any other LGA present
□ Suburb, zone, and centre descriptions match locked LGA
□ No generic or assumed planning provisions
□ Activity centre references match LGA's actual centre hierarchy
```

---

## Checklist 5 — Content Quality

```
□ Venue-specific details throughout — no generic statements
□ All [INSERT] placeholder text has been replaced
□ Venue trading name consistent throughout
□ Applicant legal entity name consistent throughout
□ All attachment references are numbered and consistent
□ Approved Manager credentials are accurate and complete
□ Trading hours stated are consistent across all sections
□ Patron capacity consistent across all sections
□ Floor plan references match uploaded floor plan
```

---

## Checklist 6 — Harm Assessment (Section 7 specific)

**WA drafts — Carnegies four-step framework:**
```
□ Carnegies four-step framework applied:
   □ Step 1: Existing harm in locality identified
   □ Step 2: Likely harm from this application identified
   □ Step 3: Comparison made between likely and existing harm
   □ Step 4: Harm weighed against public interest benefits
□ Every risk identified concludes with a specific mitigation measure
□ Mitigation measures are venue-specific — not generic
□ Evidence for harm claims sourced from KNOWLEDGE files (cited correctly)
□ Source cited: Case_Precedent_Compendium.md — Carnegies LC28/2015
```

**NSW drafts — Guideline 6 / overall-impact framework:**
```
□ HTS five-step Guideline 6 framework applied:
   □ Step 1: Locality characterised (community wellbeing baseline)
   □ Step 2: Likely harm assessed against ILGA Guideline 6 criteria
   □ Step 3: Comparison made (cumulative impact context)
   □ Step 4: Public interest benefits identified
   □ Step 5: Overall-impact conclusion under s.48(3) (verify s.48 vs s.72I)
□ Every risk identified concludes with a specific mitigation measure
□ Mitigation measures are venue-specific — not generic
□ Evidence for harm claims sourced from project knowledge files (cited correctly)
□ Source cited: ILGA Guideline 6 with publication date
□ NSW BOCSAR / NSW Health data used for locality harm baseline (not WA data)
□ Sydney CBD Entertainment Precinct conditions addressed if applicable
```

---

## Checklist 7 — Legislative Framework

**WA drafts (Liquor Control Act 1988):**
```
□ Correct section of the Act cited for this licence type
□ Statutory text quoted verbatim (not summarised or paraphrased)
□ Section 38(4)(a)(b)(c)(ca) addressed where applicable
□ s.36B(4) provisions correctly applied (packaged liquor only)
□ Section 39 certificate mentioned if applicable
□ Objects of the Act addressed (s.5)
```

**NSW drafts (Liquor Act 2007):**
```
□ Correct section of the Act cited for this licence type
□ Statutory text quoted verbatim (not summarised or paraphrased)
□ Overall-impact test under s.48(3) addressed — verify whether s.48 remains
  current or has been renumbered to s.72I under the Dec 2025 Vibrancy
  Reforms consolidation
□ Full Notification Class D (hotel applications) addressed
□ SoRPE (Statement of Risks and Potential Effects) lodged — replaced CIS
  from 1 July 2024
□ Sydney CBD Entertainment Precinct retained conditions addressed if
  applicable (24/7 incident register, crime-scene preservation, OMCG
  exclusion)
□ Objects of the Act addressed (s.3)
```

---

## Checklist 8 — Drafting Standards

```
□ Formal, regulatory, third-person tone throughout
□ No conversational language or casual phrasing
□ No speculative statements ("may", "could" — only where legally appropriate)
□ No persuasive language without evidence support
□ "It is submitted that…" construction used appropriately
□ Document is lodgement-ready without further research or editing
```

---

## Checklist 9 — Document Structure

```
□ Section numbering is sequential and correct
□ Headings match the PIA template structure
□ Sub-headings are consistent with template
□ Attachments list is complete and numbered
□ Table of Contents (if present) matches actual headings
□ No orphaned headings (heading without content)
```

---

## Checklist 10 — Common Error Prevention

These are the most frequent errors in HTS PIAs. Check each explicitly:

```
□ NOT PRESENT: LPS version confusion — draft scheme provisions cited as current law
□ NOT PRESENT: Cross-LGA bleed — planning content from wrong LGA
□ NOT PRESENT: Director's Policy cited as legal requirement
□ NOT PRESENT: Knowledge module elevated to authority status
□ NOT PRESENT: Risk identified without mitigation conclusion
□ NOT PRESENT: s.36B(4) mischaracterised (packaged liquor applications)
□ NOT PRESENT: Section 39 certificate omitted from process timeline
□ NOT PRESENT: DA assessment periods understated (referral agency timeframes)
□ NOT PRESENT: Paraphrased legislation (must be verbatim)
□ NOT PRESENT: Generic harm statements without locality grounding
```

**Cross-jurisdiction errors (Stage 1 also catches these, but reconfirm):**
```
□ NOT PRESENT: WA authority cited in NSW draft (Carnegies, Director's Policy,
  WA LPS/LPP, Liquor Control Act 1988)
□ NOT PRESENT: NSW authority cited in WA draft (ILGA Guideline, NCAT decision,
  L&GNSW page, NSW LEP/DCP, Liquor Act 2007)
□ NOT PRESENT: Stale citation un-flagged (e.g., NSW s.48 without verification
  against the Dec 2025 consolidation that may have moved it to s.72I)
□ NOT PRESENT: ILGA Guideline cited without publication date
```

---

## Checklist 11 — Stage 1 Confirmation (NEW in v1.1)

Confirm Stage 1 (lla-citation-checker) ran cleanly before producing a "READY
FOR LODGEMENT: YES" verdict.

```
□ Stage 1 audit report exists for this draft
□ Stage 1 disposition is "cleared_for_stage_2" (no FAILs outstanding)
□ Any Stage 1 WARNs have been reviewed and either resolved or accepted on the
  record (e.g., ILGA Guideline 6 publication date acknowledged as current)
□ Stage 1 jurisdiction setting matches Stage 2 jurisdiction setting
□ Any uncited assertions flagged by Stage 1 have been remedied
```

If any of the above are absent, halt Stage 2 and run Stage 1 first.

---

## Report Format

Produce the compliance report in this format:

```
COMPLIANCE CHECK REPORT (Stage 2)
==================================
Document: [Section/Document name]
Application: [Trading name] — [Licence type]
Jurisdiction: WA / NSW
LGA: [Locked LGA]
Checked: [Date]

Stage 1 (lla-citation-checker) status: PASS / WARN / FAIL / NOT RUN
  - If NOT RUN: HALT — run Stage 1 first
  - If FAIL: report shows compliance results but READY FOR LODGEMENT = NO

OVERALL STATUS: PASS / FAIL / PASS WITH MINOR ISSUES

CHECKLIST RESULTS:
------------------
[For each checklist, list: PASS / FAIL / N/A]

ISSUES REQUIRING CORRECTION:
-----------------------------
[For each failed item:]
  Issue: [Specific problem]
  Location: [Where in the document]
  Required action: [What must be done to resolve]

MINOR OBSERVATIONS (non-blocking):
-----------------------------------
[Any quality observations that do not prevent lodgement but should be noted]

READY FOR LODGEMENT: YES / NO
  - YES requires: Stage 1 PASS + Stage 2 PASS (or PASS WITH MINOR ISSUES)
```

---

## Severity Classification

**Blocking (must fix before lodgement):**
- Uncited factual claims
- Paraphrased legislation
- Cross-LGA planning content
- Draft scheme cited as operative law
- Director's Policy cited as legal requirement
- Risk without mitigation
- Missing mandatory content

**Non-blocking (should fix before lodgement):**
- Minor inconsistencies in names or numbers
- Style deviations from HTS standard
- Suboptimal citation format
- Generic phrasing that could be more specific

---

## Self-Correction Protocol

If issues are found, offer to:
1. List all issues in the report
2. Correct each issue in sequence (user confirms before moving to next)
3. Re-run the compliance check on the corrected version
4. Confirm clean pass before handoff to document builder


---

**System Version:** 1.1 — Two-stage gate, jurisdiction-aware (WA + NSW)
**Last Updated:** 21 May 2026
