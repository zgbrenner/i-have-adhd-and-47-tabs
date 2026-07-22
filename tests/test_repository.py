from __future__ import annotations

import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "i-have-adhd-and-47-tabs"
SKILL_DIR = ROOT / SKILL_NAME
DIST_ZIP = ROOT / "dist" / f"{SKILL_NAME}.zip"
ROOT_ZIP = ROOT / f"{SKILL_NAME}.zip"


class RepositoryContractTests(unittest.TestCase):
    def test_required_repository_files_exist(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "LICENSE",
            ROOT / "NOTICE.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / "CHANGELOG.md",
            ROOT / "PUBLISH.md",
            ROOT / "scripts" / "publish_to_github.sh",
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
            SKILL_DIR / "references" / "examples.md",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")
        self.assertFalse((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse(ROOT_ZIP.exists(), "Only the dist/ ZIP should be tracked")

    def test_skill_frontmatter_is_discoverable(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, rf"(?m)^name: {re.escape(SKILL_NAME)}$")
        description = re.search(r"(?m)^description:\s*(.+)$", text)
        self.assertIsNotNone(description)
        assert description is not None
        value = description.group(1)
        self.assertLessEqual(len(value), 1024)
        self.assertIn("Structures responses", value)
        self.assertIn("Use for", value)
        self.assertIn("especially when", value)
        self.assertIn("https://github.com/ayghri/i-have-adhd", text)

    def test_readme_has_installation_and_upstream_credit(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in [
            "I Have ADHD and 47 Tabs",
            "Claude",
            "ChatGPT",
            "Custom GPT",
            "Ayoub Ghriss",
            "https://github.com/ayghri/i-have-adhd",
            "MIT",
            "Make progress and wins visible",
        ]:
            self.assertIn(required, text)
        self.assertNotIn("agents/openai.yaml", text)
        self.assertNotRegex(text, r"(?m)^python scripts/")

    def test_license_preserves_original_notice(self) -> None:
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Ayoub Ghriss", text)
        self.assertIn("Copyright (c) 2026 Zachary Brenner", text)
        self.assertIn("MIT License", text)

    def test_examples_are_general_purpose(self) -> None:
        text = (SKILL_DIR / "references" / "examples.md").read_text(encoding="utf-8")
        self.assertIn("scholarship form", text)
        self.assertNotIn("Claude rejected the ZIP", text)
        self.assertNotIn("Re-upload the ZIP", text)

    def test_publish_script_rebuilds_commits_and_pushes_current_branch(self) -> None:
        text = (ROOT / "scripts" / "publish_to_github.sh").read_text(encoding="utf-8")
        self.assertIn("git init -b main", text)
        self.assertIn("git add --all", text)
        self.assertIn("git diff --cached --quiet", text)
        self.assertIn("git branch --show-current", text)
        self.assertIn('git push -u origin "$BRANCH"', text)
        self.assertIn("ORIGIN_REPO", text)
        self.assertNotRegex(text, r"(?m)^python scripts/")

    def test_distribution_zip_has_one_top_level_skill_folder(self) -> None:
        self.assertTrue(DIST_ZIP.is_file(), f"Missing {DIST_ZIP.relative_to(ROOT)}")
        with zipfile.ZipFile(DIST_ZIP) as archive:
            self.assertIsNone(archive.testzip())
            names = [name for name in archive.namelist() if name and not name.endswith("/")]
        top_levels = {name.split("/", 1)[0] for name in names}
        self.assertEqual(top_levels, {SKILL_NAME})
        self.assertIn(f"{SKILL_NAME}/SKILL.md", names)
        self.assertNotIn(f"{SKILL_NAME}/agents/openai.yaml", names)
        self.assertNotIn("__MACOSX", "\n".join(names))

    def test_build_ignores_common_stray_files(self) -> None:
        ds_store = SKILL_DIR / ".DS_Store"
        cache_dir = SKILL_DIR / "__pycache__"
        cache_file = cache_dir / "junk.pyc"
        backup = SKILL_DIR / "notes.md~"
        cache_dir.mkdir(exist_ok=True)
        ds_store.write_bytes(b"junk")
        cache_file.write_bytes(b"junk")
        backup.write_text("junk", encoding="utf-8")
        try:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build_zip.py")],
                check=True,
                cwd=ROOT,
            )
            with zipfile.ZipFile(DIST_ZIP) as archive:
                names = set(archive.namelist())
            self.assertNotIn(f"{SKILL_NAME}/.DS_Store", names)
            self.assertNotIn(f"{SKILL_NAME}/__pycache__/junk.pyc", names)
            self.assertNotIn(f"{SKILL_NAME}/notes.md~", names)
        finally:
            ds_store.unlink(missing_ok=True)
            cache_file.unlink(missing_ok=True)
            backup.unlink(missing_ok=True)
            cache_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
