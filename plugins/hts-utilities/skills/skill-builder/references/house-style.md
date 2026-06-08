# House Style — Distilled from `lla-*` and `green-holmes-*` Skills

This file captures the patterns observed across Ryan's existing skill ecosystem. Every
new skill drafted via skill-builder should match this style unless the brief explicitly
opts out.

## Frontmatter style

- `description: >` for multi-line descriptions (cleaner than one-line for long entries)
- Description length: 80–250 words is the sweet spot for Ryan's existing skills
- Always opens with a one-sentence statement of what the skill is
- Lists 5–15 specific trigger phrases inline
- Closes with negative scope ("Do NOT use for…")
- `metadata` block with at least `author`, `version`, sometimes `mcp-server` or `standard`

## Section ordering in SKILL.md body

The reliable pattern across `lla-gpt`, `lla-pia-drafter`, `green-holmes-product`:

1. **Title** (H1) — kebab-case name turned into Title Case
2. **One-paragraph opener** — what this skill does, no marketing language
3. **What this system is for** — purpose, business context, who/why
4. **What this system is NOT** — boundary-setting, explicit refusals (this is the signature section)
5. **When this skill triggers** — bullet list of phrases mapped to phases/actions
6. **Authority resolution** — what wins when sources conflict (only if the skill imports knowledge)
7. **The workflow / phases** — the actual work the skill does, with hard gates
8. **Gates** — explicit refusal conditions between phases
9. **Bundled scripts** (if any) — what they do, when to call them
10. **Reference files** (if any) — what's in them, when to read them
11. **Examples** — concrete worked examples
12. **Failure modes and recovery** — what to do when things go wrong
13. **Performance notes** — quality > speed reminders

Not every skill needs every section. But the order is durable across Ryan's skills.

## Tone

- **Direct.** No "I'd be happy to help" or "great question". Get to the work.
- **Second-person to the skill, third-person to Ryan.** "This skill does X" / "Ryan provides Y". Not "I will do X" or "you should do Y".
- **No marketing voice.** "Produces a correct brief" not "Crafts a brilliant brief".
- **Imperative for instructions, declarative for boundaries.** "Run the scraper" / "This skill does not draft from a vague brief".
- **Explicit refusal language.** "The skill refuses to advance until X" — not "the skill prefers X".
- **Australian English where present** in domain-specific terms, but skill metadata is neutral American English.

## Structural signatures

### The "authority lock"

Master skills open with an explicit authority lock (see `lla-gpt`):

```markdown
## Authoring Entity Lock (MANDATORY)

All [skill] outputs are prepared by and on behalf of:
**[Entity name]**

This lock applies to every [scope] regardless of [variable].
```

Use this when the skill governs work products with legal or branding implications.

### The "What this system is NOT"

Every non-trivial skill has this section. Not optional. It's how Ryan stops the skill
drifting into adjacent territory:

```markdown
## What this system is NOT

- **Not [X].** [Reason / consequence.]
- **Not [Y].** [Reason / consequence.]
- **Not [Z].** [Reason / consequence.]

If a sub-skill produces output that violates these principles, this skill rejects the
output regardless of which sub-skill produced it.
```

### The "hard gate"

Phase transitions in Ryan's workflow skills always have explicit gates:

```markdown
**Gate:** Ryan approves [X] explicitly. No advance without approval.
```

The word "Gate" appears in bold. The refusal is explicit.

### The "trigger phrases as bullet-list with arrow mapping"

```markdown
- "Phrase 1" or "phrase 1 variant" → Phase 1: [Name]
- "Phrase 2" → Phase 2: [Name]
```

The arrow → is consistent. Not a colon, not a dash.

## Naming convention

Ryan's existing skills use noun-phrase, not verb-ing:

- `green-holmes-product` not `building-green-holmes-products`
- `lla-pia-drafter` not `drafting-lla-pias`
- `green-holmes-publish` not `publishing-green-holmes-content`

This *does not* match Anthropic's current verb-ing + noun recommendation. For new
Green Holmes / HTS skills, Ryan's noun-phrase convention is preserved (consistency
within his ecosystem matters more than matching external convention). For skills
intended to be shared publicly or used outside Ryan's ecosystem, suggest the verb-ing
pattern in Phase 1 and let Ryan choose.

## What Ryan tends to reject

Based on patterns in existing skills:

- Sections titled "Why this matters" or "About this skill" — too marketing
- Long preambles before the work begins
- Bullet lists where prose would do
- Emoji headers
- "Pro tip:" callouts
- "This is just one approach" hedging
- Apologetic refusals ("I'm sorry but…")

## What Ryan tends to add when reviewing

Based on observed patterns:

- More specific trigger phrases
- Explicit negative scope ("Do NOT use for…")
- Authority hierarchy when it's unclear what wins on conflict
- Gates between phases
- Failure-mode recovery sections
