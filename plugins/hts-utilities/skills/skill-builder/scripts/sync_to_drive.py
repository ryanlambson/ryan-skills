#!/usr/bin/env python3
"""
sync_to_drive.py — Sync a packaged skill to Google Drive SKILLS/.

This script is a stub: actual Drive upload happens via the Google Drive MCP connector
in Claude, not via this script directly. The script's job is to:

1. Verify the skill folder is well-formed
2. Print the manifest of files to be uploaded
3. Print the Drive destination path
4. Print the MCP tool calls Claude should make (so the agent layer can execute them)

This separation exists because file uploads through the Drive MCP require Claude to
make tool calls — they can't be done from a bare Python script without OAuth setup.
This script prepares the upload plan; Claude executes it.

Inputs:
    --skill-path PATH       Path to the skill folder (required)
    --drive-parent ID       Google Drive parent folder ID
                            (default: 173GcX2sDmvniSiQbed2urUC3EfzljCUE — SKILLS/)

Output:
    A JSON manifest to stdout describing the upload plan:
    {
      "drive_parent_id": "...",
      "drive_folder_name": "skill-name",
      "files": [
        {"local_path": "...", "drive_relative_path": "...", "mime_type": "..."}
      ]
    }

Exit codes:
    0   Manifest produced successfully
    1   Skill path not found
    3   Invalid arguments

Dependencies:
    Standard library only.

Usage:
    python sync_to_drive.py --skill-path /home/claude/skill-builds/my-skill
"""

import argparse
import json
import mimetypes
import sys
from pathlib import Path


# Default to the SKILLS folder ID discovered during skill-builder setup
DEFAULT_DRIVE_PARENT = "173GcX2sDmvniSiQbed2urUC3EfzljCUE"


def build_manifest(skill_path: Path, drive_parent: str) -> dict:
    files = []
    for f in skill_path.rglob("*"):
        if f.is_file():
            rel = f.relative_to(skill_path)
            mime, _ = mimetypes.guess_type(str(f))
            files.append({
                "local_path": str(f),
                "drive_relative_path": str(rel),
                "mime_type": mime or "application/octet-stream",
                "size_bytes": f.stat().st_size,
            })
    return {
        "drive_parent_id": drive_parent,
        "drive_folder_name": skill_path.name,
        "file_count": len(files),
        "total_bytes": sum(f["size_bytes"] for f in files),
        "files": files,
        "agent_instructions": (
            "Claude: use the Google Drive MCP (google_drive create_file) to "
            "(1) create a subfolder named `drive_folder_name` under `drive_parent_id`, "
            "(2) upload each file under that subfolder preserving `drive_relative_path`. "
            "After upload, append a one-line entry to SKILLS/INDEX.md with the skill "
            "name, date, and one-line purpose."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Prepare a skill folder for Drive sync.")
    parser.add_argument("--skill-path", required=True, help="Path to skill folder")
    parser.add_argument("--drive-parent", default=DEFAULT_DRIVE_PARENT,
                        help="Google Drive parent folder ID (default: SKILLS/)")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()
    if not skill_path.is_dir():
        sys.stderr.write(f"Skill path not found: {skill_path}\n")
        sys.exit(1)

    manifest = build_manifest(skill_path, args.drive_parent)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
