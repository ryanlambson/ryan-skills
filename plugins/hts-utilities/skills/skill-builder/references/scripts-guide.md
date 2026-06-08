# Scripts Guide — Invocation, Exit Codes, Common Errors

Quick reference for the bundled scripts in `scripts/`. Read this before invoking
scripts in unfamiliar phases.

---

## scrape_static.py

**Purpose:** Default scraper for static HTML pages. Used in Phase 2 Tier 3.

**Dependencies:** `pip install requests beautifulsoup4 lxml`

**Invocation:**

```bash
# Single URL, structured JSON to stdout
python scrape_static.py --url https://agentskills.io/specification

# Multiple URLs to file
python scrape_static.py \
  --url https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview \
  --url https://github.com/anthropics/skills \
  --output /home/claude/skill-builds/my-skill/RESEARCH-raw.json

# Plain text only, narrowed to article body
python scrape_static.py --url https://example.com/blog/post --selector "article" --text-only
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | All URLs fetched successfully |
| 1 | Network error on at least one URL |
| 2 | Parse error |
| 3 | Missing dependency or bad arguments |

**When to use:** Default choice. Try this first.

**When to switch to `scrape_dynamic.py`:** If `main_text` comes back empty or wildly
smaller than expected, the page is probably JS-rendered. Switch.

---

## scrape_dynamic.py

**Purpose:** Heavy scraper for JS-rendered pages (SPAs, lazy-loaded content).

**Dependencies:** `pip install playwright beautifulsoup4 lxml` + `playwright install chromium`

**First-run setup (one-time):**

```bash
pip install playwright beautifulsoup4 lxml
playwright install chromium
```

**Invocation:**

```bash
# Same args as scrape_static, plus optional --wait-ms
python scrape_dynamic.py --url https://app.example.com/docs --wait-ms 3000

# Wait for a specific selector to appear
python scrape_dynamic.py --url https://example.com --selector "main"
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | All URLs fetched successfully |
| 1 | Network or page-load error |
| 2 | Parse error |
| 3 | Missing dependency or bad arguments |
| 4 | Playwright not installed (`playwright install chromium` needed) |

**Cold start:** ~5–10 seconds. Use only when scrape_static returns empty.

---

## qa_check.py

**Purpose:** Hard QA gate. Validates structural and content rules. The gate before output.

**Dependencies:** `pip install pyyaml`

**Invocation:**

```bash
# Human-readable report
python qa_check.py --skill-path /home/claude/skill-builds/my-skill

# JSON output for programmatic consumption
python qa_check.py --skill-path /home/claude/skill-builds/my-skill --json

# Strict mode: warnings count as failures
python qa_check.py --skill-path /home/claude/skill-builds/my-skill --strict
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | One or more checks failed (do not ship) |
| 2 | Skill folder not found |
| 3 | Bad arguments |

**Reading the report:**

- `✓ [PASS]` — check passed
- `⚠ [WARN]` — soft issue, not blocking unless `--strict`
- `✗ [FAIL]` — blocking; must be fixed before output

**What to do on FAIL:** Read the `Fix:` line. Apply the fix. Re-run the gate. Repeat
until pass. Never override.

---

## package_skill.py

**Purpose:** Zip the skill folder for upload to Claude.ai. Refuses to package if QA gate
hasn't passed.

**Dependencies:** Standard library only.

**Invocation:**

```bash
# Default: zip to /mnt/user-data/outputs/
python package_skill.py --skill-path /home/claude/skill-builds/my-skill

# Custom output directory
python package_skill.py --skill-path ./my-skill --output-dir /tmp

# Skip QA gate (NOT RECOMMENDED — only for debugging)
python package_skill.py --skill-path ./my-skill --skip-qa
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Zip created at `<output-dir>/<skill-name>.zip` |
| 1 | Skill path not found |
| 2 | QA gate has not passed — refused to package |
| 3 | Zip creation failed |

**Output:** The absolute path of the created zip is printed to stdout.

---

## sync_to_drive.py

**Purpose:** Produce a Drive upload manifest. Actual upload is via Claude's Google Drive
MCP, not this script.

**Dependencies:** Standard library only.

**Invocation:**

```bash
# Use default SKILLS folder ID
python sync_to_drive.py --skill-path /home/claude/skill-builds/my-skill

# Custom Drive parent folder
python sync_to_drive.py --skill-path ./my-skill --drive-parent 1AbCdEfGhIjKlMnOpQrStUv
```

**Output:** JSON manifest with the upload plan. Claude reads this and executes the
Drive MCP calls.

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Manifest produced |
| 1 | Skill path not found |
| 3 | Bad arguments |

---

## Common errors

### `ModuleNotFoundError: No module named 'requests'`

The scraper dependencies aren't installed. Run:

```bash
pip install requests beautifulsoup4 lxml
```

### `playwright install chromium` fails

Network issue or sandbox restriction. The skill-builder can fall back to scrape_static
alone — flag the limitation in the research note.

### `qa_check.py` keeps failing on `body_size`

SKILL.md is too long. Move detail to `references/` and link from the body. The 500-line
ceiling is hard.

### `package_skill.py` exit code 2

QA gate didn't pass. Run `qa_check.py` directly to see what failed. Fix, re-run gate,
then re-run package.

### Drive sync silently does nothing

`sync_to_drive.py` only produces a manifest. Claude must execute the Drive MCP calls
listed in the manifest's `agent_instructions`. If those aren't executed, nothing
uploads.
