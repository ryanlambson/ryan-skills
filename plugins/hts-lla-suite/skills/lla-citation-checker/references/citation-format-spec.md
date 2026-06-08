# HTS Citation Format Specification

**Status:** Locked master standard for the HTS LLA family
**Last updated:** 21 May 2026
**Owner:** HTS / lla-citation-checker

This file is the source of truth for what a valid citation looks like in any HTS LLA work product (PIA, SoRPE, LPoM, ETA, submission, NCAT review, objection response).

The lla-citation-checker `extract_citations.py` script uses the patterns below to parse citations from drafts. The lla-gpt and lla-gpt-nsw drafting skills are expected to produce citations in this format.

---

## The four absolute rules

1. **Every factual claim must be cited.** Uncited claims are flagged as WARN by the lla-citation-checker.
2. **No footnotes.** All citations are inline, in the format below.
3. **No placeholder citations.** `(Source: TBD)` or `[citation needed]` are FAILs.
4. **Quote verbatim from legislation.** Paraphrasing a section is permitted only when the quotation appears within the same paragraph.

---

## Citation categories (matching SKILL.md Section 5)

### 5.1 — Project knowledge file reference

```
(Source: FILENAME.md, Section X)
(Source: FILENAME.md)         ← acceptable for whole-file reference
```

**Rules:**
- Filename must include `.md` extension
- Filename uses ALL_CAPS_WITH_UNDERSCORES or PascalCase per HTS convention
- Section reference is optional; if provided, must match an actual heading in the file
- Example: `(Source: LEGISLATION_LiquorAct2007_NSW_HOTEL.md, Section 7)`

### 5.2 — Legislation

```
*Act Name Year* (STATE), s.N(M)
```

**Rules:**
- Act name in italics (Markdown `*...*` or Word italic)
- State in parentheses immediately after the title (e.g., `(NSW)`, `(WA)`, `(Cth)`)
- Section reference with `s.` prefix (preferred) or `section` word form
- Examples:
    - `*Liquor Act 2007* (NSW), s.48(3)`
    - `*Liquor Act 2007* (NSW), s.11A`
    - `*Liquor Control Act 1988* (WA), s.38(4)`
    - `*Gaming and Liquor Administration Act 2007* (NSW), s.36C`

### 5.3 — Regulations

```
*Regulation Name Year* (STATE), cl.N
*Regulation Name Year* (STATE), reg.N
```

**Rules:**
- Same italics + state pattern as 5.2
- Use `cl.` for clauses (NSW convention) or `reg.` for regulations (WA convention)
- Examples:
    - `*Liquor Regulation 2018* (NSW), cl.27`
    - `*Liquor Control Regulations 1989* (WA), reg.7`

### 5.4 — ILGA Guidelines (NSW only)

```
ILGA Guideline N — Title (DD Month YYYY), paragraph X
```

**Rules:**
- Always include the Guideline number
- Title is optional but recommended for first reference; subsequent references can omit
- Publication date is REQUIRED — format `DD Month YYYY` (e.g., `10 March 2025`)
- Paragraph reference is optional; recommended for specific points
- Examples:
    - `ILGA Guideline 6 — Consideration of overall impact under section 48(3) of the Liquor Act 2007 (10 March 2025), paragraph 1.1`
    - `ILGA Guideline 3 (March 2025)`

**Currency rule:** the lla-citation-checker WARNs if the publication date is more than 12 months old. ILGA Guidelines are updated periodically.

### 5.5 — Director's Policies (WA only)

```
Director's Policy (Guidance) — [Title], paragraph X
```

**Rules:**
- ALWAYS label as "(Guidance)" — Director's Policies are not law
- Title is recommended
- Paragraph reference optional
- Jurisdiction lock: only valid in WA drafts. NSW drafts citing Director's Policy → FAIL.

### 5.6 — L&GNSW operational guidance (NSW only)

```
L&GNSW, [Page Title] (nsw.gov.au), [element]
```

**Rules:**
- "L&GNSW" prefix
- Page title in plain text
- "(nsw.gov.au)" parenthetical to mark it as operational guidance
- Optional element (e.g., "Trading hours table", "Notification table")
- Examples:
    - `L&GNSW, Hotel licence page (nsw.gov.au), Trading hours table`
    - `L&GNSW, Notifying stakeholders page (nsw.gov.au)`

**Jurisdiction lock:** only valid in NSW drafts.

### 5.7 — Case law

**WA cases (in WA drafts only):**
```
Carnegies (LC28/2015)
Sand Volley
Pilbara s.64
Liquorland Karrinyup (WASC 366)
```

**NSW cases (in NSW drafts only):**
```
ILGA Decision: [Case Name] (DD Month YYYY)
NCAT: [Case Name] (DD Month YYYY)
NSW Supreme Court: [Case Name] (DD Month YYYY)
```

**Jurisdiction lock:** WA-only cases in NSW drafts → FAIL. NSW-only authorities in WA drafts → FAIL.

### 5.8 — Planning instruments

```
[LGA Name] LEP YYYY, clause N
[LGA Name] DCP YYYY, section N
[LGA Name] LPS No. N (AMD M)
[LGA Name] LPP — [Policy Title]
```

**Rules:**
- LGA name in HTS-standard form (e.g., "Sydney", "Shire of Augusta Margaret River", "City of Vincent")
- Instrument type: LEP (NSW), DCP (NSW), LPS (WA), LPP (WA), LPS amendment (WA)
- Year for current LEP/DCP/LPS; amendment number for LPS variants
- LGA-match rule: instruments must match the project's locked locality. Cross-LGA citations → FAIL.

### 5.9 — Data citations

**BOCSAR:**
```
BOCSAR Crime Tool, [Area], [metric] [period]
```

**ABS:**
```
ABS [Dataset], [Area], [element]
```

**NSW Health:**
```
NSW Health [Source], [Area]
```

**TfNSW / DOH / other:**
Use parallel structure.

**Rules:**
- Source / dataset / Area / period are all REQUIRED
- Period within last 5 years (else WARN — refresh)

### 5.10 — Web URLs

```
https://example.com/path
```

**Rules:**
- Must be well-formed HTTP/HTTPS URL
- No bare-text URLs without the scheme
- Live URLs only — anchor URLs (`#section`) are acceptable

---

## Special cases

### Combined citation (multiple sources for one claim)

Acceptable. Use a sequence within the same parenthetical:

```
(Source: LEGISLATION_LiquorAct2007_NSW_HOTEL.md, Section 7; ILGA Guideline 6, paragraph 1.1)
```

### Inline section quote

If a section is quoted, the citation immediately follows:

```
"The Authority must not grant a licence (other than a producer/wholesaler licence) unless the Authority is satisfied that the overall impact of the licence being granted will not be detrimental to the wellbeing of the local or broader community" (*Liquor Act 2007* (NSW), s.48(3)).
```

### Attachment references

```
Attachment N — [Description]
```

Examples:
- `Attachment 1 — Floor Plan, Level 25 Rooftop Bar`
- `Attachment 7 — ASIC Extract, Fiveight OCQ Operations Pty Ltd`

Attachment references are NOT citations to authority; they are pointers to bundled evidence. The lla-citation-checker recognises and skips them.

---

## What is NOT a valid citation

- `(Source: see below)` — placeholder
- `(Source: the Act)` — too vague
- `as discussed above` — not a citation
- `the Authority's policy` — must name the policy
- `recent research` — must name the research
- `BOCSAR data` (without area, metric, period) — incomplete
- Bare hyperlinks without context — see 5.10 rules
- Carnegies in a NSW draft (wrong jurisdiction)
- ILGA Guideline 6 in a WA draft (wrong jurisdiction)
- Cited section that doesn't exist in the cited Act
