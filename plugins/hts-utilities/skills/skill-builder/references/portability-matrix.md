# Portability Matrix — Skill Features Across Agent Platforms

The Agent Skills standard is open, but platforms vary in what they support beyond the
core. This matrix is the reference for deciding what to include in a skill and what to
flag as Claude-only.

Refresh from web research at Phase 2 every time.

---

## Platform support (as of May 2026)

| Feature | Claude.ai | Claude Code | Claude API | Codex CLI | Gemini CLI | Cursor | Copilot | Goose |
|---------|-----------|-------------|------------|-----------|------------|--------|---------|-------|
| Core SKILL.md (name + description + body) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `scripts/` Python execution | ✓ | ✓ | ✓ | partial | partial | ✗ | partial | ✓ |
| `scripts/` Bash execution | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| `references/` files loaded on demand | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `assets/` (templates, data, images) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `metadata` block (custom fields) | ✓ | ✓ | ✓ | partial | partial | partial | partial | partial |
| `allowed-tools` restriction | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `license` field | ignored | ignored | ignored | ignored | ignored | ignored | ignored | ignored |
| `compatibility` field | ignored | ignored | ignored | ignored | ignored | ignored | ignored | ignored |
| Anthropic API embeds (Claude in artifacts) | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Claude Artifacts | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| MCP server invocation | ✓ | ✓ | ✓ | partial | partial | partial | partial | ✓ |
| Google Drive MCP | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

Legend: ✓ supported · ✗ not supported · partial = supported with caveats · ignored = field present but no effect

---

## Decision rules for skill-builder

### If the brief says "portable across all platforms":

- Use only core features (SKILL.md + body + optional scripts/references/assets)
- No `allowed-tools`, no Claude-specific MCPs in scripts
- Scripts use only standard libraries or libraries declared at top of script
- No mention of Artifacts, no Anthropic API embed code

### If the brief says "Claude only":

- All features available
- Use Anthropic API embeds for AI-powered Artifacts
- Use Drive/Gmail/Slack MCPs freely
- Declare in `metadata.compatibility`: `"Claude.ai, Claude Code, Claude API"`

### If the brief is silent:

- Default to **portable core** + declare any Claude-specific features in `metadata.compatibility`
- This is the safest default — works everywhere Ryan uses it, doesn't break if shared

---

## Claude-specific features that should always be flagged

If a skill uses any of these, declare it in frontmatter:

```yaml
metadata:
  compatibility: "Claude.ai only — uses Anthropic API embeds in Artifacts"
```

- Anthropic API calls inside Artifacts (the "Claude in Claude" pattern)
- Claude-specific MCP connectors (Google Drive, Gmail, Canva, Slack via Claude's MCP layer)
- Claude Artifacts as the output target
- `present_files` tool calls
- References to `/mnt/user-data/uploads` or `/mnt/skills/` paths
- The Code Execution Tool beta features

---

## What "partial" means per platform

### Codex CLI / Gemini CLI

- Reads SKILL.md and core frontmatter
- Limited or no support for arbitrary script execution (depends on agent runtime)
- `metadata` is read but custom fields may be ignored

### Cursor

- Reads SKILL.md when manually placed in the project
- No native script execution; scripts must be invoked by the user

### GitHub Copilot (via VS Code agent)

- Reads SKILL.md
- Bash scripts can run in VS Code's integrated terminal
- Python scripts run if Python extension is configured

---

## Refresh log

- 19 May 2026 — initial draft from web research. Sources: agentskills.io showcase,
  paperclipped.de adoption tracking, agensi.io standard explainer.
- Refresh by scraping the Agent Skills Client Showcase
  (https://agentskills.io/clients) and current docs on each platform at Phase 2.
