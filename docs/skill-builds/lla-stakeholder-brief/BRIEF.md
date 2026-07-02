# BRIEF — lla-stakeholder-brief

Phase 1 of 4 (skill-builder workflow). Status: awaiting approval.

## 1. Skill name

`lla-stakeholder-brief`

Noun-phrase pattern, consistent with the existing `lla-*` suite (lla-pia-drafter, lla-citation-checker). Kebab-case, 21 chars, no reserved words.

## 2. Trigger phrases

- "The PIA is complete, draft the stakeholder briefs"
- "Draft the LEU email" / "Draft the CHO email"
- "Section 8 emails" / "Community Consultation emails"
- "Draft the pre-lodgement notification for [venue]"
- "Send the pre-lodgement briefs" (drafting step)
- "Mark the consultation as sent" / "Update Section 8, briefs sent [date]" (post-send step)

## 3. Negative triggers (must NOT fire)

- Drafting the PIA itself or any PIA section (lla-pia-drafter)
- The statutory advertising Notice of Application (different instrument, prescribed form)
- Objection responses or correspondence after lodgement
- General emails unrelated to a completed PIA
- Consumer survey work (lla-consumer-survey-drafter)

## 4. Core workflow

**Phase A — Extract.** Read the completed PIA (docx path supplied by Ryan or found in the project's DLGSC folder). Extract: applicant entity + ACN, licence class sought, premises name and address, venue concept and key features, directors and credentials, trading conditions list (verbatim), planning context (one line), locality. If any field is missing or still carries a placeholder or (TO DO)/highlight marker in the sections relied upon, STOP and report what is incomplete.

**Phase B — Draft.** Generate recipient variants from the reference structure (SKS Cockburn example + Last Slice Eaton example, held in references/):
- WA Police Liquor Enforcement Unit (LEU)
- Chief Health Officer (CHO)
- Local government (optional, on request)
Rules: trading conditions carried verbatim from the PIA (never re-typed from a template); conditions block keyed to the licence class stated in the PIA (tavern restricted / hotel / hotel restricted / small bar); lla-writing-conventions applied (banned terms, CCTV entry-and-exit-points wording, no em-dashes in paragraphs); each email ends with the standard feedback invitation and HTS signature block; explicit statement that pre-lodgement contact does not constitute endorsement is preserved in the PIA, not claimed in the email.

**Phase C — Review gate.** Run the conventions check script over the drafts. Present drafts to Ryan. No sending; drafting only.

**Phase D — Post-send PIA update (on Ryan's confirmation that briefs were sent).** Update the PIA Community Consultation section: insert sent dates, change prospective wording to past tense, remove the (TO DO) marker and yellow highlighting. Save with backup copy.

## 5. Gates and refusals

- Refuses to draft if the PIA trading conditions section contains placeholders or unresolved markers.
- Refuses to invent any applicant, premises, or planning fact not present in the PIA.
- Refuses to state or imply LEU/CHO endorsement or support.
- Phase D runs only on explicit confirmation the emails were actually sent, with dates.
- Never sends email itself, even if a mail connector is available, unless Ryan explicitly instructs in the session.

## 6. Authority hierarchy

1. The completed PIA for this application (sole source of facts; conditions verbatim)
2. lla-writing-conventions (style; mandatory)
3. Reference examples (structure only, never facts)
4. lla-gpt master rules (tone, authority discipline) where not covered above

Conflicts resolve upward: if a reference example conflicts with the PIA's content, the PIA wins.

## 7. Output type

- Ready-to-send email drafts (subject + body) per recipient, delivered in chat and optionally as .docx in the project's DLGSC folder
- On Phase D: edited PIA docx (formatting preserved, backup created)

## 8. Bundled scripts

- `scripts/check_conventions.py` — deterministic post-draft check: banned terms (sits/food-led/need/community outside protected strings), em-dashes in body text, CCTV scope phrases, leftover placeholders. Exit 0 pass / 1 fail with line detail.
- No extraction script: extraction is judgment-laden (protected quotes, licence class nuances) and stays with the agent.

## 9. MCP / tool dependencies

- File access to the client project folder (Cowork mounted folder or uploaded PIA)
- Optional: Gmail/Outlook connector for send-on-instruction (declared as optional; absence does not degrade drafting)

## 10. Distribution target

- Primary: Claude (Cowork + claude.ai upload)
- Portable per Agent Skills open standard; no Claude-only features. Script requires Python 3 stdlib only.
