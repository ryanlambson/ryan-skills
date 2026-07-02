# OUTLINE — lla-stakeholder-brief

Phase 3 of 4. Status: awaiting approval.

## Proposed frontmatter

```yaml
---
name: lla-stakeholder-brief
description: >
  HTS pre-lodgement stakeholder brief drafter. Use this skill whenever a
  Public Interest Assessment is complete and Ryan or the HTS team needs the
  Section 8 / Community Consultation emails drafted — the pre-lodgement
  briefs to the WA Police Liquor Enforcement Unit (LEU), the Chief Health
  Officer (CHO), and optionally the local government. Trigger phrases:
  "PIA is complete, draft the stakeholder briefs", "draft the LEU email",
  "draft the CHO email", "Section 8 emails", "pre-lodgement notification",
  "mark the consultation as sent". Extracts applicant, licence class,
  premises and trading conditions verbatim from the completed PIA, keys the
  conditions block to the licence class, applies lla-writing-conventions,
  and on confirmation of sending updates the PIA consultation section to
  past tense with dates. Do NOT trigger for PIA drafting, the statutory
  Notice of Application, objection responses, or post-lodgement
  correspondence.
license: Proprietary. HTS internal use only.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: "1.0"
  role: pre-lodgement-consultation
  jurisdiction: agnostic
  set_skill: "true"
---
```

(Description ~1010 chars — under the 1024 limit; verified at draft time.)

## SKILL.md section structure (target ≤300 lines)

1. Title + set-skill statement + Authoring Entity Lock (HTS entity block)
2. Position in the pipeline (diagram: PIA complete → this skill → send → Phase D update; relationship to lla-pia-drafter, lla-writing-conventions, optional lla-citation-checker)
3. What this skill is NOT (Notice of Application, objection replies, endorsement claims, auto-send)
4. Trigger phrases → phase mapping
5. Authority hierarchy (PIA > lla-writing-conventions > reference examples > lla-gpt tone)
6. Phase A — Extract (field list, placeholder/highlight stop rule)
7. Phase B — Draft (recipient variants; licence-class keyed conditions; conventions; structure per references/email-template.md)
8. Phase C — Review gate (run scripts/check_conventions.py; present drafts; never send unless expressly instructed in-session)
9. Phase D — Post-send PIA update (explicit confirmation + dates required; past-tense edit; remove TO DO markers/highlighting; backup before save)
10. Licence-class matrix (tavern restricted / tavern / hotel / hotel restricted / small bar: packaged liquor line + capacity note differences)
11. Worked examples (pointers to references/)
12. Troubleshooting / failure modes (missing ACN, draft PIA, conflicting conditions, no licence class stated)

## scripts/

- `check_conventions.py` — deterministic post-draft check on a text/markdown file:
  banned terms (sits-locational heuristic, food-led, need, community) with a
  protected-strings allowlist; em-dash and spaced en-dash in body text; CCTV scope
  phrases ("throughout", "internal and external", "full coverage"); leftover
  placeholders ([INSERT, TO DO, XX]). Exit 0 pass / 1 fail with line detail.
  Python 3 stdlib only.

## references/

- `email-template.md` — canonical structure with slot names ({{APPLICANT_ENTITY}},
  {{ACN}}, {{LICENCE_CLASS}}, {{PREMISES}}, {{CONDITIONS_VERBATIM}} …) and the fixed
  closing/signature block.
- `example-sks-cockburn.md` — the SKS Cockburn Central hotel example (structure
  reference only; pre-conventions wording flagged as such).
- `example-last-slice-eaton.md` — the Eaton tavern restricted brief (conventions-
  compliant model output).
- `licence-class-matrix.md` — full licence-class differences table (packaged liquor,
  lodger exception, capacity references, s.98 trading hours line).

## assets/

None. (No binary templates required; emails are text.)

## Trigger phrases (final)

Positive: "PIA is complete, draft the stakeholder briefs" / "draft the LEU email" /
"draft the CHO email" / "Section 8 emails" / "Community Consultation emails" /
"pre-lodgement notification for [venue]" / "mark the consultation as sent [date]".
Negative: PIA section drafting, Notice of Application, objection responses,
post-lodgement correspondence, consumer survey work.

## QA criteria for this skill (Phase 4 gate)

Structural: spec-valid frontmatter; name = folder; description <1024 no angle brackets;
body ≤500 lines; script has shebang, passes py_compile, stdlib-only, no network, reads
only its inputs. Content: entity lock present; NOT-section present; triggers mapped;
authority hierarchy present; ≥2 worked examples; troubleshooting present; exact script
invocation shown; every referenced file exists; no hallucinated tool access; house tone.
Portability: no Claude-only features; scripts stdlib-only. Domain-specific: conditions
verbatim rule stated as a refusal; endorsement disclaimer rule present; Phase D
confirmation gate explicit; licence-class matrix covers all five s.41 classes.
