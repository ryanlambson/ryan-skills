# Agent Skills Open Standard — Snapshot

This file is the working reference for the Agent Skills specification as of the most
recent Phase 2 webscrape. Refresh this file every Phase 2 by scraping the canonical
sources and replacing the content below.

**Canonical sources (in priority order):**

1. https://agentskills.io/specification — the authoritative spec
2. https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview — Anthropic's product docs
3. https://github.com/anthropics/skills — reference implementation
4. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — engineering blog

---

## Origin and adoption

- Originally developed by Anthropic
- Released as an open standard on **18 December 2025**
- Now hosted at agentskills.io under Linux Foundation / Agentic AI Foundation governance
- Adopted by 32+ tools as of March 2026: Claude Code, Codex CLI (OpenAI), Gemini CLI (Google), GitHub Copilot, Cursor, JetBrains Junie, AWS Kiro, Block Goose, Snowflake, Databricks, ByteDance, Mistral AI, Spring AI, and others

## The minimal specification

A skill is a folder containing a `SKILL.md` file. That's it.

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code (Python, Bash, JS)
├── references/       # Optional: additional documentation
├── assets/           # Optional: templates, images, logos, data
└── ...               # Any additional files or directories
```

## SKILL.md format

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

[Instructions Claude follows when this skill is active.]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

## Required frontmatter fields

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | kebab-case, lowercase letters + numbers + hyphens only, ≤64 chars, no `claude`/`anthropic` |
| `description` | string | ≤1024 chars, no XML angle brackets, must include WHAT + WHEN |

## Optional frontmatter fields

| Field | Purpose |
|-------|---------|
| `license` | MIT / Apache-2.0 / etc. for open-source distribution |
| `allowed-tools` | Restrict which tools the skill can invoke (e.g. `"Bash(python:*) WebFetch"`) |
| `compatibility` | 1–500 char string declaring platform/runtime needs |
| `metadata` | Custom key-value pairs (author, version, mcp-server, tags, etc.) |

## Three-level progressive disclosure

1. **Frontmatter** — always in context (~100 words). Used to decide *whether* to load the skill.
2. **SKILL.md body** — loaded when the skill is judged relevant. Contains workflow instructions.
3. **Linked files** (`references/`, `scripts/`, `assets/`) — loaded on demand by Claude when the body references them.

## Description guidance ("pushy" descriptions)

Current Anthropic guidance is to write descriptions that *combat undertriggering*. Use phrases like:

- "Use this skill whenever the user mentions…"
- "Trigger when the user asks to…"
- "Make sure to use this skill if…"

A vague "helps with projects" will never trigger. A specific, pushy description triggers reliably.

## Naming conventions

- **Verb-ing + noun** is Anthropic's current recommendation: `analyzing-marketing-campaign`, `generating-practice-questions`, `drafting-survey-questions`
- **Noun-phrase** is acceptable and common: `green-holmes-product`, `lla-pia-drafter`, `pdf-processing`
- kebab-case only
- ≤64 characters
- no `claude` or `anthropic` (reserved)

## Size guidance (updated from January 2026 PDF)

- **SKILL.md body**: keep under **500 lines** (current guidance). The Jan 2026 PDF said 5000 words; current standard is tighter.
- **Description**: ≤1024 characters
- **Push everything used <20% of the time** to `references/`

## Security

- No XML angle brackets (`<` or `>`) in frontmatter (injection prevention)
- Skills from untrusted sources can be malicious — scripts can exfiltrate data or invoke tools beyond stated purpose
- Audit all bundled scripts before running a skill from an unknown source

## Platform support today

| Platform | Frontmatter fields beyond `name`/`description`? | Notes |
|----------|------------------------------------------------|-------|
| Claude.ai | Full | Upload via Settings → Capabilities → Skills |
| Claude Code | Full | Plugin directory or local skills folder |
| Claude API | Full | `/v1/skills` endpoint; Messages API `container.skills` param |
| Codex CLI (OpenAI) | Core | Reads `skills.md` (early support) |
| Gemini CLI (Google) | Core | Reads SKILL.md |
| GitHub Copilot | Core | Via VS Code agent skills |
| Cursor | Core | Manual placement |
| Goose (Block) | Core | Compatible with open spec |

For maximum portability, stick to the core spec (name, description, markdown body,
optional scripts/references/assets). Advanced features (`allowed-tools`,
`compatibility`, complex `metadata`) may degrade in non-Claude tools.

## Last refreshed

Refresh this section with the date and source URLs every time Phase 2 webscrape runs.

- Snapshot taken: 19 May 2026
- Sources: agentskills.io/specification, github.com/anthropics/skills, platform.claude.com docs
