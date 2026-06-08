# HTS Document Style Guide
## Hospitality Total Services (Aus) Pty Ltd
### Version 1.0 — CONFIRMED MASTER STANDARD
### Derived from forensic XML analysis of LB Safety Bay PIA & Last Slice Kwinana PIA
### Confirmed by Ryan — April 2026

---

## STATUS: LOCKED FOR PRODUCTION USE

This document is the confirmed master formatting standard for all HTS documents generated
by the LLA GPT system. All specifications have been verified against source documents and
confirmed by Ryan. Do not modify without explicit instruction.

---

## 1. PAGE SETUP

| Setting | Value | Notes |
|---|---|---|
| Paper Size | A4 | 11906 × 16838 DXA — NOT US Letter |
| Dimensions | 8.268" × 11.693" | ISO A4 |
| Language | en-AU | Australian English — enforced at document level |
| Top Margin | 1.181" (1700 DXA) | 30mm — symmetric standard |
| Bottom Margin | 1.181" (1700 DXA) | 30mm |
| Left Margin | 1.181" (1700 DXA) | 30mm |
| Right Margin | 1.181" (1700 DXA) | 30mm |
| Header distance | 0.094" (135 DXA) | Very tight — header sits close to top edge |
| Footer distance | 0.388" (558 DXA) | |

**Implementation note:** Always set page size explicitly in docx-js.
A4 in DXA: `width: 11906, height: 16838`
Content width with 30mm margins: `11906 - 1700 - 1700 = 8506 DXA`

---

## 2. TYPOGRAPHY — BASE DOCUMENT

| Property | Value | DXA / Half-points |
|---|---|---|
| Body font | Calibri | `minorHAnsi` theme alias |
| Body size | 12pt | `w:sz val="24"` |
| Body alignment | Justified (both edges) | `w:jc val="both"` |
| Body line spacing | 1.15× automatic | `w:line="276" w:lineRule="auto"` |
| Body space after | 80pt standard / 60pt tight | Per paragraph |
| Language | en-AU | `w:lang val="en-AU"` |

**Font resolution:**
- `majorHAnsi` theme alias → **Cambria** (all headings)
- `minorHAnsi` theme alias → **Calibri** (body text)

Use explicit font names (`Cambria`, `Calibri`, `Arial`) in generated documents
rather than theme aliases to ensure consistent rendering.

---

## 3. HEADING HIERARCHY

### Colour Palette

| Name | Hex | Usage |
|---|---|---|
| HTS Navy | #002060 | H1 — primary section headings |
| HTS Mid-Blue | #4F81BD | H2, H3, H4 — sub-headings |
| Black | #000000 | H6 — special use headings |
| White | #FFFFFF | Heading 8/9 — inverted/table headers |

### Heading Specifications

| Level | Font | Size | Size (half-pts) | Weight | Colour | Underline | Space Before | Space After | Numbered |
|---|---|---|---|---|---|---|---|---|---|
| H1 | Cambria | 18pt | `val="36"` | Bold | #002060 | Double | 24pt | 12pt | Yes — sequential |
| H2 | Cambria | 16pt | `val="32"` | Bold | #4F81BD | None | 10pt | 6pt | Yes — `1.1` format |
| H3 | Cambria | 14pt | `val="28"` | Bold | #4F81BD | None | 10pt | 6pt | Yes — `1.1.1` format |
| H4 | Cambria | 14pt | `val="28"` | Bold + Italic | #4F81BD | None | 10pt | 0pt | Optional |

### Numbering Pattern

```
Level 0 (H1):  1.   2.   3.   ...  (decimal, trailing period)
Level 1 (H2):  1.1  1.2  1.3  ...  (decimal, dot-separated)
Level 2 (H3):  1.1.1  1.1.2  ...   (decimal, dot-separated)
```

**Numbering indent configuration:**
```
H1: left=0.500" (720 DXA), hanging=0.250" (360 DXA)
H2: left=0.750" (1080 DXA), hanging=0.250" (360 DXA)
H3: left=1.000" (1440 DXA), hanging=0.500" (720 DXA)
```

**Implementation note:** Use a single continuous numbering list across the
entire document. Each section document (when generating in parts) must declare
its correct `start` value so the final compiled document has sequential numbering.
This is a required input variable per section — see Section 15.

### H1 Underline — Double Underline

H1 headings use **double underline** (`w:u w:val="double"`). This is NOT a
paragraph border — it is a character-level double underline on the heading text.
This is confirmed intentional HTS formatting.

---

## 4. BODY TEXT

### Standard Body Paragraph

| Property | Value | Notes |
|---|---|---|
| Font | Calibri | Explicit — do not rely on inheritance |
| Size | 12pt (`val="24"`) | Explicit on all body runs |
| Line spacing | 1.15× auto | `line="276" lineRule="auto"` |
| Alignment | Justified | `jc="both"` |
| Space after | 80pt standard | `val="1600"` in twips (80×20) |
| Space after | 60pt tight | `val="1200"` |
| Space after | 30pt compact | `val="600"` |

### Legislative Text (Verbatim Quotations)

Quoted statutory provisions use progressive indentation matching the
legislative subsection structure:

| Level | Indent Left | Notes |
|---|---|---|
| Section (top) | 0.099" | e.g., `s.38(4)` |
| Subsection | 0.492" | e.g., `(1)` |
| Paragraph | 0.690" | e.g., `(a)` |
| Sub-paragraph | 0.985" | e.g., `(i)` |

Font: Calibri 12pt, justified, space-after 60pt.

### Indented Submission Paragraphs

For formal submission paragraphs that are subordinate to numbered headings:

| Property | Value |
|---|---|
| Style | `ListParagraph` |
| Font | Calibri 12pt |
| Indent left | 0.394" (matches H1 numbering overhang) |
| Space after | 80pt |
| Line spacing | 1.15× |

---

## 5. HEADER

Appears on every page. Single line, centred.

| Property | Value |
|---|---|
| Content | `Prepared by Hospitality Total Services (Aus) Pty Ltd on behalf of [CLIENT_LEGAL_ENTITY]` |
| Font | Calibri |
| Size | 10pt (`val="20"`) |
| Alignment | Centre (`jc="center"`) |
| Style | Plain — no bold, no underline, no colour |
| Distance from top | 0.094" (135 DXA) |

**Variable:** `CLIENT_LEGAL_ENTITY` — required input, changes per application.
Example: "Waikiki Hotel (WA) Pty Ltd"

---

## 6. FOOTER

Two elements on every page.

### Element 1 — Page Number

| Property | Value |
|---|---|
| Content | Auto page number field (not static) |
| Alignment | Right (`jc="right"`) |
| Font | Calibri 11pt (inherited) |
| Format | Numeric only — no "Page X of Y" |

**Implementation:** Use Word `PAGE` field code (`w:fldChar` + `w:instrText` with `PAGE`),
not a static number.

### Element 2 — Website

| Property | Value |
|---|---|
| Content | `www.hospitalitytotalservices.com.au` |
| Alignment | Centre (`jc="center"`) |
| Font | Calibri 11pt (inherited) |
| Format | Plain text — not a hyperlink |

---

## 7. FOOTNOTES & CITATIONS

This is the most distinctive HTS formatting element. The system uses
**inline numbered references** — not standard Word superscripts.

### Footnote Reference (In Body Text)

| Property | Value | Implementation |
|---|---|---|
| Format | Inline number in square brackets e.g. `[1]` | `w:footnoteReference` |
| Size | 12pt | `w:sz val="24"` — explicit, matches body |
| Vertical alignment | Baseline | `w:vertAlign` NOT set — no superscript |
| Appearance | Full-size number, same baseline as surrounding text | Confirmed intentional |

**Critical:** Do NOT use `w:vertAlign val="superscript"`. The reference number
sits on the same baseline as body text at 12pt. This is a deliberate legal
document convention.

### Footnote Text (Footnote Area at Bottom of Page)

| Property | Value |
|---|---|
| Font | Arial | **Explicit — not inherited** |
| Size | 10pt (`val="20"`) | Smaller than body to distinguish |
| Line spacing | Single (default) | |
| Space after | 0pt | Tight footnote area |

### Hyperlink Style in Footnotes

| Property | Value |
|---|---|
| Colour | #0000FF (blue) for web URLs | |
| Underline | None | Non-standard but confirmed — blue text only, no underline |
| Style | `Hyperlink` character style | |
| Font | Arial 10pt (inherited from footnote) | |

### Footnote Content Types

**Type 1 — URL citation:**
Hyperlinked URL pointing to legislation, government publications, planning
documents, or other web resources.
Format: `[display text as URL or descriptive text]`

**Type 2 — Attachment reference:**
Plain text reference to a submitted attachment.
Format: `Attachment [N] — [Description]`
Example: `Attachment 2 — City of Kwinana Local Commercial and Activity Centre Strategy`
No hyperlink. Same Arial 10pt style.

---

## 8. TABLE OF CONTENTS

| Property | Value |
|---|---|
| Heading text | **"Contents"** |
| Heading style | `TOCHeading` — Cambria 18pt, Bold, #002060, double underline |
| TOC1 | Cambria 14pt, Bold, space-before 12pt, space-after 6pt, hanging 0.788" |
| TOC2 | Calibri 10pt, Italic, space-before 6pt, indent 0.153" |
| TOC3 | Calibri 10pt, indent 0.306" |
| TOC4–TOC9 | Calibri 10pt, progressive indent (additional 0.153" per level) |

---

## 9. COVER PAGE

Standard structure for all HTS PIA documents. Elements in order:

| Element | Style | Font | Size | Alignment | Notes |
|---|---|---|---|---|---|
| Document type | `BodyText3` | Cambria | 22pt | Left, offset | e.g., "Public Interest Assessment" |
| Sub-type | `BodyText3` | Cambria | 16pt | Left, offset | e.g., "Conditional Grant of a Tavern Restricted Licence" |
| Premises Name | `Normal` | Calibri | 14pt | Left, offset | `Premises Name: [TRADING_NAME]` |
| Applicant | `Normal` | Calibri | 12pt | Left, offset | `Applicant: [CLIENT_LEGAL_ENTITY]` |
| Location | `Normal` | Calibri | 12pt | Left, offset | `Location: [PREMISES_ADDRESS]` |
| Spacer | `Normal` | — | — | — | Empty paragraph |
| "Prepared by:" | `Normal` | Calibri | 12pt | Centre | |
| HTS address | `Normal` | Calibri | 8pt | Centre | `Office 2, 48 Kishorn Road, Applecross WA 6153` |
| Copyright notice | `Normal` | Calibri | 11pt | Centre | "This Submission is not to be copied in part or its entirety…" |

---

## 10. LISTS & BULLET POINTS

| List Type | Format | Left indent | Hanging | Level |
|---|---|---|---|---|
| Bullet (primary) | Filled circle • | 0.500" (720 DXA) | 0.250" (360 DXA) | 0 |
| Bullet (secondary) | Open circle ○ | 1.000" (1440 DXA) | 0.250" (360 DXA) | 1 |
| Bullet (tertiary) | Square ▪ | 1.500" (2160 DXA) | 0.250" (360 DXA) | 2 |
| Numbered (primary) | `1.` decimal | 0.500" (720 DXA) | 0.250" (360 DXA) | 0 |
| Numbered (sub) | `1.1` decimal | 0.750" (1080 DXA) | 0.250" (360 DXA) | 1 |
| Alpha | `a.` lowerLetter | 1.000" (1440 DXA) | 0.250" (360 DXA) | 1 |
| Roman | `i.` lowerRoman | 1.500" (2160 DXA) | 0.125" (180 DXA) | 2 |

**Implementation:** Never use Unicode bullet characters. Use `LevelFormat.BULLET`
with proper numbering config in docx-js. See docx skill for implementation pattern.

---

## 11. TABLES

| Property | Value |
|---|---|
| Cell font | Calibri 12pt |
| Cell spacing | Before 1.8pt, line=247 exact |
| Cell alignment | Left (default — override per column as needed) |
| Cell padding | `top: 80, bottom: 80, left: 120, right: 120` |
| Table width | DXA (fixed) — never percentage |
| Border style | `BorderStyle.SINGLE`, size 1, colour #CCCCCC |
| Header row shading | `ShadingType.CLEAR`, fill #002060 (navy), text white |
| Width basis | Content width: 8506 DXA (A4 with 30mm margins) |

**Critical:** Always set both `columnWidths` on the table AND `width` on each
cell. Use `ShadingType.CLEAR` — never SOLID for table shading.

---

## 12. COLOUR REFERENCE

| Name | Hex | Usage |
|---|---|---|
| HTS Navy | #002060 | H1, TOC heading, table headers |
| HTS Mid-Blue | #4F81BD | H2, H3, H4 |
| Black | #000000 | H6, body text |
| Hyperlink Blue | #0000FF | URLs in footnotes |
| Visited Hyperlink | #800080 | Followed hyperlinks |
| White | #FFFFFF | Inverted headings (H8/H9), table header text |
| Light Grey | #CCCCCC | Table borders |

---

## 13. FULL STYLE QUICK REFERENCE

```
DOCUMENT
  Paper:      A4  (11906 × 16838 DXA)
  Margins:    30mm all sides (1700 DXA each)
  Language:   en-AU

FONTS
  Headings:   Cambria  (majorHAnsi)
  Body:       Calibri  (minorHAnsi)
  Footnotes:  Arial

HEADING SIZES
  H1:   Cambria 18pt | Bold | #002060 | Double underline | Numbered (1.)
  H2:   Cambria 16pt | Bold | #4F81BD | No underline     | Numbered (1.1)
  H3:   Cambria 14pt | Bold | #4F81BD | No underline     | Numbered (1.1.1)
  H4:   Cambria 14pt | Bold+Italic | #4F81BD | No underline

BODY
  Font:       Calibri 12pt
  Spacing:    1.15× auto
  Alignment:  Justified
  Space after: 80pt (standard) / 60pt (tight) / 30pt (compact)

HEADER
  Text:       "Prepared by Hospitality Total Services (Aus) Pty Ltd
               on behalf of [CLIENT_LEGAL_ENTITY]"
  Font:       Calibri 10pt | Centred

FOOTER
  Left:       (empty)
  Centre:     www.hospitalitytotalservices.com.au  (Calibri 11pt)
  Right:      [PAGE NUMBER FIELD]  (Calibri 11pt)

FOOTNOTES
  Reference:  Inline 12pt, baseline (NOT superscript)
  Text:       Arial 10pt
  URLs:       Blue #0000FF, no underline
  Attachments: Plain Arial 10pt, no hyperlink

TOC
  Title:      "Contents"  (Cambria 18pt, Bold, #002060, double underline)
  TOC1:       Cambria 14pt Bold
  TOC2+:      Calibri 10pt, progressive indent
```

---

## 14. DOCUMENT GENERATION IMPLEMENTATION NOTES

Critical notes for the `lla-document-builder` skill and any generation scripts:

1. **A4 only** — Always set `width: 11906, height: 16838` in DXA. Never use US Letter.
2. **Explicit fonts** — Specify `Cambria` and `Calibri` and `Arial` directly. Do not use theme aliases.
3. **Footnote references are NOT superscripts** — Generate as `w:footnoteReference` at 12pt, no `vertAlign`.
4. **Footer page numbers use field codes** — Use `w:fldChar`/`w:instrText PAGE` sequence, not static text.
5. **H1 double underline** — Use `w:u w:val="double"` on heading text runs, not a paragraph border.
6. **Section numbering requires start values** — When generating individual sections for later stitching, the `start` value of the heading numbering list must match the section number. E.g., Section 3 starts at 3.
7. **Bullet points use numbering config** — Never insert Unicode bullet characters (`•`, `○`). Use `LevelFormat.BULLET` with proper `numbering.config` in docx-js.
8. **Table widths in DXA** — Content width is 8506 DXA. Never use `WidthType.PERCENTAGE`.
9. **Arial for footnotes is explicit** — Set on the `FootnoteText` paragraph style, not inherited.
10. **Copyright notice on cover page** — Include on every document: *"This Submission is not to be copied in part or its entirety without the prior written consent of Hospitality Total Services (Aus) Pty Ltd."*

---

## 15. REQUIRED INPUT VARIABLES PER DOCUMENT

These must be supplied before any section generation begins:

| Variable | Example | Used In |
|---|---|---|
| `CLIENT_LEGAL_ENTITY` | "Waikiki Hotel (WA) Pty Ltd" | Header (every page), cover page, body |
| `TRADING_NAME` | "Liquor Barons Safety Bay" | Cover page |
| `PREMISES_ADDRESS` | "Lot 100, 434 Safety Bay Road, Safety Bay" | Cover page, Section 2 |
| `LICENCE_TYPE` | "Tavern Restricted Licence" | Cover page title, body introduction |
| `SECTION_START_NUMBER` | `3` | Heading numbering `start` value for this section |
| `DOCUMENT_DATE` | "April 2026" | Cover page, footer if required |
| `SECTION_TITLE` | "Location and Locality" | H1 heading text |

---

## 16. SECTION STITCHING PROTOCOL

When generating documents section-by-section for later compilation:

1. **Each section is generated as a standalone `.docx`** with correct heading
   start number, full HTS header/footer, and correct styles.
2. **Final compilation** merges all sections into one document in sequence.
3. **Table of Contents** is generated last, after all sections are confirmed,
   using heading styles to auto-populate entries.
4. **Page numbers** auto-update on final compile — individual section documents
   will show partial page counts, which is expected.
5. **Footnote numbering** restarts per section during drafting. On final compile,
   footnote numbers run continuously from 1. This must be reconciled at compile stage.

---

*Prepared by LLA GPT — Forensic XML analysis of HTS source documents*
*Confirmed by Ryan — April 2026*
*Version 1.0 — LOCKED MASTER STANDARD*
