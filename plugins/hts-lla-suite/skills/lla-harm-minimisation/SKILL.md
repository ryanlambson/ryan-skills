---
name: lla-harm-minimisation
description: >
  HTS harm minimisation drafting tool for Section 7 and related harm sections
  of Western Australian liquor licence PIAs. Use this skill whenever drafting
  or reviewing harm minimisation content, the Carnegies four-step assessment,
  s.38(4)(a) harm or ill-health arguments, s.38(4)(b) amenity impacts,
  s.38(4)(c) offence and annoyance, harm mitigation measures, management plans,
  CPTED strategies, responsible service of alcohol content, or any content
  addressing alcohol-related harm in a licensing submission. Also trigger for
  requests to "write the harm section", "do the Carnegies assessment", "what
  mitigation measures should we include", "draft the RSA content", or any
  instruction to address harm in a PIA. This skill ensures every risk is
  paired with a mitigation measure and that evidence is correctly sourced
  from knowledge modules without elevating them above their authority tier.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.1.0
  category: harm-assessment
---

# LLA Harm Minimisation — Section 7 Drafting Workflow

## Purpose

This skill governs the drafting of harm minimisation content for HTS PIAs.
It applies the Carnegies four-step framework systematically, draws correctly
from knowledge modules, and ensures every identified risk concludes with a
specific, venue-appropriate mitigation measure.

---

## Pre-Delivery Gate (MANDATORY)

Harm minimisation content cites Case_Precedent_Compendium.md (Carnegies),
KNOWLEDGE files, ABS / AIHW / AIC / NSW Health data, and the locked LGA's
planning controls. All these are exactly what the HTS two-stage pre-delivery
gate verifies:

1. **Stage 1 — lla-citation-checker.** Confirms every Carnegies, KNOWLEDGE,
   data, and planning citation resolves to a real source and is formatted
   correctly.
2. **Stage 2 — lla-compliance-checker.** Confirms Carnegies four-step
   framework applied with explicit conclusions, every risk has a mitigation
   measure, and no knowledge module has been elevated to authority status.

Run Stage 1 before Stage 2. The Drafting Checklist at the bottom of this
skill is Stage 2 input.

---

## MANDATORY: Knowledge Module Status

Knowledge modules are **Tier 6 — Supporting Evidence Only**.

```
KNOWLEDGE_HarmMinimisation.md   → evidence base for mitigation strategies
KNOWLEDGE_AlcoholInformation.md → alcohol research and public health data
KNOWLEDGE_AlcoholAdvertising.md → responsible promotion and advertising controls
KNOWLEDGE_EntertainmentNoise.md → noise management for amenity sections
```

**Rules:**
- Never cite knowledge modules as binding requirements
- Never use knowledge modules to override planning instruments or legislation
- Citation format: "Based on the evidence outlined in [KNOWLEDGE_FILE.md, Section X]…"
- Knowledge modules support arguments — they do not make arguments

---

## Step 1 — Establish the Locality Harm Profile

Before assessing this application's harm, establish what harm already
exists in the locality. Sources:

- LGA planning documents (existing licensed premises data)
- KNOWLEDGE_HarmMinimisation.md (general harm patterns)
- KNOWLEDGE_AlcoholInformation.md (population-level data)
- Any locality-specific data provided by the applicant

**Draft content for:**
- Existing licensed premises in the locality (number, type, proximity)
- Known harm indicators (if available from public sources)
- Population characteristics relevant to harm risk
- Any existing harm minimisation infrastructure in the locality

Cite every claim. Do not assume or invent locality harm data.

---

## Step 2 — Apply the Carnegies Four-Step Framework

Source: `Case_Precedent_Compendium.md — Carnegies LC28/2015`

### Step 1: Identify Existing Harm in the Locality

Draft content addressing:
- Current licensed premises density and their operating profiles
- Any known or documented alcohol-related incidents in the area
- Vulnerable population groups in the locality
- Existing harm minimisation measures in place

### Step 2: Identify Likely Harm from This Application

For this specific venue, assess:
- Patron profile (who will use this venue)
- Trading hours and peak periods
- Venue type and its associated harm patterns
- Proximity to sensitive uses (residential, schools, transport hubs)
- Any specific risk factors for this application

### Step 3: Compare Likely Harm Against Existing Harm

- Is the likely harm from this venue additive to existing harm?
- Is it of the same type or a different character?
- Does this venue's operating model reduce, maintain, or increase
  the locality's overall harm profile?

### Step 4: Weigh Harm Against Public Interest Benefits

- What public interest benefits does this venue provide?
  (tourism, employment, community amenity, service to unmet need)
- Do the benefits outweigh the harm?
- Is the net public interest outcome positive?

**Conclusion:** Each step must reach an explicit conclusion.
Each identified harm must link to a specific mitigation measure.

---

## Step 3 — Mitigation Measures Library

Draw from `KNOWLEDGE_HarmMinimisation.md` for evidence-based measures.
Adapt each measure to this specific venue — no generic lists.

### Responsible Service of Alcohol

```
□ RSA-trained staff — all service staff hold current RSA certification
□ Management holds RSA certification (Approved Manager level)
□ RSA signage displayed at service points
□ House policy for identifying and managing intoxicated patrons
□ Refusal of service procedures documented in Management Plan
□ Incident register maintained and reviewed
```

### Patron Management

```
□ Capacity limit enforced — [X] persons maximum
□ Entry/exit management during peak periods
□ CCTV coverage of entry, gaming area, outdoor areas
□ Security personnel during [specified hours] — licensed crowd controllers
□ Patron transport information displayed (taxi ranks, public transport)
□ Water available at all times, free of charge
□ Food available during all trading hours
```

### CPTED Strategies (Crime Prevention Through Environmental Design)

```
□ Clear sightlines — staff can observe all areas
□ Lighting adequate — interior and exterior (lux levels per AS1158)
□ No concealed areas that limit supervision
□ Outdoor areas visible from street and interior
□ CCTV coverage with [X] days retention
□ Entry/exit design limits conflict points
```

Source: `KNOWLEDGE_HarmMinimisation.md` — CPTED section

### Hours Management

```
□ Trading hours limited to [proposed hours]
□ Last drinks called [X] minutes before close
□ Staggered departure procedures during close
□ No alcohol service in the [X] minutes before venue close
□ Extended trading only by ETP (if applicable)
```

### Advertising and Promotions

```
□ No irresponsible promotions — no shouting, no rapid consumption events
□ Discount alcohol promotions not conducted
□ Promotions comply with ABAC Responsible Alcohol Marketing Code
□ No advertising targeting minors or depicting excessive consumption
```

Source: `KNOWLEDGE_AlcoholAdvertising.md`

### Community and Industry Engagement

```
□ Liaison with local police on harm reduction
□ Participation in local liquor accord (if applicable)
□ Community complaints procedure documented and published
□ Neighbour notification protocol in place
```

---

## Step 4 — Amenity Section (s.38(4)(b))

Address amenity impacts from noise, patron behaviour, and operating hours.

### Noise Management

Source: `KNOWLEDGE_EntertainmentNoise.md`

```
□ Acoustic assessment (if live music or amplified sound proposed)
□ Compliance with Environmental Protection (Noise) Regulations 1997
□ Building envelope noise attenuation measures
□ Operational noise controls (glass handling, outdoor area management)
□ Noise complaint response procedure
□ Trading hours limited to reduce late-night noise impact
```

### Interface with Sensitive Uses

Identify any sensitive uses near the premises:
- Residential dwellings within [distance]
- Schools, childcare centres
- Places of worship
- Hospitals or medical centres

For each sensitive use, address how the venue's operations will
not unreasonably impact amenity.

Source: LGA planning pack — amenity and interface provisions

---

## Step 5 — Management Plan Integration

Harm minimisation content must be consistent with and supported by
the Management Plan (if separately prepared).

Key Management Plan elements that must align with harm sections:
- RSA training requirements
- Security arrangements
- Incident management procedures
- Hours of operation
- Patron capacity

Flag any inconsistencies between PIA harm content and Management Plan.

---

## Drafting Checklist — Harm Sections (Stage 2 inputs)

Run Stage 1 (`lla-citation-checker`) first. This checklist is verified by
Stage 2 (`lla-compliance-checker`) before the harm section ships.

```
□ Carnegies four-step framework applied with explicit conclusions at each step
□ Existing locality harm profile established with cited evidence
□ Likely harm from this application identified specifically (not generically)
□ Every identified risk concludes with a specific mitigation measure
□ Mitigation measures are venue-specific — not a generic list
□ Knowledge modules cited as evidence only ("Based on evidence outlined in…")
□ Knowledge modules NOT cited as binding requirements
□ Carnegies cited: (Source: Case_Precedent_Compendium.md — Carnegies LC28/2015)
□ CPTED measures address the specific venue layout
□ RSA content reflects actual staffing and management arrangements
□ Hours content is consistent with trading hours stated elsewhere in PIA
□ Capacity content is consistent with floor plan and patron capacity stated elsewhere
□ Amenity section addresses all sensitive uses identified in Section 2 (Locality)
□ No generic statements — every claim is specific to this venue and locality
```


---

**System Version:** 1.1 — Two-stage pre-delivery gate wired
**Last Updated:** 21 May 2026
