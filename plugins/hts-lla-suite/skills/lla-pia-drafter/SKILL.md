---
name: lla-pia-drafter
description: >
  HTS PIA drafter for generating Public Interest Assessment sections for Western
  Australian liquor licence applications. Use this skill whenever the user asks
  to draft, write, generate, or adapt any PIA section — including Introduction,
  Location and Locality, Venue and Operation, The Applicant, Legislative
  Framework, Public Interest, Harm sections (38(4)(a)(b)(c)(ca)), Summary,
  Advertising, or Attachments. Also trigger for requests to "start the PIA",
  "do the next section", "adapt this for the new application", "write section X",
  or any instruction to produce submission-ready content for LGIRS lodgement.
  This skill governs the section-by-section drafting workflow and works in
  conjunction with lla-document-builder to produce formatted output.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: pia-generation
---

# LLA PIA Drafter — Section-by-Section Workflow

## Purpose

This skill manages the drafting of Public Interest Assessment sections for
HTS liquor licence applications. It governs information gathering, section
sequencing, content generation, and handoff to the document builder.

Each section is drafted individually, reviewed, then compiled into a final
document. This approach ensures quality control at every stage and allows
genuine rewriting for each new applicant rather than copy-paste adaptation.

---

## Pre-Delivery Gate (MANDATORY)

Every PIA section produced by this skill must pass through the HTS two-stage
pre-delivery gate before being marked submission-ready:

1. **Stage 1 — lla-citation-checker.** Citation audit. Verifies every
   legislative, regulatory, Director's Policy, case-law, planning-instrument
   and data citation against its source. Flags uncited factual claims.
2. **Stage 2 — lla-compliance-checker.** HTS QA checklists, including the
   per-section completion checklist at the bottom of this skill.

Each completed section draft is handed to Stage 1 before being handed to
Stage 2. Stage 2 will not produce a "READY FOR LODGEMENT: YES" verdict until
Stage 1 reports `cleared_for_stage_2`.

---

## MANDATORY BEFORE DRAFTING ANY SECTION

### 1. Confirm Project Files Are Loaded

The following must be accessible in the active project:
```
□ LEGISLATION_LCA1988_MASTER_INDEXED.md
□ DP_PIA_MasterCompendium.md
□ Case_Precedent_Compendium.md
□ KNOWLEDGE_HarmMinimisation.md
□ [LGA]_PLANNING_MASTER_PACK.md  (locality-specific)
□ PIA template for this licence type
```

If any are missing: stop and request upload before proceeding.

### 2. Confirm Client Variables

```
□ Legal entity name (Pty Ltd)
□ Trading name
□ Full premises address
□ Director name(s)
□ Approved Manager (name, card type, expiry)
□ Licence type being applied for
□ Venue concept
□ Patron capacity
□ Trading hours requested
□ Food service model
□ Key features (TAB, gaming, live music, alfresco, etc.)
□ Floor plan uploaded
□ Menu or food concept available
□ Consumer survey data (if applicable)
```

### 3. Run Planning Pre-Check (Before Section 2)

```
□ Zone confirmed from current gazetted scheme (not draft)
□ Use class confirmed: P / D / A / X
□ LPP exemption check — DA required?
□ Special Control Area?
□ Heritage listed?
□ Events/functions proposed?
□ Street-facing alfresco?
□ New signage?
□ Settlement-specific policies?
```

Source: locked LGA planning pack only. Never infer from general knowledge.

---

## Section Sequence and File Sources

Work through sections in this order. Each section references specific
project files — use ONLY those files for that section's content.

| # | Section Title | Primary Sources | Time Est. |
|---|---|---|---|
| 1 | Introduction | Legislation, DP_PIA, application info | 10–15 min |
| 2 | Location and Locality | LGA Planning Pack | 15–20 min |
| 3 | Venue and Operation | Floor plan, menu, concept docs | 20–25 min |
| 4 | The Applicant | Application documents | 10 min |
| 5 | Legislative Framework | LEGISLATION_LCA1988 | 15 min |
| 6 | Public Interest | DP_PIA, Planning Pack, KNOWLEDGE files | 20–25 min |
| 7 | s.38(4)(a) — Harm or Ill-health | KNOWLEDGE_HarmMinimisation, Case_Precedent | 25–30 min |
| 8 | s.38(4)(b) — Amenity | KNOWLEDGE_EntertainmentNoise, Planning Pack | 20 min |
| 9 | s.38(4)(c) — Offence/Annoyance | KNOWLEDGE_HarmMinimisation, DP_PIA | 15 min |
| 10 | s.38(4)(ca) — Tourism/Culture | KNOWLEDGE_Tourism, KNOWLEDGE_FoodCulture | 15 min |
| 11 | Summary | All preceding sections | 10 min |
| 12 | Advertising | KNOWLEDGE_AlcoholAdvertising, DP_PIA | 10 min |
| 13 | Attachments | Attachment list compiled from above | 10 min |

---

## Drafting Rules (Apply to Every Section)

### Source-of-Truth Rule
- Use ONLY content from project files
- NEVER draw on general knowledge, memory, or prior projects
- If information is absent from project files: state what is missing

### Citation Standard
Every factual claim must cite its source:
```
(Source: FILE_NAME.md, Section/Heading)
```
No uncited assertions. No placeholder citations.

### Authority Hierarchy
1. Legislation — quote verbatim only, never paraphrase
2. Director's Policies — label as "(Guidance)", never as law
3. Case Law — methodology only, cite case name and reference
4. Planning documents — current gazetted scheme only
5. Knowledge modules — supporting evidence only, never authority

### Drafting Tone
- Formal, regulatory, third-person
- Submission-ready — suitable for LGIRS lodgement without further editing
- "It is submitted that…" / "The Applicant acknowledges…"
- No conversational language, no speculation, no generic statements

### Originality Standard
Each section must be genuinely rewritten for the current applicant.
The source PIA informs argument structure — not prose. Clients pay for
original work. No section should be identifiable as adapted from a prior PIA.

---

## Section-Specific Rules

### Section 1 — Introduction
- Use MANDATORY text from template where indicated
- Check whether venue is in an activity centre (conditional paragraphs 1.8–1.9)
- Confirm all attachment numbers are referenced

### Section 2 — Location and Locality
- Use natural geographic boundaries — not arbitrary radius measurements
- Extract zone, use class, and centre hierarchy from planning pack
- Cite specific planning document name and section for every provision

### Section 5 — Legislative Framework
- Quote statutory provisions verbatim from LEGISLATION_LCA1988_MASTER_INDEXED.md
- Identify the applicable section for this licence type
- Do NOT paraphrase legislation under any circumstances

### Section 7 — Harm Assessment (s.38(4)(a))
Apply the Carnegies four-step framework:
```
Step 1: Identify existing harm in the locality
Step 2: Identify likely harm from this application
Step 3: Compare likely harm against existing harm
Step 4: Weigh harm against public interest benefits
```
Every risk identified MUST conclude with a mitigation measure.
Source: Case_Precedent_Compendium.md — Carnegies LC28/2015

### Section 8 — Amenity (s.38(4)(b))
- Address noise, hours, patron behaviour, and interface with nearby uses
- Reference KNOWLEDGE_EntertainmentNoise.md for mitigation evidence
- Cite locality-specific planning controls from LGA planning pack

---

## Output Format Per Section

Each completed section is delivered as:
1. **Plain text draft** — for review in chat (with all citations inline)
2. **Stage 1 audit** — handoff to `lla-citation-checker` for citation verification
3. **Stage 2 audit** — handoff to `lla-compliance-checker` for QA (uses the
   Section Completion Checklist below)
4. **Handoff to lla-document-builder** — for formatting into .docx (only
   after Stages 1 and 2 both clear)

Confirm the plain text draft is approved AND the two-stage gate is cleared
before triggering document generation.

---

## Stop Rules

Stop and request clarification if:
- Required project file is missing
- Client variable is unknown and cannot be inferred
- Planning provision is not in the locked LGA planning pack
- Instruction would require using general knowledge not in project files
- Section content conflicts with a higher authority source

Do not proceed past a stop condition by making assumptions.

---

## Section Completion Checklist (Stage 2 inputs)

These items are checked by `lla-compliance-checker` (Stage 2) once Stage 1
(citation audit) has cleared. Before delivering any section:
```
□ All claims cited to specific project file and section
□ Statutory text quoted verbatim (not paraphrased)
□ Director's Policy labelled as guidance
□ No cross-LGA planning references
□ Knowledge modules cited as evidence only (not authority)
□ All risks concluded with mitigation measures
□ Venue-specific details throughout (not generic)
□ No [INSERT] placeholder text remaining
□ Venue name and legal entity consistent throughout
□ Attachment references numbered and accurate
□ Section is original — not identifiable as adapted prose
```


---

**System Version:** 1.1 — Two-stage pre-delivery gate wired
**Last Updated:** 21 May 2026
