# Jurisdiction Citation Map

**Status:** Locked master standard
**Last updated:** 21 May 2026
**Owner:** HTS / lla-citation-checker

This file is the source of truth for which authorities are valid for which jurisdiction. The `apply_stale_registry.py` and `audit_report.py` scripts consult this map to enforce cross-jurisdictional citation discipline.

Why it matters: a NSW SoRPE that cites Carnegies (a WA case) is professionally embarrassing and analytically wrong (the WA case applies a different statutory framework). The lla-citation-checker FAILs any out-of-jurisdiction citation so this never reaches lodgement.

---

## NSW authorities (valid in NSW drafts only)

| Authority | Citation pattern | Notes |
|---|---|---|
| Liquor Act 2007 (NSW) | `*Liquor Act 2007* (NSW), s.X` | Primary statute |
| Liquor Regulation 2018 (NSW) | `*Liquor Regulation 2018* (NSW), cl.X` | Primary regulation |
| Gaming and Liquor Administration Act 2007 (NSW) | `*Gaming and Liquor Administration Act 2007* (NSW), s.X` | Procedural / ILGA establishment |
| ILGA Guidelines (1–17) | `ILGA Guideline N — Title (DD Month YYYY)` | Authoritative guidance from decision body |
| L&GNSW operational pages | `L&GNSW, [Page] (nsw.gov.au)` | Operational guidance |
| ILGA decisions | `ILGA Decision: [Case] (DD Month YYYY)` | Tier 4 precedent |
| NCAT decisions | `NCAT: [Case] (DD Month YYYY)` | Merits review |
| NSW Supreme Court (s.69 *Supreme Court Act 1970* judicial review) | `NSW Supreme Court: [Case] (DD Month YYYY)` | Judicial review |
| Sydney LEP 2012 / Sydney DCP 2012 | `Sydney LEP 2012, clause X` | LGA planning |
| Other NSW LGA planning instruments | `[LGA] LEP YYYY` or `[LGA] DCP YYYY` | LGA-locked |
| BOCSAR | `BOCSAR Crime Tool, [Area], [metric] [period]` | Crime statistics |
| NSW Health (HealthStats) | `NSW Health HealthStats, [Area]` | Health data |
| TfNSW Centre for Road Safety | `TfNSW Centre for Road Safety, [period]` | Road safety data |
| Data After Dark | `Office of the 24-Hour Economy Commissioner, Data After Dark, [period]` | Night-time economy |

## WA authorities (valid in WA drafts only)

| Authority | Citation pattern | Notes |
|---|---|---|
| Liquor Control Act 1988 (WA) | `*Liquor Control Act 1988* (WA), s.X` | Primary statute |
| Liquor Control Regulations 1989 (WA) | `*Liquor Control Regulations 1989* (WA), reg.X` | Primary regulation |
| Director's Policies | `Director's Policy (Guidance) — [Title], paragraph X` | Authoritative guidance |
| Carnegies (LC28/2015) | `Carnegies (LC28/2015)` | Master harm framework case |
| Sand Volley | `Sand Volley` | WA precedent |
| Pilbara s.64 | `Pilbara s.64` | WA precedent |
| Liquorland Karrinyup (WASC 366) | `Liquorland Karrinyup (WASC 366)` | WA precedent |
| WA Local Planning Schemes | `[Shire / City of X] LPS No. N (AMD M)` | LGA planning |
| WA Local Planning Policies | `[Shire / City of X] LPP — [Policy Title]` | LGA planning |
| WA Local Planning Strategies | `[Shire / City of X] Local Planning Strategy` | LGA planning |

## Jurisdiction-agnostic authorities (valid in any draft)

| Authority | Citation pattern | Notes |
|---|---|---|
| Australian Bureau of Statistics (ABS) | `ABS [Dataset YYYY], [Area]` | Census, SEIFA, Quickstats |
| Australian Institute of Health and Welfare | `AIHW [Publication], [Year]` | National health data |
| AIC (Australian Institute of Criminology) | `AIC [Publication / Monograph], [Year]` | Criminology research |
| Centre for Disease Control and Prevention | `CDC [Publication YYYY]` | International — use sparingly |
| Peer-reviewed research (Livingston, Jiang, Donnelly, Morrison etc) | `Author et al. (YYYY)` | From ILGA Guideline 6 Annexure A or equivalent |
| Federal Acts (Commonwealth) | `*Act Name Year* (Cth), s.X` | Where genuinely relevant |

---

## Cross-jurisdiction FAIL rules

The lla-citation-checker FAILs any citation that matches a wrong-jurisdiction pattern:

| Source jurisdiction | Forbidden cite in | Result |
|---|---|---|
| Carnegies (LC28/2015) | NSW draft | FAIL — wrong jurisdiction; use ILGA Guideline 6 / s.48 instead |
| Sand Volley, Pilbara s.64, Liquorland Karrinyup | NSW draft | FAIL — WA cases only |
| Director's Policy | NSW draft | FAIL — Director's Policy is a WA instrument; use ILGA Guidelines |
| WA LPS / LPP citations | NSW draft | FAIL — wrong state |
| ILGA Guideline references | WA draft | FAIL — ILGA is the NSW authority |
| ILGA Decisions / NCAT decisions | WA draft | FAIL — wrong jurisdiction |
| Liquor Act 2007 (NSW) | WA draft | FAIL — wrong state |
| Liquor Control Act 1988 (WA) | NSW draft | FAIL — wrong state |
| NSW LEP / DCP citations | WA draft | FAIL — wrong state |
| Sydney CBD Entertainment Precinct conditions | WA draft | FAIL — NSW-specific overlay |

---

## How to update this map

When HTS expands to a new state (e.g., VIC, QLD):
1. Add a new section for that state's authorities (parallel structure to the NSW / WA sections above)
2. Add cross-jurisdiction FAIL rules for the new state's authorities
3. Increment the "Last updated" date
4. Update the lla-citation-checker tests to confirm new categories are recognised
