from __future__ import annotations

import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "i-have-adhd-and-47-tabs"
SKILL_DIR = ROOT / SKILL_NAME
DIST_ZIP = ROOT / "dist" / f"{SKILL_NAME}.zip"


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
            SKILL_DIR / "agents" / "openai.yaml",
            SKILL_DIR / "references" / "examples.md",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")

    def test_skill_frontmatter_is_discoverable(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, rf"(?m)^name: {re.escape(SKILL_NAME)}$")
        description = re.search(r"(?m)^description:\s*(.+)$", text)
        self.assertIsNotNone(description)
        assert description is not None
        self.assertTrue(description.group(1).startswith("Use when"))
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
        ]:
            self.assertIn(required, text)

    def test_license_preserves_original_notice(self) -> None:
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Ayoub Ghriss", text)
        self.assertIn("Copyright (c) 2026 Zachary Brenner", text)
        self.assertIn("MIT License", text)

    def test_openai_metadata_uses_new_name(self) -> None:
        text = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "I Have ADHD and 47 Tabs"', text)
        self.assertIn(SKILL_NAME, text)
        self.assertIn("allow_implicit_invocation: true", text)

    def test_publish_script_can_initialize_unpacked_repository(self) -> None:
        text = (ROOT / "scripts" / "publish_to_github.sh").read_text(encoding="utf-8")
        self.assertIn("git init -b main", text)
        self.assertIn("git add .", text)
        self.assertIn("gh repo create", text)


    def test_distribution_zip_has_one_top_level_skill_folder(self) -> None:
        self.assertTrue(DIST_ZIP.is_file(), f"Missing {DIST_ZIP.relative_to(ROOT)}")
        with zipfile.ZipFile(DIST_ZIP) as archive:
            self.assertIsNone(archive.testzip())
            names = [name for name in archive.namelist() if name and not name.endswith("/")]
        top_levels = {name.split("/", 1)[0] for name in names}
        self.assertEqual(top_levels, {SKILL_NAME})
        self.assertIn(f"{SKILL_NAME}/SKILL.md", names)
        self.assertNotIn("__MACOSX", "\n".join(names))


if __name__ == "__main__":
    unittest.main()
