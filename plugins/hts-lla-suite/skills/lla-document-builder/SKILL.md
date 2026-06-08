---
name: lla-document-builder
description: >
  HTS document builder for Hospitality Total Services (Aus) Pty Ltd. Generates
  correctly formatted .docx files for liquor licence PIAs, submissions, and
  supporting documents using the confirmed HTS style standard. Use this skill
  whenever generating, compiling, or formatting any Word document for an LLA
  project — including individual PIA sections, cover pages, compiled full PIAs,
  objection responses, management plans, or any other HTS work product. Also
  trigger when the user asks to "produce the document", "generate the docx",
  "compile sections", "stitch together", "format the output", or requests any
  downloadable Word file. This skill enforces HTS branding, typography, and
  formatting on every document regardless of content type.
metadata:
  author: Hospitality Total Services (Aus) Pty Ltd
  version: 1.0.0
  category: document-generation
---

# LLA Document Builder — HTS Formatting Standard

## Purpose

This skill generates and formats all Word documents (.docx) produced under
the LLA GPT system. It enforces the confirmed HTS Style Standard on every
document, ensuring consistency across all PIA sections, submissions, and
supporting materials.

## MANDATORY FIRST STEP

Before writing any document generation code, read the full style specification:

```
references/HTS_Style_Guide_v1.0.md
```

This file is the authoritative source for all formatting decisions. Do not
rely on memory or assumption for any typographic value — always read the
spec first.

Also read the docx skill at `/mnt/skills/public/docx/SKILL.md` before writing
any generation code.

---

## Document Types

This skill handles three document modes:

### Mode 1 — Single Section
Generate one PIA section as a standalone `.docx`.
Required inputs: section number, section title, section content, client variables.

### Mode 2 — Full Document Compile
Stitch multiple approved sections into one complete `.docx`.
Required inputs: all section files in order, TOC instruction.

### Mode 3 — Supporting Document
Generate non-PIA documents (objection responses, management plans, ETPs).
Required inputs: document type, content, client variables.

---

## Required Client Variables (Request Before Generating)

If any of these are missing, stop and ask before proceeding:

```
□ CLIENT_LEGAL_ENTITY   — e.g., "Waikiki Hotel (WA) Pty Ltd"
□ TRADING_NAME          — e.g., "Liquor Barons Safety Bay"
□ PREMISES_ADDRESS      — e.g., "Lot 100, 434 Safety Bay Road, Safety Bay"
□ LICENCE_TYPE          — e.g., "Tavern Restricted Licence"
□ SECTION_NUMBER        — e.g., 3  (for heading start numbering)
□ SECTION_TITLE         — e.g., "Location and Locality"
□ DOCUMENT_DATE         — e.g., "April 2026"
```

---

## Generation Workflow

### Step 1 — Read Style Spec
Load `references/HTS_Style_Guide_v1.0.md` and the docx skill.
Extract all typographic values needed for this document type.

### Step 2 — Read Section Content
Receive or locate the drafted section content from the LLA GPT system.
Do not generate legal content here — this skill formats only.

### Step 3 — Generate Script
Write a Node.js script using the `docx` npm library.
Save script to `/home/claude/generate_[section_name].js`.

Apply these non-negotiable formatting rules from the Style Guide:
- A4 paper: `width: 11906, height: 16838` DXA
- Margins: 1700 DXA all sides
- Fonts: Cambria (headings), Calibri (body), Arial (footnotes) — explicit, not theme aliases
- H1: Cambria 18pt, Bold, #002060, double underline, numbered
- H2: Cambria 16pt, Bold, #4F81BD, numbered
- H3/H4: Cambria 14pt, Bold (#4F81BD), numbered
- Body: Calibri 12pt, 1.15× line spacing, justified
- Header: "Prepared by HTS… on behalf of [CLIENT_LEGAL_ENTITY]" — Calibri 10pt, centred
- Footer: website centred (Calibri 11pt) + page number field right
- Footnote text: Arial 10pt, explicit
- Footnote references: inline 12pt, NO superscript (vertAlign not set)
- Heading start number: set to SECTION_NUMBER value
- Bullets: LevelFormat.BULLET with numbering config — never Unicode characters

### Step 4 — Execute and Validate
```bash
node /home/claude/generate_[section_name].js
python /mnt/skills/public/docx/scripts/office/validate.py [output_file]
```

Fix any validation errors before proceeding.

### Step 5 — Deliver
Copy final file to `/mnt/user-data/outputs/`.
Use present_files tool to make available for download.

---

## Section Stitching (Mode 2)

When compiling a full document from approved sections:

1. Receive all section `.docx` files in correct order
2. Verify heading numbers are sequential across sections
3. Generate a combined document preserving all styles
4. Add "Contents" TOC using heading styles to auto-populate
5. Reconcile footnote numbering — footnotes must run continuously 1, 2, 3…
   across the full document (not restart per section)
6. Validate final compiled document
7. Deliver to `/mnt/user-data/outputs/` with filename:
   `[TRADING_NAME]_PIA_[LICENCE_TYPE]_[DATE].docx`

---

## Quality Checks Before Delivery

```
□ Paper size confirmed A4 (not US Letter)
□ All margins 30mm / 1700 DXA
□ Header present on all pages with correct client entity name
□ Footer present on all pages — page number field (not static) + website
□ H1 uses Cambria 18pt, Bold, #002060, double underline
□ H2 uses Cambria 16pt, Bold, #4F81BD
□ Body text Calibri 12pt throughout
□ Footnote text Arial 10pt (explicit)
□ Footnote references inline 12pt, no superscript
□ Heading numbers start at correct SECTION_NUMBER
□ No Unicode bullet characters
□ No static page numbers in footer
□ Document validated without errors
□ HTS copyright notice present on cover page
```

---

## Error Handling

**Validation fails:** Unpack XML, identify and fix the specific element,
repack, revalidate. Do not deliver unvalidated documents.

**Font not rendering:** Ensure Cambria, Calibri, and Arial are specified
as explicit strings, not theme aliases (`majorHAnsi`, `minorHAnsi`).

**Page numbers static:** Replace with proper `w:fldChar`/`w:instrText PAGE`
field code sequence.

**Heading numbering wrong:** Check the `start` value on the numbering list
definition. Each section document must have its L0 start set to SECTION_NUMBER.

---

## File Naming Convention

| Document Type | Filename Format |
|---|---|
| Single section | `[SectionNumber]_[SectionTitle]_[TradingName].docx` |
| Full compiled PIA | `[TradingName]_PIA_[LicenceType]_[Date].docx` |
| Objection response | `[TradingName]_ObjectionResponse_[Date].docx` |
| Management plan | `[TradingName]_ManagementPlan_[Date].docx` |
| ETP submission | `[TradingName]_ETP_[Date].docx` |

Use underscores, no spaces. Truncate trading names over 20 characters.

---

## Reference Files

- `references/HTS_Style_Guide_v1.0.md` — Complete formatting specification
  (read this first on every generation task)
