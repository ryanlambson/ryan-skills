# Example 1 — Simple Document Skill

A skill that drafts a meeting note in a specific format. Single output, no scripts,
no MCP. The lightest skill shape.

## Brief (Phase 1)

**Skill name:** `drafting-meeting-notes` (verb-ing pattern)
**Trigger phrases:**
- "Write up the meeting"
- "Draft notes from our discussion"
- "Turn this into meeting notes"
- "Meeting note in our format"
- "Note this meeting"

**Negative triggers:** Do not trigger for "take notes" mid-conversation (that's just
note-taking, not a structured deliverable). Do not trigger for transcripts (different shape).

**Core workflow:**
1. Ask for the meeting metadata if not provided (date, attendees, purpose)
2. Identify decisions, action items, open questions in the source material
3. Draft the note using the fixed section order
4. Return the note in markdown, ready to paste

**Gates:** Do not advance to drafting without meeting metadata.

**Authority hierarchy:** N/A (no imports).

**Output type:** Markdown document, inline in chat.

**Bundled scripts:** None.

**MCP / tool dependencies:** None.

**Distribution target:** Portable across all platforms.

## Research (Phase 2)

- Tier 1: Internal knowledge sufficient for a single-output skill of this shape
- Tier 2: Drive `anthropic-skills-repo` — check `example-skills/` for similar shapes
- Tier 3: Skip live scrape (no domain-specific sources; standard format only)

## Outline (Phase 3)

```
drafting-meeting-notes/
└── SKILL.md  (~80 lines)
```

Frontmatter description (draft):

> Drafts a meeting note in the standard team format. Use when the user asks to write
> up, summarise, or draft notes from a meeting, discussion, or call. Triggers on
> "write up the meeting", "draft notes from our discussion", "turn this into meeting
> notes", or any request to produce a structured meeting deliverable. Does NOT trigger
> for casual note-taking, transcripts, or general summarisation.

Section structure:
1. Title
2. One-paragraph opener
3. When this skill triggers
4. The standard format (the template the note follows)
5. Required metadata
6. Drafting rules (what to include / exclude)
7. Examples (2 worked examples)

## Draft (Phase 4)

SKILL.md is 80 lines, well under the 500-line ceiling. No scripts, no references, no
assets. QA gate passes on first try.

## Output

`/mnt/user-data/outputs/drafting-meeting-notes.zip` + Drive backup.

---

**Why this is a useful example:**

It shows that the four-phase workflow doesn't have to be heavy. For a single-output
skill, the brief is short, the research is short, the outline is short, and the draft
is one file. The discipline of the phases matters; the volume of each phase scales to
the complexity of the skill.
