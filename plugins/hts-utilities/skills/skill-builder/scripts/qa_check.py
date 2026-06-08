#!/usr/bin/env python3
"""
qa_check.py — Hard QA gate for skill-builder Phase 4.

Runs the structural checks defined in skill-builder/SKILL.md against a draft skill
folder. Every check must pass. There is no override. Returns pass/fail with detail.

Inputs:
    --skill-path PATH    Path to the skill folder to check (required)
    --json               Output machine-readable JSON instead of human-readable text
    --strict             Treat warnings as failures (default: warnings reported but pass)

Output (human):
    PASS / FAIL header
    Per-check status with offending line/file
    Suggested fix for any failure

Output (--json):
    {
      "skill_path": "...",
      "passed": true|false,
      "checks": [
        {"id": "name_kebab_case", "level": "fail|warn|pass", "detail": "...", "fix": "..."}
      ]
    }

Exit codes:
    0   All checks passed
    1   One or more checks failed
    2   Skill folder not found or unreadable
    3   Invalid arguments

Dependencies:
    pip install pyyaml

Usage:
    python qa_check.py --skill-path /home/claude/skill-builds/my-new-skill
    python qa_check.py --skill-path ./my-skill --json --strict
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Missing dependency: pyyaml. Run: pip install pyyaml\n")
    sys.exit(3)


# ---------- Constants ----------

KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_TOKENS = {"claude", "anthropic"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_BODY_LINES = 500
FORBIDDEN_DESCRIPTION_CHARS = ("<", ">")
DANGEROUS_PATTERNS = [
    re.compile(r"curl\s+[^\|]*\|\s*(bash|sh|zsh)"),
    re.compile(r"\beval\s*\("),
    re.compile(r"\bexec\s*\("),
    re.compile(r"wget\s+[^\|]*\|\s*(bash|sh)"),
    re.compile(r"requests\.get\([^)]*\)\.text\s*\)\s*$", re.MULTILINE),  # crude remote-exec detection
]


# ---------- Helpers ----------

def add_check(checks, check_id, level, detail, fix=""):
    checks.append({"id": check_id, "level": level, "detail": detail, "fix": fix})


def parse_frontmatter(skill_md_text):
    """Return (frontmatter_dict, body_text) or (None, error_message)."""
    if not skill_md_text.startswith("---"):
        return None, "SKILL.md does not start with --- frontmatter delimiter"

    parts = skill_md_text.split("---", 2)
    if len(parts) < 3:
        return None, "Frontmatter not properly closed with second ---"

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, f"Invalid YAML in frontmatter: {e}"

    if not isinstance(fm, dict):
        return None, "Frontmatter must be a YAML mapping"

    return fm, parts[2]


# ---------- Individual checks ----------

def check_skill_md_exists(skill_path: Path, checks):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        add_check(checks, "skill_md_exists", "fail",
                  f"SKILL.md not found at {skill_md}",
                  "Create SKILL.md (case-sensitive) at the root of the skill folder.")
        return False
    add_check(checks, "skill_md_exists", "pass", "SKILL.md present")
    return True


def check_folder_name(skill_path: Path, checks):
    name = skill_path.name
    ok = True
    if not KEBAB_CASE.match(name):
        add_check(checks, "folder_kebab_case", "fail",
                  f"Folder name '{name}' is not kebab-case",
                  "Rename folder to lowercase with hyphens, e.g. my-cool-skill.")
        ok = False
    if len(name) > MAX_NAME_LENGTH:
        add_check(checks, "folder_name_length", "fail",
                  f"Folder name '{name}' exceeds {MAX_NAME_LENGTH} chars",
                  f"Shorten the folder name to <={MAX_NAME_LENGTH} characters.")
        ok = False
    for token in RESERVED_TOKENS:
        if token in name.lower():
            add_check(checks, "folder_reserved_token", "fail",
                      f"Folder name contains reserved token '{token}'",
                      f"Rename the skill to avoid '{token}' anywhere in the name.")
            ok = False
    if ok:
        add_check(checks, "folder_name", "pass", f"Folder name '{name}' is valid")
    return ok


def check_frontmatter(skill_path: Path, checks):
    skill_md = skill_path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    fm, rest = parse_frontmatter(text)
    if fm is None:
        add_check(checks, "frontmatter_parseable", "fail", rest,
                  "Wrap frontmatter in --- delimiters and ensure valid YAML.")
        return None, None
    add_check(checks, "frontmatter_parseable", "pass", "Frontmatter parses cleanly")
    return fm, rest


def check_name_field(fm, skill_path: Path, checks):
    name = fm.get("name")
    if not name:
        add_check(checks, "name_present", "fail", "Frontmatter missing `name` field",
                  "Add `name: your-skill-name` to frontmatter.")
        return False
    if not isinstance(name, str) or not KEBAB_CASE.match(name):
        add_check(checks, "name_kebab_case", "fail",
                  f"`name` field '{name}' is not kebab-case",
                  "Use lowercase letters, numbers, and hyphens only.")
        return False
    if name != skill_path.name:
        add_check(checks, "name_matches_folder", "fail",
                  f"`name: {name}` does not match folder name '{skill_path.name}'",
                  f"Set `name` to '{skill_path.name}' or rename the folder to '{name}'.")
        return False
    for token in RESERVED_TOKENS:
        if token in name.lower():
            add_check(checks, "name_reserved_token", "fail",
                      f"`name` contains reserved token '{token}'",
                      "Rename to avoid 'claude' or 'anthropic'.")
            return False
    add_check(checks, "name_field", "pass", f"`name: {name}` is valid")
    return True


def check_description_field(fm, checks):
    desc = fm.get("description")
    if not desc:
        add_check(checks, "description_present", "fail",
                  "Frontmatter missing `description` field",
                  "Add a description that says WHAT the skill does and WHEN to use it.")
        return False
    desc = str(desc)
    if len(desc) > MAX_DESCRIPTION_LENGTH:
        add_check(checks, "description_length", "fail",
                  f"Description is {len(desc)} chars, max is {MAX_DESCRIPTION_LENGTH}",
                  "Trim the description and push detail into the SKILL.md body.")
        return False
    for ch in FORBIDDEN_DESCRIPTION_CHARS:
        if ch in desc:
            add_check(checks, "description_no_xml", "fail",
                      f"Description contains forbidden character '{ch}'",
                      "Remove all < and > characters from the description.")
            return False
    # Soft check: WHAT + WHEN signal
    when_signals = ["use when", "use this", "trigger", "whenever", "if the user", "asks to", "asks for"]
    has_when = any(sig in desc.lower() for sig in when_signals)
    if not has_when:
        add_check(checks, "description_has_when", "warn",
                  "Description doesn't seem to include a clear WHEN/trigger clause",
                  "Add a phrase like 'Use this skill when...' or list trigger phrases.")
    add_check(checks, "description_field", "pass", f"Description present ({len(desc)} chars)")
    return True


def check_body_size(body: str, checks):
    line_count = body.count("\n") + 1
    if line_count > MAX_SKILL_BODY_LINES:
        add_check(checks, "body_size", "fail",
                  f"SKILL.md body is {line_count} lines, exceeds {MAX_SKILL_BODY_LINES}",
                  "Push detail into references/ and link from SKILL.md.")
        return False
    add_check(checks, "body_size", "pass", f"Body is {line_count} lines")
    return True


def check_no_readme(skill_path: Path, checks):
    readme = skill_path / "README.md"
    if readme.exists():
        add_check(checks, "no_readme", "fail",
                  "README.md found inside skill folder",
                  "Move README.md to the repo root (one level up from the skill folder).")
        return False
    add_check(checks, "no_readme", "pass", "No README.md inside skill folder")
    return True


def check_scripts(skill_path: Path, checks):
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists():
        add_check(checks, "scripts_dir", "pass", "No scripts/ directory (optional)")
        return True

    all_ok = True
    for script in scripts_dir.iterdir():
        if not script.is_file():
            continue
        suffix = script.suffix
        text = script.read_text(encoding="utf-8", errors="replace")

        # Shebang for executable scripts
        if suffix in (".py", ".sh"):
            first_line = text.split("\n", 1)[0] if text else ""
            if not first_line.startswith("#!"):
                add_check(checks, f"script_shebang::{script.name}", "warn",
                          f"{script.name} has no shebang",
                          "Add #!/usr/bin/env python3 or #!/usr/bin/env bash on line 1.")

        # Syntax check
        if suffix == ".py":
            rv = subprocess.run([sys.executable, "-m", "py_compile", str(script)],
                                capture_output=True, text=True)
            if rv.returncode != 0:
                add_check(checks, f"script_syntax::{script.name}", "fail",
                          f"Python syntax error in {script.name}: {rv.stderr.strip()}",
                          "Fix the syntax error before shipping.")
                all_ok = False
        elif suffix == ".sh":
            rv = subprocess.run(["bash", "-n", str(script)],
                                capture_output=True, text=True)
            if rv.returncode != 0:
                add_check(checks, f"script_syntax::{script.name}", "fail",
                          f"Bash syntax error in {script.name}: {rv.stderr.strip()}",
                          "Fix the bash syntax error before shipping.")
                all_ok = False

        # Security: dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            if pattern.search(text):
                add_check(checks, f"script_security::{script.name}", "fail",
                          f"{script.name} contains a dangerous pattern (likely remote-exec)",
                          "Remove curl|bash, eval, or remote-fetch-and-execute constructs.")
                all_ok = False
                break

    if all_ok:
        add_check(checks, "scripts", "pass", "All scripts pass syntax and security checks")
    return all_ok


def check_references_exist(skill_path: Path, body: str, checks):
    """If SKILL.md mentions references/*.md, those files must exist."""
    referenced = re.findall(r"references/([\w\-/.]+\.md)", body)
    if not referenced:
        add_check(checks, "references_exist", "pass", "No reference files referenced")
        return True
    missing = []
    for ref in set(referenced):
        if not (skill_path / "references" / ref).exists():
            missing.append(ref)
    if missing:
        add_check(checks, "references_exist", "fail",
                  f"SKILL.md references missing files: {', '.join(missing)}",
                  "Create the missing reference files or remove the references.")
        return False
    add_check(checks, "references_exist", "pass",
              f"All {len(set(referenced))} referenced files exist")
    return True


# ---------- Main ----------

def run_checks(skill_path: Path, strict: bool) -> dict:
    checks = []
    skill_path = skill_path.resolve()

    if not skill_path.is_dir():
        return {
            "skill_path": str(skill_path),
            "passed": False,
            "checks": [{"id": "skill_path", "level": "fail",
                        "detail": "Skill path is not a directory",
                        "fix": "Pass a valid folder path."}],
        }

    if not check_skill_md_exists(skill_path, checks):
        return {"skill_path": str(skill_path), "passed": False, "checks": checks}

    check_folder_name(skill_path, checks)
    fm, body = check_frontmatter(skill_path, checks)
    if fm is not None:
        check_name_field(fm, skill_path, checks)
        check_description_field(fm, checks)
        check_body_size(body, checks)
        check_references_exist(skill_path, body, checks)
    check_no_readme(skill_path, checks)
    check_scripts(skill_path, checks)

    fail_levels = {"fail"}
    if strict:
        fail_levels.add("warn")
    passed = not any(c["level"] in fail_levels for c in checks)

    return {"skill_path": str(skill_path), "passed": passed, "checks": checks}


def render_human(report: dict) -> str:
    lines = []
    header = "PASS" if report["passed"] else "FAIL"
    lines.append(f"=== QA Gate: {header} ===")
    lines.append(f"Skill: {report['skill_path']}")
    lines.append("")
    for c in report["checks"]:
        marker = {"pass": "✓", "warn": "⚠", "fail": "✗"}.get(c["level"], "?")
        lines.append(f"  {marker} [{c['level'].upper()}] {c['id']}")
        if c.get("detail"):
            lines.append(f"      → {c['detail']}")
        if c.get("fix") and c["level"] != "pass":
            lines.append(f"      Fix: {c['fix']}")
    lines.append("")
    failures = [c for c in report["checks"] if c["level"] == "fail"]
    warnings = [c for c in report["checks"] if c["level"] == "warn"]
    lines.append(f"Summary: {len(failures)} failure(s), {len(warnings)} warning(s), "
                 f"{sum(1 for c in report['checks'] if c['level'] == 'pass')} pass(es)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="QA gate for skill-builder Phase 4.")
    parser.add_argument("--skill-path", required=True, help="Path to the skill folder")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    report = run_checks(Path(args.skill_path), strict=args.strict)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_human(report))

    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
