#!/usr/bin/env python3
"""
package_skill.py — Zip a skill folder for upload.

Used by skill-builder after the QA gate passes. Produces a .zip ready for upload to
Claude.ai (Settings → Capabilities → Skills) or for placement in a Claude Code skills
directory.

Inputs:
    --skill-path PATH    Path to the skill folder to package (required)
    --output-dir PATH    Where to write the zip (default: /mnt/user-data/outputs/)

Output:
    A zip file at {output-dir}/{skill-name}.zip

Exit codes:
    0   Success (zip created)
    1   Skill path not found
    2   QA gate has not passed (refuse to package)
    3   Zip creation failed

Dependencies:
    Standard library only.

Usage:
    python package_skill.py --skill-path /home/claude/skill-builds/my-skill
    python package_skill.py --skill-path ./my-skill --output-dir /tmp
"""

import argparse
import shutil
import sys
import subprocess
import zipfile
from pathlib import Path


# Files and folders that should never end up in the packaged skill
EXCLUDE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
    "Thumbs.db",
    ".git",
    ".gitignore",
    "node_modules",
    ".venv",
    "venv",
    ".env",
}


def should_skip(path: Path) -> bool:
    """Return True if path matches any exclusion pattern."""
    parts = set(path.parts)
    return bool(parts & EXCLUDE_PATTERNS) or path.suffix in {".pyc", ".pyo"}


def make_clean_zip(skill_path: Path, output_path: Path) -> str:
    """Zip the skill folder, excluding cruft. Returns the output path as string."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in skill_path.rglob("*"):
            rel = f.relative_to(skill_path.parent)
            if should_skip(rel):
                continue
            zf.write(f, arcname=str(rel))
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Package a skill folder as a zip.")
    parser.add_argument("--skill-path", required=True, help="Path to skill folder")
    parser.add_argument("--output-dir", default="/mnt/user-data/outputs/",
                        help="Where to write the zip")
    parser.add_argument("--skip-qa", action="store_true",
                        help="Skip the QA gate check (NOT recommended)")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()
    if not skill_path.is_dir():
        sys.stderr.write(f"Skill path not found: {skill_path}\n")
        sys.exit(1)

    # Refuse to package if QA hasn't passed
    if not args.skip_qa:
        qa_script = Path(__file__).parent / "qa_check.py"
        if qa_script.exists():
            rv = subprocess.run(
                [sys.executable, str(qa_script), "--skill-path", str(skill_path)],
                capture_output=True, text=True,
            )
            if rv.returncode != 0:
                sys.stderr.write("QA gate has not passed. Refusing to package.\n")
                sys.stderr.write(rv.stdout)
                sys.exit(2)
        else:
            sys.stderr.write(f"Warning: qa_check.py not found at {qa_script}\n")

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / f"{skill_path.name}.zip"
    try:
        archive = make_clean_zip(skill_path, zip_path)
    except Exception as e:
        sys.stderr.write(f"Zip creation failed: {e}\n")
        sys.exit(3)

    print(archive)


if __name__ == "__main__":
    main()
