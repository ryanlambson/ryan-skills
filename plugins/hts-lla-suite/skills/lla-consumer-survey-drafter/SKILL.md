---
name: lla-consumer-survey-drafter
description: >
  HTS consumer survey drafter for Western Australian liquor licence applications.
  Use this skill whenever the user asks to draft, adapt, review, redraft, or
  produce any consumer survey or Attachment 2A for a liquor licence application —
  including liquor stores, taverns, small bars, restaurants, hotel licences, or
  extended trading permits. Also trigger for requests to "adapt this survey for
  [new applicant]", "review my draft survey", "redraft the introduction",
  "apply the edits from these notes", "produce a consumer survey for [premises]",
  or any instruction to produce survey content destined for LGIRS lodgement as
  Attachment 2A or equivalent evidence under s.36B(4) / s.38(4). This skill is
  the content layer — for SurveyMonkey deployment, hand off to surveymonkey-transposer.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: consumer-survey-generation
  related_skills:
    - lla-gpt (master skill — HTS branding and authority hierarchy)
    - lla-document-builder (for .docx output)
    - lla-pia-drafter (for the PIA section that consumes survey data)
    - lla-precedent-advisor (for case-law citations in report-back)
    - lla-harm-minimisation (for harm-minimisation paragraph wording)
    - surveymonkey-transposer (for deployment to SurveyMonkey)
---

# LLA Consumer Survey Drafter

## Purpose

Drafts, adapts, and reviews consumer surveys for WA liquor licence applications.
Surveys produced under this skill are lodgement-grade evidence supporting the
s.36B(4) consumer requirement test and the s.38(4) public interest assessment.

This skill is the **content layer**. It produces survey copy in markdown
(canonical, editable) and hands off to `lla-document-builder` for .docx output
or to `surveymonkey-transposer` for SurveyMonkey deployment.

---

## Pre-Delivery Gate (MANDATORY)

Consumer surveys cite the Liquor Control Act 1988 (s.36B(4), s.38(4)),
benchmark cases (Liquorland Karrinyup, Liquorland South Bunbury), and
locality-specific competitor lists. All of these are exactly what the HTS
two-stage pre-delivery gate verifies:

1. **Stage 1 — lla-citation-checker.** Confirms every legislative,
   case-law, and project knowledge citation in the survey introduction and
   the report-back stub is correctly formatted and resolves to its source.
2. **Stage 2 — lla-compliance-checker.** Runs the survey QA checklist
   (below) plus structural and authority-hierarchy checks.

Run Stage 1 before Stage 2. The QA checklist further down feeds Stage 2.

For deployment to SurveyMonkey, route through `surveymonkey-transposer` only
after both gates clear.

---

## Core principle: Precedent-first

**Default action: adapt an existing approved HTS survey. Do not build from scratch.**

When a survey is requested, the first move is to identify which HTS precedent best
matches the licence type and adapt it — swapping in applicant, address, locality,
competitor list, and any premises-specific manner of trade. Structure, question
order, question wording, answer options, and skip logic mirror the precedent
unless the client explicitly directs otherwise.

If the user supplies a content brief or info pack alongside a precedent, the
**precedent governs structure**; the brief supplies swap-in content only. The
brief is not a structural override. If the brief proposes structural deviations,
flag them and ask before applying.

### HTS precedent library (current)

| Precedent | Licence type | Strength | Project knowledge file |
|-----------|--------------|----------|------------------------|
| Liquor Barons Safety Bay | Liquor store with drive-through + walk-in | **Gold standard** for liquor store applications | Attachment_2A_-_Consumer_Survey.pdf |
| Australind Specialty Cellars | Liquor store with dual-lane drive-through | Strong precedent for tech-forward / Southwest-focused stores | SurveyMonkey_418664274.pdf |
| Piara Cellars | Liquor store adjacent to IGA | Strong precedent for shopping-centre liquor stores | SurveyMonkey_411832857.pdf |
| Queen Maeve's | Tavern Restricted (cultural venue) | Gold standard for cultural / community taverns | SurveyMonkey_420325647.pdf |
| The Iris Pavilion | Tavern Unrestricted (family hospitality) | Gold standard for family-friendly hospitality | SurveyMonkey_522107591.pdf |
| Moon and Mary | Tavern Unrestricted (cuisine-led) | Gold standard for cuisine-led venues | SurveyMonkey_516403109.pdf |
| Coogee Boathouse | Tavern Restricted + ETP | Strong precedent for marina / waterside venues | SurveyMonkey_521736758.pdf |

Always confirm which precedent is being used at the start of a drafting task.

### When to deviate from precedent

Only deviate on explicit client direction, and flag every deviation. Common
legitimate deviations:

- New competitor mix (locality-specific Q3 outlets)
- New "reasonable requirements" options (Q4) reflecting venue concept
- New "specialty products" options (Q7) reflecting product range
- Age band aggregation (e.g. 18–30 / 31–50 / 51–70 / 70+ instead of six bands)
- Locality-specific terminology (e.g. "Witchcliffe Ecovillage", "Margaret River")

### High-risk deviations — challenge before applying

Some deviations weaken evidentiary value for the PIA. Flag and challenge:

- **Removing Q6 (frequency).** Loses the weekly/fortnightly/monthly evidence that drives the "reasonable demand" narrative under s.36B(4).
- **Removing Q7 (specialty products).** Loses the spine of unmet-consumer-requirements evidence under s.36B(4).
- **Removing the harm minimisation paragraph entirely.** Leaves the application open to "you're not addressing harm" criticism in the s.38(4)(a) limb. Recommend trim, not cut.
- **Flipping the polarity of Q11/Q12 (harm/amenity).** Safety Bay convention is positive-framed so "Yes" is supportive. Flipping inverts every report-back metric. Workable, but flag the implications.
- **Adding brand names of proposed co-tenants.** Creates expectation-vs-delivery exposure if the named tenants don't materialise. Strongly recommend generic categories instead.

---

## Workflow

### Stage 1: Information gathering

Before drafting, confirm:

```
□ Licence type (liquor store / tavern restricted / tavern unrestricted / small bar / hotel / restaurant / ETP)
□ Legal entity name (Pty Ltd, trust structure if any)
□ Trading name
□ Full premises address (lot/diagram/volume/folio if known)
□ Locality definition (which suburb names define the "locality" for Q1 and Q3 options)
□ Manner of trade summary (drive-through, walk-in, browse area, cool room, etc.)
□ Operating hours (if relevant to the application)
□ Existing licensed outlets in the locality (Q3 competitors)
□ Distribution method (online via SurveyMonkey / print / both)
□ Target sample size (minimum 50; 150–300+ for contested or specialty applications)
```

If a content brief or info pack is supplied, parse it against this checklist
first. Flag any missing items and ask before proceeding.

### Stage 2: Precedent selection and adaptation

1. Pick the closest-matching precedent from the library
2. Map swap-in fields from the brief to the precedent structure
3. Identify locality-specific competitor outlets for Q3
4. Identify any premises-specific features for Q4/Q7
5. Confirm any deviations from precedent (flag high-risk deviations)
6. Produce the markdown draft

### Stage 3: Markdown draft

Output the survey as markdown using this structure:

```
# [Trading Name]
## Consumer Survey
## [Licence Type] Application
## [Premises Address]

[Addressee block — typically the Director of Liquor Licensing]

## Introduction
[One paragraph — applicant entity, survey purpose, trading name, address]

## Manner of Trade
[Lead paragraph — drive-through/walk-in, localities served]
[Bullet list of premises features]
[Operator paragraph — experienced industry professionals, track record]
[Trading hours — only if relevant]
[Harm minimisation paragraph — trim, not cut]

## What will happen with the information you provide
[Submission paragraph — destination, purpose]
[Public interest definition — bold heading, italicised quote]
[Privacy/redaction note]
[HTS contact details — Ryan Lambson or Mario Sequeira]

[15–16 questions — see "Standard question architecture" below]
```

### Stage 4: Review and edit-handling

If the user returns markup, voice notes, or written edits, use the
**numbered-edit confirmation protocol** (see below) before applying changes.

### Stage 5: Output

- **.md file** — canonical, editable, in `/mnt/user-data/outputs/`
- **.docx file** — optional, for external review, generated via `lla-document-builder`
- **SurveyMonkey deployment** — optional, via `surveymonkey-transposer`

---

## Numbered-edit confirmation protocol

When edits arrive ambiguously — handwritten markup on a photo, voice-to-text
transcripts, free-prose comments, email feedback — do not interpret silently.

### The protocol

1. **Read the markup end-to-end first.** Do not start applying edits during the read.
2. **Group by page or section** in the order the markup appears.
3. **State each edit in one sentence** in plain English, with explicit before/after wording where possible.
4. **Number every edit** so the user can answer against specific numbers.
5. **Flag ambiguities** at the bottom with a clear ask: "I read this as X — confirm or correct."
6. **Wait for confirmation** before applying any edits.
7. **Apply all edits in one redraft** — not piecemeal — once confirmation is in.

### Example format

```
**Page 1 — Manner of Trade**

1. Lead paragraph: insert "and passing through" → "…visitors in **and passing through** the Witchcliffe locality."
2. Move bullet 2 ("walk-in retail browse area") to first position, prefix with "Easy access to".
3. Spirits bullet: insert "craft" → "A full spirits selection including **craft** whisky, vodka, gin, rum, and liqueurs."

**Page 2 — Introduction**

4. Italicise the public interest definition.
5. Bold "Public Interest" in the lead-in.

**Ambiguities to confirm:**
- Item 22: I read the polarity flip on Q11 as deliberate — confirm? Note this inverts all your report-back metrics.
```

### Why this matters

Markup is dense with intent and silent on ambiguity. A photo annotation might
look like a deletion but mean "move this here." A voice note might say "get rid
of this bit" with the antecedent unclear. Numbering forces precision and gives
the client a confirmation surface that's faster than re-marking.

This protocol saved a full round of rework on the Thirsty Camel Witchcliffe
adaptation (May 2026).

---

## Strategic reframe handling

Sometimes a client mid-process redirects the survey's strategic framing — for
example, shifting from "consumer survey for a liquor store" to "community
consultation about a Greenfield site where a liquor store is one use."

### How to handle reframes

1. **Slow down.** Don't redraft on the first pass. A reframe is a directional
   shift, not an edit round.
2. **Separate clear direction from ambiguous direction.** Voice-to-text
   transcripts are noisy. Reread carefully. Distinguish "definitely change this"
   from "I think they're saying X but unclear."
3. **Flag regulatory exposure.** Reframes that dilute the s.36B(4) consumer
   requirement focus can weaken evidentiary value. Common risks:
   - Survey reads as "site consultation," respondents don't engage with the
     packaged-liquor question with consumer-requirement intent
   - LGIRS reviewer argues the methodology dilutes evidence weight
   - Mismatch between survey framing and PIA framing creates audit exposure
4. **Propose mitigation.** Usually: keep the liquor questions intact and load-
   bearing; reframe only the introduction; explain the broader context in the
   PIA covering letter so the reviewer understands the methodology was sound.
5. **Ask numbered questions before drafting.** Same protocol as edit-handling.
6. **Redraft only after confirmation on each numbered question.**

### Reframe patterns to watch for

- **"Site uses" framing** instead of "liquor store" framing
- **"Related services / additional retail" questions** that broaden the survey beyond packaged liquor
- **Removal of the formal LGIRS addressee block** from the top (acceptable if regulatory framing stays in the body)
- **De-licensing of operator language** ("development of premises" vs "development of licensed premises")

These are all defensible if handled with discipline.

---

## Defensive drafting principles

### No brand names you can't guarantee delivery on

If the survey asks about co-tenants, complementary retail, food offerings, or
any element of the broader development, **do not name brands**.

❌ "Subway, Pizza Hut, 7-Eleven, KFC"
✅ "Convenience food (e.g. sandwich shop, bakery)"

Reasoning: a named brand on the survey creates a documented expectation. If the
brand doesn't materialise, an objector can cite the survey as misrepresentation.
The Liquor Commission has criticised exactly this mismatch in past decisions.

### No "fast food" framing

Avoid "fast food" as a category label. It triggers Health Department interest
in the s.38(4)(a) harm limb and creates an angle for objectors about "attracting
youth" or "supporting unhealthy lifestyles."

❌ "Fast food outlet"
✅ "Convenience food"
✅ "Café / bakery"
✅ "Quick-service food"

### Polarity discipline on harm/amenity questions

Safety Bay convention: harm and amenity questions are **positive-framed** so
that "Yes" is the supportive answer. This makes report-back analysis simpler
and aligns with the s.38(4) statutory language.

Standard polarity:
- "Do you believe [the proposed premises] will **not cause** undue harm..." → Yes = supportive
- "Do you believe [the proposed premises] would have a **negative impact** on amenity..." → No = supportive (counter-intuitive but mirrors statutory test)

If the client wants to flip polarity, do it — but flag that every report-back
metric inverts and the PIA report-back paragraphs need to be rewritten too.

### Leading questions

Avoid questions that bias respondents toward approval:

❌ "Would you support this great new local liquor store?"
✅ "Do you support the liquor store licence application for the proposed [Trading Name]?"

❌ "Don't you agree that [premises] would benefit the community?"
✅ "Do you believe it is in the public interest to conditionally approve a Liquor Store Licence for the proposed [Trading Name]?"

### Trim, don't cut, the harm minimisation paragraph

Cutting it entirely opens the "you're not addressing harm" line of attack from
the Health Department. Trim instead. One sentence is sufficient if the longer
version feels heavy:

> "Comprehensive harm minimisation protocols will be in place, including CCTV
> surveillance, strict ID verification, secure storage of spirits, and a
> zero-tolerance approach to anti-social behaviour, with no unaccompanied
> juveniles permitted on the premises."

Defer to `lla-harm-minimisation` for fuller harm-min content destined for the
PIA body or Management Plan.

---

## Standard question architecture

The standard liquor store consumer survey is **15–16 questions** mirroring
Safety Bay. Aggregate question count above 16 is the fatigue ceiling.

### Q1 — Relationship to locality
- Single choice, required
- 4–5 options + "Other (please specify)"
- Options reflect residency, work, frequent visitor, broader LGA

### Q2 — Age group
- Single choice, required
- Standard six bands (18–24 / 25–34 / 35–44 / 45–54 / 55–64 / 65+) or aggregated four bands (18–30 / 31–50 / 51–70 / 70+)

### Q3 — Current packaged liquor outlets
- Multi-select, required
- Locality-specific competitor list + "I do not consume alcohol" + "Other liquor store outside the locality (please specify)"

### Q4 — Reasonable requirements
- Multi-select, required
- 8–10 options drawn from convenience, drive-through, parking, pricing, WA producers, specialty products, independent service, brand requests
- This is the s.36B(4) "consumer requirement" evidence spine

### Q5 — Intent to shop
- Single choice, required
- Yes / No / Unsure

### Q6 — Frequency *(optional but recommended)*
- Single choice, required if included
- Weekly / Fortnightly / Monthly / Unsure
- Provides "reasonable demand" volume estimate for the s.36B(4) analysis

### Q7 — Specialty products *(optional but recommended)*
- Multi-select, required if included
- 7–8 options reflecting product range + "Other (please specify)"
- This is the unmet-consumer-requirements evidence spine

### Q8 — Caters to unmet requirements
- Single choice, required
- Yes / No / Unsure

### Q9 — Support for the application
- Single choice, required
- Yes (Go to Q11) / No (Go to Q10) / Unsure (Go to Q11)
- Skip logic anchor

### Q10 — Reasons for not supporting
- Multi-select, conditional (only if Q9 = No)
- 3–4 options + "Other (please specify)"

### Q11 — Harm/ill-health
- Single choice, required
- Positive-framed: "will not cause undue harm..."
- Yes / No (Yes = supportive)

### Q12 — Amenity impact
- Single choice, required
- Negative-framed: "negative impact on amenity..."
- No / Yes (No = supportive)

### Q13 — Disturbance/inconvenience
- Single choice, required
- No concerns / Yes, I have concerns

### Q14 — Public interest
- Single choice, required
- Yes / No

### Q15 — Additional comments
- Open text, optional
- Free-form qualitative feedback for the PIA report-back

### Q16 — Contact details + 18+ declaration
- Demographic block with Name (required), Suburb (required), Email/Phone (optional)
- Includes the 18+ declaration in the question heading

---

## QA checklist (Stage 2 inputs — run before handoff)

Stage 1 (`lla-citation-checker`) audits the citations first. This checklist
is verified by Stage 2 (`lla-compliance-checker`) before the survey is
handed off to `lla-document-builder` or `surveymonkey-transposer`.

```
□ Introduction names applicant entity correctly
□ Premises address correct (street + suburb + postcode + lot/diagram if known)
□ Addressee block matches the current licensing authority address
  (Department of Local Government, Industry Regulation and Safety / PO Box 6119 East Perth WA 6892
   — confirmed correct as of May 2026)
□ Public interest definition present and italicised
□ "Public Interest" lead-in is bolded
□ Privacy/redaction note present
□ HTS contact details present (Ryan Lambson + Mario Sequeira)
□ Q1 locality options reflect the actual locality (not copied from precedent without adaptation)
□ Q3 competitor list reflects actual locality outlets
□ Q4 reasonable requirements include the venue's distinctive features
□ Q9 skip logic specifies Q11 (or current equivalent) on Yes/Unsure, Q10 on No
□ Q11/Q12 polarity matches Safety Bay convention (Yes = supportive for harm; No = supportive for amenity)
□ Harm minimisation paragraph present (trimmed acceptable; cut not acceptable)
□ Total question count is 12–16
□ No leading question wording
□ No brand names of un-secured co-tenants
□ No "fast food" category labels
□ 18+ declaration present on the contact details question
```

---

## Report-back stub for PIA

Every survey contemplates a report-back paragraph that must be written into the
PIA after responses are collected. At the time of drafting the survey, produce
a **stub** that names the metrics to be reported and the benchmark cases.

### Standard liquor store report-back stub

```
[Section 6.40–6.42 of the PIA — to be completed after survey closes]

Once the survey closes, report on:
- Total verified respondents (target: 150+; specialty applications: 300+)
- Proportion residing within the defined locality (target: >60%)
- Demographic distribution by age band
- Top three reasons for current out-of-locality purchasing (Q3)
- Top three "reasonable requirements" identified (Q4)
- Proportion intending to shop at the proposed premises (Q5: Yes + Unsure combined)
- Proportion supporting the conditional grant (Q9 Yes — target: >75%)
- Proportion considering the grant to be in the public interest (Q14 Yes — target: >75%)
- Most-cited specialty product categories (Q7)
- Summary of concerns raised (Q10, Q15)

Benchmark cases:
- Liquorland Karrinyup (LC07/2017) — granted on 70% support
- Liquorland South Bunbury (LC18/2015) — refused on 40% support / 47% opposition

Defer to lla-precedent-advisor for additional or more recent benchmark cases.
```

---

## Handoff conventions

### To lla-document-builder

When a .docx is needed for external review or print distribution:

```
Please produce a .docx of the consumer survey in /mnt/user-data/outputs/.
Use A4, Arial 11pt, open-circle markers (○) for single-select options,
open-square markers (☐) for multi-select options, and bold question headings.
```

### To surveymonkey-transposer

When the survey needs to be deployed to SurveyMonkey:

```
Please deploy this survey to SurveyMonkey. The introduction text goes into
three descriptive_text blocks on three intro pages. All questions go onto a
single "Survey Questions" page in order. Q9 skip logic is configured manually
by the user after deployment (MCP limitation).
```

### To lla-pia-drafter

When the survey results are in and the PIA section needs to be written:

```
The survey has closed with [X] responses. Please draft Section 6.40–6.42 of
the PIA using the report-back stub from the survey draft, populated with
the actual response data.
```

---

## Lessons captured

- **Thirsty Camel Witchcliffe (May 2026):** Numbered-edit protocol developed in response to handwritten markup that was initially misread. Strategic reframe handling developed in response to Mario's broader-site framing voice note. No-brand-names rule reinforced.
- **Liquor Barons Safety Bay (precedent):** Established the 16-question architecture, positive-framed harm/amenity polarity, and the Q9 skip-logic anchor.

Future lessons should be added to this section as they emerge.


---

**System Version:** 1.1 — Two-stage pre-delivery gate wired
**Last Updated:** 21 May 2026
