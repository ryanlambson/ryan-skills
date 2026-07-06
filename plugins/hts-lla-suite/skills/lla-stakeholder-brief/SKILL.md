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

# LLA Stakeholder Brief — Pre-Lodgement Consultation Emails

This is a **set skill** — a permanent member of the HTS LLA toolkit, included in every
LLA project regardless of jurisdiction. It exists for one reason: every completed PIA
requires pre-lodgement briefs to the regulatory and public health stakeholders, and
those briefs must match the PIA exactly. A brief that diverges from the PIA — a
different condition, a different capacity, a different address — is worse than no brief
at all. This skill drafts the briefs from the PIA and from nothing else.

## Authoring Entity Lock

All work this skill supports is on behalf of:

**Hospitality Total Services (Aus) Pty Ltd (HTS)**
Planning & Liquor Licensing Consultancy — Office 2, 48 Kishorn Road, Applecross WA 6153
admin@hospitalitytotalservices.com.au | (08) 9316 8699

The signature block on every draft is the HTS block. The sender is Ryan Lambson or the
nominated HTS representative, never the applicant.

## Position in the pipeline

```
lla-pia-drafter → completed PIA (placeholders resolved)
        │
        ▼
lla-stakeholder-brief  ← this skill
   Phase A  Extract from the PIA
   Phase B  Draft recipient variants   ── applies lla-writing-conventions
   Phase C  Review gate                ── scripts/check_conventions.py
        │
        ▼  Ryan sends the emails
        │
   Phase D  Post-send PIA update (dates in, TO DO markers out)
```

If a draft cites legislation beyond ss.41 and 98 of the Liquor Control Act 1988 (WA)
or the equivalent NSW provisions, offer to route it through `lla-citation-checker`
before delivery.

## What this skill is NOT

- **Not the statutory Notice of Application.** That is a prescribed instrument produced
  at advertising, not a courtesy brief. Route to the advertising workflow.
- **Not an objection response or post-lodgement correspondence tool.**
- **Not a sender.** This skill drafts. It never transmits email, even where a mail
  connector is available, unless Ryan gives an explicit in-session instruction to send.
- **Not a source of facts.** It holds no venue, applicant, or planning knowledge of its
  own. If the PIA does not contain a fact, the fact does not go in the email.
- **Not an endorsement machine.** No draft may state or imply that the LEU, CHO, or any
  authority supports the application. The PIA's standard disclaimer (pre-lodgement
  contact is not endorsement) stays in the PIA; the email simply invites feedback.

## Trigger phrases → action

- "PIA is complete, draft the stakeholder briefs" → Phases A–C, all recipients
- "Draft the LEU email" / "Draft the CHO email" → Phases A–C, that recipient
- "Section 8 emails" / "Community Consultation emails" → Phases A–C
- "Pre-lodgement notification for [venue]" → Phases A–C
- "Briefs sent [date]" / "Mark the consultation as sent" → Phase D only

## Authority hierarchy

1. **The completed PIA for this application** — sole source of facts; trading
   conditions are carried verbatim
2. **lla-writing-conventions** — mandatory style layer (banned terms, CCTV scope,
   no em-dashes in paragraphs)
3. **Reference examples** (`references/`) — structure only, never facts
4. **lla-gpt master rules** — tone and authority discipline where not covered above

If a reference example conflicts with the PIA, the PIA wins. If the PIA conflicts with
itself, stop and report the conflict; do not pick a side silently.

## Phase A — Extract

Read the completed PIA (path supplied by Ryan, or locate the PIA docx in the project's
DLGSC folder). Extract:

| Field | Source in PIA |
| --- | --- |
| Applicant entity + ACN/ABN | Introduction / The Applicant |
| Licence class sought | Introduction / Legislative Framework |
| Premises name + full address | Cover page / Introduction |
| Venue concept, key features | Venue and Operation |
| Directors + credentials | The Applicant |
| Trading conditions (verbatim) | Introduction trading conditions block |
| Planning context (one line) | Location and Locality |
| Locality name | Location and Locality |

**Stop rule.** If any required field is missing, or if the sections relied upon still
contain placeholders (`[INSERT`, `XX`), "(TO DO)" markers, or highlighting, STOP and
report exactly what is incomplete. Do not draft around a gap and do not invent a value.

## Phase B — Draft

Produce one email per recipient using `references/email-template.md`:

1. **WA Police Liquor Enforcement Unit (LEU)** — emphasis: harm minimisation measures,
   CCTV (entry and exit points only), management credentials, incident management
2. **Chief Health Officer (CHO)** — emphasis: harm minimisation, at-risk group
   measures, low- and non-alcoholic range, food availability
3. **Local government** (on request) — emphasis: planning alignment, activity centre
   contribution, employment

Drafting rules:

- Trading conditions are pasted **verbatim from the PIA**, then renumbered for the
  email. Never re-type conditions from a template.
- The conditions block and packaged liquor line are keyed to the licence class stated
  in the PIA — see `references/licence-class-matrix.md`. Never assume the class.
- Apply `lla-writing-conventions` to all HTS-authored text: no "sits" (locational),
  no "food-led", no "need", no "community" outside protected statutory phrases, CCTV
  at entry and exit points only, no em-dashes inside paragraphs.
- Close with the standard feedback invitation and the HTS signature block.
- Subject line format: "Pre-Lodgement Advice – Application for the Conditional Grant
  of a [Licence Class] – [Premises Name], [Suburb]".

## Phase C — Review gate

Run the deterministic check over each draft before presenting it:

```
python3 scripts/check_conventions.py <draft-file.md>
```

Exit 0 = pass; exit 1 = fail with line-level detail. Fix every finding and re-run.
Only passing drafts are presented to Ryan. Present all recipient variants together with
a one-line note of any judgement calls made during extraction.

## Phase D — Post-send PIA update

Runs **only** when Ryan confirms the briefs were actually sent, with dates. Then:

1. Back up the PIA docx (same folder, `_backup [date]` suffix) before touching it.
2. In the Community Consultation section: change prospective wording ("will be
   provided", "was invited") to past tense with the sent dates.
3. Remove the "(TO DO)" marker from the section heading and strip the review
   highlighting from the consultation paragraphs.
4. Preserve all formatting; edit the existing document, never rebuild it.
5. Report the edits made and the backup filename.

If Ryan reports only some recipients were briefed, update only those paragraphs and
leave the markers on the rest.

## Licence-class matrix (summary)

Full table with wording: `references/licence-class-matrix.md`. In brief — tavern
restricted and small bar: packaged liquor prohibited; hotel restricted: packaged liquor
to lodgers only; tavern and hotel: packaged liquor as conditioned in the PIA. Small bar
carries the 150-person capacity (patrons plus staff). Trading hours reference s.98(1)
LCA 1988 (WA). **In every case the PIA's own conditions block is the source of truth;
the matrix only guides emphasis and the packaged liquor sentence.**

## Worked examples

- `references/example-last-slice-eaton.md` — tavern restricted, conventions-compliant
  model output. This is the standard to match.
- `references/example-sks-cockburn.md` — hotel restricted, structure reference only.
  Its wording predates lla-writing-conventions; do not copy phrasing from it.

## Troubleshooting

- **PIA has no ACN/ABN** → stop; request the ASIC extract or Applicant Entity document.
- **PIA still in draft (placeholders/highlighting present)** → stop; report the
  outstanding items; suggest completing the PIA first.
- **Licence class not stated or ambiguous** → stop; never infer the class from the
  venue concept.
- **Conditions in the PIA conflict with the licence class** (e.g. a lodger exception in
  a tavern restricted application) → stop and flag; this is a PIA defect, not an email
  drafting choice.
- **Ryan asks the skill to send the email** → confirm the connector, recipients, and
  final text explicitly in-session before sending; absent that confirmation, drafting
  only.
- **NSW matter** → same workflow; swap statutory references per the NSW modules and
  route citations through `lla-citation-checker`.
