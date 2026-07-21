#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "i-have-adhd-and-47-tabs"
SKILL_DIR = ROOT / NAME
SKILL = SKILL_DIR / "SKILL.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if SKILL_DIR.name != NAME:
        fail("skill folder name does not match expected name")
    if not SKILL.is_file():
        fail(f"missing {SKILL.relative_to(ROOT)}")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    frontmatter = parts[1]

    name_match = re.search(r"(?m)^name:\s*(.+?)\s*$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)
    if not name_match or name_match.group(1) != NAME:
        fail(f"frontmatter name must be {NAME}")
    if not description_match:
        fail("frontmatter description is required")
    if not description_match.group(1).startswith("Use when"):
        fail("description must start with 'Use when'")
    if len(frontmatter) > 2048:
        fail("frontmatter is unexpectedly large")

    required_files = [
        SKILL_DIR / "agents" / "openai.yaml",
        SKILL_DIR / "references" / "examples.md",
        SKILL_DIR / "LICENSE",
        SKILL_DIR / "NOTICE.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing:
        fail(f"missing supporting files: {', '.join(missing)}")

    required_attribution = "https://github.com/ayghri/i-have-adhd"
    if required_attribution not in text:
        fail("SKILL.md must retain upstream attribution")

    print(f"OK: {NAME} source package is valid")


if __name__ == "__main__":
    main()
