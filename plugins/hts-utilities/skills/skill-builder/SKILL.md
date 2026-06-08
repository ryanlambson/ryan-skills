---
name: skill-builder
description: >
  Master skill-building system. Use this skill whenever Ryan asks to build, draft,
  scaffold, generate, or create a new Claude skill — including phrases like "build me a
  skill for X", "make a skill that does Y", "scaffold a skill", "draft a SKILL.md",
  "turn this workflow into a skill", "spec out a skill", "create an agent skill", or
  any request involving the Agent Skills open standard. Also trigger when Ryan
  describes a repeatable workflow he wants packaged, references SKILL.md, frontmatter,
  progressive disclosure, or asks to review or improve an existing skill. Runs a
  four-phase interactive workflow (Brief, Research, Outline, Draft, QA) and produces a
  ready-to-upload skill folder, backed up to Google Drive. Cognitive layer plus
  bundled Python scripts for webscraping and validation. Do NOT use for executing
  existing skills or general workflow advice unrelated to skill packaging.
metadata:
  author: Ryan Lambson (Green Holmes / HTS)
  version: 1.0.0
  standard: agent-skills-1.0 (agentskills.io)
  output-location: /mnt/user-data/outputs/ + Google Drive SKILLS/
---

# Skill Builder — Master Skill

The skill that loads first when Ryan asks to build a new Claude skill. It does not produce
skills in one shot. It runs a four-phase interactive workflow with hard gates between
each phase. Speed is not the goal. A correct, portable, production-grade skill is the
goal.

This skill is the **cognitive layer**. The Python scripts in `scripts/` are the
**execution layer**. They share a single source of truth (this file). The agent never
drifts from the skill, and the skill never asks the scripts to do something they cannot do.

---

## What this system is for

Ryan builds skills to capture repeatable workflows — for liquor licensing (LLA), for
Green Holmes content and product work, for media pipelines, and for one-off domain
expertise that would otherwise need re-explaining every conversation. Each new skill
must:

- Conform to the Agent Skills open standard (portable across Claude, Codex CLI, Gemini CLI, Cursor, Copilot)
- Match Ryan's house style (kebab-case, authority hierarchies, hard gates, no-fluff prose)
- Trigger reliably without over-firing
- Survive the QA gate before output

This skill exists to make every new skill ship with the same quality as `lla-pia-drafter`
and `green-holmes-product` — without Ryan re-deriving the structure each time.

---

## What this system is NOT

- **Not a one-shot generator.** A skill is not a prompt. It is a contract. The workflow refuses to skip phases.
- **Not Claude-exclusive.** Output conforms to the open Agent Skills standard. Skills must work in Codex CLI, Gemini CLI, etc., unless the brief explicitly opts out.
- **Not opinion-free.** When Anthropic's current guidance contradicts the January 2026 PDF (`TheCompleteGuidetoBuildingSkillforClaude.pdf`), current guidance wins. Web research resolves the conflict.
- **Not webscraping-first.** Ryan's expertise and the skill-builder's own knowledge lead. Webscraping is the *check-our-work* step, not the *generate-from-scratch* step.
- **Not script-blind.** Every skill that involves data processing, validation, or external API calls gets bundled scripts, not language-only instructions. Code is deterministic; language interpretation isn't.

If any phase produces output that violates these principles, the QA gate rejects it
regardless of how polished the rest of the skill is.

---

## When this skill triggers

This skill triggers on first mention of skill-building. Specifically:

- "Build me a skill for X" / "Create a skill that does Y" → Phase 1: Brief
- "Draft a SKILL.md for…" / "Spec out a skill…" → Phase 1: Brief
- "Turn this workflow into a skill" → Phase 1: Brief (with workflow as input)
- "Research what's current for X skills" → Phase 2: Research (skip to)
- "Show me the outline" / "Let's review the outline" → Phase 3: Outline Review
- "Draft it" / "Build it" / "Generate the skill" → Phase 4: Draft (after outline approved)
- "QA this skill" / "Check this skill" → QA Gate (standalone on existing skill)
- "Review my skill folder" → QA Gate (standalone on existing skill)

If Ryan engages without naming the phase, this skill identifies it from context and
confirms before proceeding.

---

## Authority resolution

When guidance from two sources conflicts:

1. **Anthropic's current documented standard** (agentskills.io, docs.claude.com/agent-skills, github.com/anthropics/skills) wins on format and structural rules. Always check via webscraping at Phase 2.
2. **Ryan's house style** (this skill's *What this system is/is NOT* + the patterns observed in `lla-*` and `green-holmes-*` skills) wins on tone, structure of sections, gate logic, naming.
3. **The January 2026 PDF** (`TheCompleteGuidetoBuildingSkillforClaude.pdf`) is the durable reference. Default to it for principles. Override only when Tier 1 contradicts.
4. **Google Drive `SKILLS/anthropic-skills-repo/`** is the example library. Reference for production patterns. Not authority on format.

The Agent Skills open standard is the structural constraint. House style is the
cosmetic constraint. Webscraping resolves conflicts between them when they emerge.

---

## The four-phase workflow

Each phase has a hard gate. The skill refuses to advance until the gate passes.

### Phase 1: Brief

**Output:** A complete brief at `/home/claude/skill-builds/[skill-slug]/BRIEF.md`.

The brief is the contract for the build. If the brief is wrong, everything downstream
is wrong. Time spent here is paid back five times in the draft phase.

**The brief must specify:**

1. **Skill name** (kebab-case, ≤64 chars, no `claude`/`anthropic` prefix). Suggest the *verb-ing + noun* pattern (Anthropic's current recommendation) but accept noun-phrase if Ryan prefers (matches his existing `green-holmes-*` and `lla-*` conventions).
2. **Trigger phrases** — at least 5 specific phrases a user would actually say. Mix exact-match and paraphrased.
3. **Negative triggers** — what should NOT activate this skill (combats over-triggering).
4. **Core workflow** — the actual steps the skill will execute. If multi-phase, name the phases.
5. **Gates and refusals** — what the skill refuses to do. What it requires before advancing.
6. **Authority hierarchy** — if the skill imports knowledge from other files or systems, what wins when they conflict.
7. **Output type** — what the skill produces (document, code, decision, message draft, etc.).
8. **Bundled scripts needed** — any deterministic operations that should be code, not language.
9. **MCP / tool dependencies** — does it need Drive, Gmail, Canva, custom MCP, web search?
10. **Distribution target** — Claude.ai only? Codex CLI? Both? Portable?

The brief is rejected if any of the ten sections is missing or vague.

**Gate:** Ryan approves the brief explicitly with "approved" or "go". No advance without
explicit approval. If Ryan says "looks good but…" the brief is updated and re-presented.

### Phase 2: Research

**Output:** A research note at `/home/claude/skill-builds/[skill-slug]/RESEARCH.md`.

Research runs in three tiers, in order, every time.

**Tier 1: Internal knowledge** — Apply what this skill and Claude already know from the
January 2026 PDF and Anthropic's documented standard. Draft the structural decisions
(frontmatter, body sections, scripts/references/assets layout).

**Tier 2: Drive reference library** — Consult `Google Drive/SKILLS/anthropic-skills-repo/`
for current example patterns. Look for skills in the same shape (workflow automation,
document creation, MCP enhancement). Extract concrete patterns to reuse.

**Tier 3: Live web check** — Call `scripts/scrape_static.py` (or `scrape_dynamic.py` for
JS-heavy sources) against:

- `https://agentskills.io/specification` (the canonical standard)
- `https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview` (Anthropic docs)
- `https://github.com/anthropics/skills` (reference implementation)
- Any **domain-specific** sources implied by the brief (e.g., for a SurveyMonkey skill, scrape SurveyMonkey API docs)

The Tier 3 check exists to catch innovations that have landed since training cutoff or
since the PDF was published. Flag any discrepancy between Tier 1 expectations and Tier 3
reality. Surface the discrepancy explicitly in the research note.

**Gate:** Research note presented to Ryan. Discrepancies flagged. Ryan confirms "research
clear" or asks for more digging. No advance without confirmation.

### Phase 3: Outline Review

**Output:** A skill outline at `/home/claude/skill-builds/[skill-slug]/OUTLINE.md` showing:

- Proposed frontmatter (name, description draft, metadata)
- SKILL.md section structure (headings, in order)
- List of bundled scripts with one-line purpose each
- List of reference files (if any) with one-line purpose each
- List of asset files (if any) with one-line purpose each
- The trigger-phrase list (final, post-Phase-1 refinement)
- The QA criteria this specific skill will be tested against

The outline is the chance to catch structural mistakes before drafting. Drafting is
expensive; restructuring at outline stage is cheap.

**Gate:** Ryan approves the outline. Common interventions: "split that section",
"add a reference file for X", "the description is too vague", "verb-ing pattern please".

### Phase 4: Draft

**Output:** A complete skill folder at `/home/claude/skill-builds/[skill-slug]/`
containing:

```
[skill-slug]/
├── SKILL.md                  # Required, follows agreed outline
├── scripts/                  # Bundled scripts as agreed
├── references/               # Reference files as agreed (if any)
├── assets/                   # Templates, data, images (if any)
└── examples/                 # Example invocations and expected outputs
```

The draft follows the outline. If the draft has to deviate from the outline, the
deviation is flagged explicitly to Ryan. Silent drift is the failure mode.

SKILL.md is kept under 500 lines (current Anthropic guidance, tighter than the
January 2026 PDF's 5000-word figure). Content above 500 lines gets pushed to
`references/`.

**Gate:** Draft passes the QA gate (next section). No exceptions.

---

## QA Gate (hard pass/fail)

Run by `scripts/qa_check.py`. Every check must pass or the skill cannot ship. No
override flag, no "ship anyway" — if a check fails, the offending content is fixed
and the gate re-runs.

### Structural checks (automated by qa_check.py)

- [ ] `SKILL.md` exists, exact filename (case-sensitive)
- [ ] Folder name is kebab-case, ≤64 chars, no spaces, no underscores, no capitals
- [ ] Folder name does not contain `claude` or `anthropic` (reserved)
- [ ] Folder name matches `name` field in frontmatter
- [ ] YAML frontmatter delimited by `---` on both sides
- [ ] `name` field present, kebab-case
- [ ] `description` field present, ≤1024 characters, no `<` or `>` characters
- [ ] Description includes WHAT (the skill does) and WHEN (trigger conditions)
- [ ] Description includes at least 3 specific trigger phrases
- [ ] SKILL.md body is ≤500 lines
- [ ] No `README.md` inside the skill folder (it goes at repo level, not skill level)
- [ ] All bundled scripts have a shebang and are executable
- [ ] All bundled scripts pass a syntax check (`python -m py_compile` for `.py`, `bash -n` for `.sh`)
- [ ] No script calls `curl | bash`, `eval`, `exec`, or fetches and executes remote code (security)
- [ ] No script reads from outside its own skill folder or `/mnt/user-data/` (sandbox respect)

### Content checks (assessed by Claude reading the draft)

- [ ] Skill body opens with a one-paragraph statement of what the skill does (matches description)
- [ ] At least one *What this system is NOT* section or equivalent boundary-setting
- [ ] Trigger-phrase section with bullet-list mapping phrases to phases/actions
- [ ] Authority hierarchy section if the skill imports from other sources
- [ ] Examples section with at least 2 concrete worked examples
- [ ] Troubleshooting section (or equivalent failure-mode coverage)
- [ ] If the skill calls scripts, each script invocation in the body shows the exact command
- [ ] Reference files referenced from SKILL.md actually exist in `references/`
- [ ] No mention of capabilities the skill does not have (no hallucinated tool access)
- [ ] Tone matches Ryan's house style: direct, no fluff, no marketing voice

### Portability checks (assessed by Claude reading the draft)

- [ ] Skill does not assume Claude-specific features unless flagged in `metadata.compatibility`
- [ ] If skill uses Claude-only features (artifacts, Anthropic API embeds), this is declared explicitly
- [ ] Scripts use only standard libraries or libraries the user is expected to have, with a list at the top of each script

**Output of QA gate:** A pass/fail report. If any item fails, the report names the
failed item, the offending line/file, and the suggested fix. Ryan can ask for the fix
to be applied; the gate re-runs after.

---

## Output and distribution

When the QA gate passes:

1. **Zip the skill folder** to `/mnt/user-data/outputs/[skill-slug].zip`
2. **Present the zip via `present_files`** for immediate download
3. **Sync to Google Drive** at `SKILLS/[skill-slug]/` (via `scripts/sync_to_drive.py`)
4. **Append a one-line entry** to `SKILLS/INDEX.md` in Drive: name, date, one-line purpose
5. **Provide installation instructions** in chat: "Upload via Claude.ai → Settings → Capabilities → Skills" and the Codex CLI / Cursor equivalents

The zip is ready to upload to Claude.ai. The Drive copy is the backup and the upgrade
channel — drop new reference material into a skill's folder in Drive and the next time
that skill is invoked through skill-builder, the new material is picked up.

---

## Bundled scripts

All in `scripts/`. Each has a header comment listing its purpose, inputs, outputs, and
dependencies.

- **`scrape_static.py`** — Default scraper for static HTML pages. Uses `requests` + `BeautifulSoup`. Used in Phase 2 Tier 3 for most sources. Fastest.
- **`scrape_dynamic.py`** — Heavy scraper for JS-rendered pages. Uses `playwright`. Used in Phase 2 Tier 3 when a site is JS-heavy (single-page apps, content gated behind client-side rendering). Slower; requires `playwright install chromium`.
- **`qa_check.py`** — Runs the structural checks of the QA gate. Returns pass/fail with details. Always run before output.
- **`package_skill.py`** — Zips the skill folder for `/mnt/user-data/outputs/`.
- **`sync_to_drive.py`** — Pushes the skill folder to Google Drive `SKILLS/[skill-slug]/`. Requires Google Drive MCP connector.

See `references/scripts-guide.md` for invocation patterns and exit codes.

---

## Reference files

- **`references/agent-skills-spec.md`** — Snapshot of the open standard from agentskills.io. Refreshed by Phase 2 scrape.
- **`references/house-style.md`** — Ryan's house style distilled from `lla-*` and `green-holmes-*` skills: tone, section ordering, gate logic, naming.
- **`references/scripts-guide.md`** — How to invoke each bundled script. Exit codes, common errors.
- **`references/portability-matrix.md`** — Which features work in which agent platforms (Claude, Codex CLI, Gemini CLI, Cursor, Copilot).

---

## Examples

Three worked examples in `examples/` showing the workflow end-to-end:

- **`examples/01-simple-document-skill.md`** — Single-file output skill, no scripts. (E.g., "draft a meeting note in our format".)
- **`examples/02-mcp-enhancement-skill.md`** — Skill that orchestrates an existing MCP (e.g., "publish a Green Holmes post to WordPress with featured image"). Multiple scripts.
- **`examples/03-master-skill.md`** — A master skill that governs sub-skills (in the shape of `lla-gpt`).

These are documentation, not executable. Reading them in Phase 3 helps Ryan visualise
the output before drafting begins.

---

## Common patterns and anti-patterns

### Patterns to use

- **Authority hierarchy at the top** — every skill that imports knowledge needs one
- **Hard gates between phases** — refusal conditions stated explicitly
- **Trigger phrases as bullet-list with mapping** — phrase → phase/action
- **Verb-ing + noun naming** for new skills (Anthropic's current recommendation)
- **"Pushy" descriptions** — combat undertriggering with phrases like "Use this skill whenever Ryan asks to…"
- **Progressive disclosure aggressively** — anything used <20% of the time goes to `references/`
- **Code for determinism** — validation, parsing, API calls: scripts, not language

### Anti-patterns to refuse

- **README.md inside the skill folder** (it goes at repo level, separate from the skill)
- **`claude` or `anthropic` in skill name** (reserved)
- **Vague descriptions** ("helps with projects" — undertriggers)
- **Universal descriptions** ("use for any document task" — overtriggers)
- **XML angle brackets in frontmatter** (`<` or `>` — security restriction)
- **Capitalised or space-separated folder names**
- **Scripts that hide their purpose, fetch remote code, or break the sandbox**

---

## Failure modes and recovery

**Brief is too vague to research.** → Reject the brief. Return to Ryan with the specific
ten-section template and ask for the missing pieces. Do not proceed to Phase 2.

**Webscraping fails (network down, site blocked).** → Surface the failure. Offer to
proceed on Tier 1 + Tier 2 alone, with an explicit warning in the research note that
Tier 3 was skipped. Flag this in the final skill's metadata so a future re-run can fill
the gap.

**Outline review surfaces a structural conflict** (e.g., "this needs to be a master skill
with sub-skills, not a single skill"). → Pause. Don't push through. Re-do the brief
with the new structure.

**QA gate fails repeatedly on the same item.** → Stop. The skill design is wrong, not
the draft. Return to outline review.

**Ryan asks to ship without QA passing.** → Refuse. The QA gate is a hard gate. No
override. Offer to fix the failing item instead.

---

## Performance notes

- Take time. A correct skill saves hours every conversation forever; a hasty skill costs hours every time it under- or over-triggers.
- Quality is more important than speed.
- Do not skip the research phase even when the brief seems obvious.
- The 500-line SKILL.md ceiling is a real ceiling. Push everything else to references/.
