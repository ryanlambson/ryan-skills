---
name: tracked-document-editor
description: >
  Applies specific, targeted edits to an existing fully-uploaded .docx as tracked
  changes attributed to R.Lambson, while preserving the original formatting and
  branding of that document exactly. Use this skill whenever Ryan uploads a complete
  document and asks to amend it, apply edits, mark it up, change X to Y, or update it
  at review stage — including NMPs, HMPs, PIAs, submissions, letters, and management
  plans. Trigger phrases: "amend this document", "apply these edits to the attached
  doc", "edit this docx and track the changes", "mark up this document", "update this
  but keep the formatting", "change X to Y in this document". Tracked changes are
  mandatory; never a clean rewrite unless Ryan explicitly requests one. Do NOT use for
  drafting new documents from scratch, summarising or reviewing without editing, or
  spreadsheet/presentation creation.
metadata:
  author: Ryan Lambson (HTS)
  version: 1.0.0
  standard: agent-skills-1.0
  depends-on: public docx skill (unpack/pack/validate mechanism)
  compatibility: claude.ai (requires code execution and the docx skill)
---

# Tracked Document Editor

This skill governs how edits are applied to an existing, fully-uploaded `.docx` at the
review stage. Every edit is written as a Word tracked change attributed to **R.Lambson**,
and the original document's formatting and branding are preserved exactly. The skill never
restyles, never reformats, and never rewrites the document wholesale unless Ryan explicitly
asks for that.

This skill is the **governance layer**. The mechanism — unpacking the `.docx`, editing the
XML, repacking — belongs to the public **docx skill**. This skill decides *how* that
mechanism is allowed to be used.

---

## What this skill is for

Ryan works in document review cycles: a client or regulatory document is drafted, then
amended through rounds of targeted changes (an NMP gains the council's noise conditions, a
PIA section is tightened, a submission absorbs an RFI response). At that stage the document
already has its formatting and its client branding locked in. The job is not to rebuild it —
it is to insert precise changes that a reviewer can see, accept, or reject in Word, without
disturbing anything else.

This skill exists so that every such edit ships the same way: as clean tracked changes,
correctly attributed, with the source document's styling untouched.

---

## What this skill is NOT

- **Not a document drafter.** It does not create documents from scratch. New documents go
  through the docx skill directly or through the relevant builder skill (e.g.
  `lla-document-builder`).
- **Not a rewriter.** It does not rephrase, restructure, or "improve" prose beyond the
  specific edits requested. A full or substantial rewrite happens only when Ryan explicitly
  asks for one.
- **Not a reviewer-only tool.** If Ryan wants commentary or a critique without changing the
  file, that is not this skill.
- **Not a re-brander.** It never applies a fixed palette or house style. Branding is read
  from the uploaded document and matched. There is no "HTS colour" — colours, fonts, and
  styles belong to whichever client the document is for.
- **Not for formats that cannot carry tracked changes.** PDFs cannot. Spreadsheets and
  presentations do not carry clean Word-style tracked changes. This skill is for `.docx`.

If a request would violate any of these, the skill stops and raises it with Ryan rather than
proceeding.

---

## When this skill triggers

Trigger when a complete document is uploaded **and** Ryan asks for specific edits to it:

- "amend this document" / "make these edits to the attached doc"
- "apply these changes to the uploaded NMP / HMP / PIA / submission"
- "edit this docx and track the changes"
- "mark up this document with the following edits"
- "we're at review stage, change X to Y in this document"
- "update this document but keep the formatting"

**Do NOT trigger for:**

- Drafting a new document from scratch (no source document to preserve)
- Summarising, critiquing, or reviewing a document without editing it
- Creating or editing spreadsheets (`.xlsx`) or presentations (`.pptx`)
- Any request where no document has actually been uploaded

If the intent is editing but no file is attached, ask Ryan to upload the document before
proceeding. Do not invent or reconstruct the document from memory.

---

## Authority resolution

When guidance conflicts:

1. **This skill's rules win on *how* edits are applied** — tracked changes mandatory,
   R.Lambson attribution, no restyling, override-by-asking.
2. **The public docx skill wins on *mechanism*** — the unpack → edit XML → repack process
   and the tracked-change tag syntax (`<w:ins>` / `<w:del>`, `<w:delText>` inside deletions).
3. **The uploaded document wins on *all* formatting and branding** — it is the single source
   of truth for fonts, colours, sizes, list styles, heading styles, and layout. Inserted
   content copies the formatting of the surrounding content. Never impose an external style.

---

## The workflow

### Step 1 — Confirm the file

Confirm a complete document is uploaded and is `.docx`.

- If it is `.doc` (legacy binary): flag to Ryan that it must be converted to `.docx` first,
  and that this single conversion step can cause minor formatting shift. Convert with the
  docx skill's `soffice.py` only after Ryan acknowledges, then proceed.
- If it is `.pdf`, `.xlsx`, or `.pptx`: stop. Explain that the format cannot carry clean
  tracked changes and ask how Ryan wants to proceed.

### Step 2 — Read the document and the edit list

Extract the text (`extract-text document.docx`) to locate the exact passages to change.
Identify, for each edit, the precise run(s) affected. Read enough surrounding XML to copy
the existing run properties (`<w:rPr>`) so inserted content matches font, colour, size, and
style exactly.

### Step 3 — Unpack

```bash
python /mnt/skills/public/docx/scripts/office/unpack.py document.docx unpacked/
```

### Step 4 — Apply edits as tracked changes

Edit `unpacked/word/document.xml` with the Edit/str_replace tool directly. For every change:

- Wrap insertions in `<w:ins w:author="R.Lambson" w:date="...">` and deletions in
  `<w:del w:author="R.Lambson" w:date="...">` (use `<w:delText>` inside deletions).
- **Attribute every change to `R.Lambson`** — exact string, no space after the full stop.
- Copy the original run's `<w:rPr>` into new runs so formatting is identical to the
  surrounding text.
- When deleting an entire paragraph or list item, mark the paragraph mark deleted too (add
  `<w:del>` inside `<w:pPr><w:rPr>`) so accepting changes leaves no empty paragraph.
- Change only what the edit requires. Do not touch unrelated runs, spacing, or styling.

Use unique `w:id` values for each tracked-change element.

### Step 5 — Repack and validate

```bash
python /mnt/skills/public/docx/scripts/office/pack.py unpacked/ output.docx --original document.docx
```

Then render a visual check to confirm branding and layout survived and the changes display
as tracked markup:

```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 110 output.pdf page
```

View the affected pages. Confirm: branding intact, inserted text matches surrounding style,
changes appear as tracked insertions/deletions.

### Step 6 — Deliver

Present the amended file via `present_files` with a short summary of what changed, then give
the mandatory closing reminders below.

---

## Gates and refusals

- **Tracked changes are mandatory.** Within scope, edits are always tracked changes. Never
  deliver a silently-rewritten clean file.
- **No wholesale rewrite without explicit request.** Proceed silently with tracked edits for
  normal targeted changes. Stop and ask Ryan first **only** when:
  1. applying the edit properly would require restructuring or reformatting that breaks the
     original layout;
  2. Ryan has asked for something that is genuinely cleaner as a rewrite; or
  3. the edits are so extensive that tracked changes would render the document unreadable.

  In those cases, explain the trade-off and let Ryan choose. Do not default to a rewrite.
- **Branding and formatting are locked.** Never restyle, recolour, or reformat. Match the
  uploaded document. This is non-negotiable.
- **Never fake tracked changes** on a format that cannot carry them. Flag the limitation.

---

## Mandatory closing reminders

Every time this skill delivers an amended document, finish with these reminders:

1. **Footer / version block:** If the document's version-control footer is an image
   (screenshot), it cannot be edited as a tracked change. **Remind Ryan to manually update
   the version number and review date.** If the footer is live text or a real table, offer
   to update it (as a tracked change, or cleanly, Ryan's call).
2. **Attribution:** Confirm all tracked changes are attributed to R.Lambson.
3. **Branding:** Confirm the original formatting and branding were preserved.

---

## Examples

### Example 1 — Targeted edit, proceed silently

Ryan uploads `Attachment_6_-_NMP.docx` and writes: "Add the council's noise conditions — no
live music in the alfresco, 72 dB day / 67 dB evening, and the agreed trading hours. Track
the changes."

The skill: confirms `.docx`; extracts text to locate the music and limits sections; unpacks;
inserts the new bullets and sections as `<w:ins author="R.Lambson">`, each new run copying the
surrounding Calibri/heading formatting from the document; repacks; renders a visual check;
presents the file; reminds Ryan to manually update the footer version/date. No rewrite, no
restyle, no question needed — the edits are targeted and additive.

### Example 2 — Override threshold, stop and ask

Ryan uploads a PIA section and writes: "Tighten this — it's repetitive and the order is
wrong."

This implies restructuring, not targeted edits. The skill stops and asks: "This reads as a
restructure rather than tracked line edits — reordering and condensing would produce so many
tracked changes the section becomes unreadable in markup. Do you want (a) tracked line edits
only, leaving the order as-is, or (b) a clean rewrite of the section?" It proceeds only on
Ryan's answer.

---

## Failure modes and recovery

**`.doc` uploaded (legacy).** Flag the conversion requirement and the minor-formatting-shift
risk. Convert via `soffice.py` only after Ryan acknowledges, then proceed.

**Footer is an image.** The version block cannot be edited. Do not attempt to recreate it.
Surface this and remind Ryan to update it manually. (Fixing the template footer from a
screenshot to a native table is a separate template job, not this skill.)

**No document uploaded.** Do not reconstruct from memory or a prior version. Ask Ryan to
upload the document.

**Edit would break layout.** Stop and raise it (override threshold). Offer the trade-off.
Never silently reflow the document to make an edit fit.

**Validation fails on repack.** Re-open the unpacked XML, fix the malformed element, repack.
Do not ship an unvalidated file.

---

## Performance notes

- Surgical beats wholesale. The value of this skill is that everything *except* the requested
  change stays byte-for-byte intact.
- Preservation quality outranks speed. A faithfully-matched insertion is worth more than a
  fast one that subtly shifts a font or colour.
- Always run the visual check before delivery. Tracked changes that look right in XML can
  still reveal a styling mismatch on the page.
