---
name: lla-precedent-advisor
description: >
  HTS legal precedent advisor for Western Australian liquor licensing case law
  and decisions. Use this skill whenever the user asks about legal precedents,
  case law, how to apply a specific case, what cases support an argument,
  the Carnegies framework, consumer requirements doctrine, harm assessment
  methodology, mandatory objects, proportionality in conditions, or any
  question involving LLA or Supreme Court decisions. Also trigger for requests
  to "find a case for this argument", "what precedent supports", "how does
  Carnegies apply here", "cite the relevant case law", or any instruction to
  use legal decisions to support a PIA argument. This skill ensures case law
  is applied at the correct authority level — never elevated above legislation
  or Director's Policy.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: legal-research
---

# LLA Precedent Advisor — Case Law Application

## Purpose

This skill guides the correct identification and application of Western
Australian liquor licensing precedents within HTS PIAs. It ensures case law
is used for methodology and principle — never cited as binding authority above
its proper tier in the authority hierarchy.

---

## Pre-Delivery Gate (MANDATORY)

Case-law citations are exactly what Stage 1 of the HTS pre-delivery gate
verifies. Any precedent citation produced under this skill must survive both
gates before it reaches a delivered work product:

1. **Stage 1 — lla-citation-checker.** Confirms every case citation
   (Carnegies, Liquorland Karrinyup, Sand Volley, Pilbara s.64, WASC 128,
   Tokyo Mart, NCAT decisions, NSW Supreme Court decisions) is in the
   project's Case_Precedent_Compendium.md or equivalent, and is formatted
   correctly per the HTS citation specification.
2. **Stage 2 — lla-compliance-checker.** Confirms case law is applied at
   the correct authority tier (Tier 3 — never elevated above legislation or
   Director's Policy).

WA-only cases (Carnegies, Sand Volley, Pilbara s.64, Liquorland Karrinyup) in
a NSW draft are FAILs at Stage 1. This skill is WA-locked — for NSW
precedent advice, use the NSW-specific track.

---

## MANDATORY: Authority Hierarchy Reminder

Case law sits at **Tier 3** in the HTS authority hierarchy:

```
Tier 1 — Legislation (Liquor Control Act 1988) — SUPREME
Tier 2 — Director's Policies — GUIDANCE
Tier 3 — Case Law & Licensing Precedent ← YOU ARE HERE
Tier 4 — Locality Planning (current gazetted)
Tier 5 — Draft Planning Instruments (reference only)
Tier 6 — Knowledge Modules (supporting evidence only)
```

**Case law never overrides legislation or Director's Policy.**
Case law provides methodology, interpretive principles, and assessment
frameworks — not binding legal requirements.

Always source case law from: `Case_Precedent_Compendium.md`
Never cite cases from memory or general knowledge.

---

## Key Cases — Quick Reference

### Carnegies (LC28/2015)
**Principle:** Four-step harm assessment framework
**Use for:** Section 7 — s.38(4)(a) harm or ill-health assessments
**Framework:**
1. Identify existing harm in the locality
2. Identify likely harm from this application
3. Compare likely harm against existing harm
4. Weigh harm against public interest benefits

**Citation format:**
`(Source: Case_Precedent_Compendium.md — Carnegies LC28/2015)`

---

### Liquorland Karrinyup (WASC 366)
**Principle:** Consumer requirements doctrine
**Use for:** Packaged liquor applications — demonstrating unmet demand
**Key doctrine:** Applicant must demonstrate that consumer requirements
for liquor in the locality are not adequately met by existing outlets.
**Related:** Also applicable to s.36B(4) submissions

**Citation format:**
`(Source: Case_Precedent_Compendium.md — Liquorland Karrinyup WASC 366)`

---

### WASC 128
**Principle:** Consumer requirements — geographic locality definition
**Use for:** Defining the relevant locality using natural boundaries
**Key doctrine:** Locality should be defined by natural geographic
features and community patterns — not arbitrary radius measurements.

**Citation format:**
`(Source: Case_Precedent_Compendium.md — WASC 128)`

---

### Sand Volley
**Principle:** Mandatory objects doctrine
**Use for:** Demonstrating how an application serves the objects of the Act
**Key doctrine:** The objects of the Act in s.5 are mandatory considerations —
the licensing authority must have regard to them in every determination.

**Citation format:**
`(Source: Case_Precedent_Compendium.md — Sand Volley)`

---

### Pilbara s.64
**Principle:** Proportionality in licence conditions
**Use for:** Responding to proposed conditions or challenging unreasonable
conditions imposed by the licensing authority
**Key doctrine:** Conditions imposed must be proportionate to the harm
or risk they are designed to address.

**Citation format:**
`(Source: Case_Precedent_Compendium.md — Pilbara s.64)`

---

### Tokyo Mart (LC38/2017)
**Principle:** Cultural community requirements
**Use for:** Applications serving specific cultural communities — demonstrating
unmet demand for culturally specific products
**Key doctrine:** Cultural specificity of product range can constitute
a distinct consumer requirement not met by general packaged liquor outlets.

**Citation format:**
`(Source: Case_Precedent_Compendium.md — Tokyo Mart LC38/2017)`

---

## Precedent Application Process

### Step 1 — Identify the Argument Need
What is the applicant trying to establish?
- Demonstrating public benefit → Sand Volley (mandatory objects)
- Harm assessment → Carnegies (four-step framework)
- Unmet consumer demand → Liquorland Karrinyup + WASC 128
- Cultural community need → Tokyo Mart
- Proportionate conditions → Pilbara s.64

### Step 2 — Search the Compendium
Always search `Case_Precedent_Compendium.md` for the specific case before citing.
Do not rely on the quick reference above alone — read the full case entry for
the precise principle and any limitations.

### Step 3 — Extract Methodology Only
From the case, extract:
- The legal principle or test established
- The methodology or framework to apply
- Any limitations or qualifications on the principle

Do NOT extract:
- Factual findings specific to that case (these do not apply to new applications)
- Outcome (what the authority decided) as precedent for the same outcome here

### Step 4 — Apply to Current Facts
Apply the case methodology to the current application's specific facts:
- Reference the case for the framework
- Apply the framework to the current venue, locality, and applicant
- Reach a reasoned conclusion based on the current facts

### Step 5 — Cite Correctly
```
Format: (Source: Case_Precedent_Compendium.md — [Case Name/Reference])

Example: "Applying the four-step harm assessment framework established in
Carnegies (LC28/2015) (Source: Case_Precedent_Compendium.md — Carnegies
LC28/2015), the Applicant submits as follows..."
```

---

## What Case Law Cannot Do

Case law in a PIA submission **cannot:**

- Override a statutory provision in the Liquor Control Act 1988
- Override a Director's Policy requirement
- Establish that an application must be approved
- Guarantee any particular outcome
- Substitute for locality-specific planning evidence
- Replace the need for venue-specific factual evidence

---

## Precedent Strategy by Application Type

### Tavern Restricted Application
Primary cases: Carnegies (harm), Sand Volley (objects of Act)
Supporting: Pilbara s.64 (if conditions proposed)

### Hotel Application
Primary cases: Carnegies (harm), Sand Volley (objects of Act)
Supporting: WASC 128 (locality definition)

### Packaged Liquor Application
Primary cases: Liquorland Karrinyup (consumer requirements), WASC 128 (locality)
Supporting: Carnegies (harm), Tokyo Mart (if cultural community basis)

### Small Bar / Restaurant ETP
Primary cases: Sand Volley (public benefit), Carnegies (harm)
Supporting: Pilbara s.64 (proportionate conditions)

### Objection Response
All cases potentially relevant depending on grounds of objection.
Identify the objection's legal basis first, then select the applicable
precedent framework to rebut.

---

## Common Errors in Case Law Application (Stage 1 + Stage 2 inputs)

Stage 1 (`lla-citation-checker`) and Stage 2 (`lla-compliance-checker`) both
audit these. Catching them in-draft saves rework.

```
□ Citing case outcome as precedent for same outcome (incorrect)
□ Using case law to override legislation (incorrect — Tier 1 always prevails)
□ Citing Director's Policy cases as binding law (incorrect)
□ Applying case methodology without adapting to current facts (lazy application)
□ Citing cases from memory without checking Case_Precedent_Compendium.md
□ Over-relying on one case when multiple cases apply
□ Citing interstate or federal cases without noting WA applicability
```


---

**System Version:** 1.1 — Two-stage pre-delivery gate wired
**Last Updated:** 21 May 2026
