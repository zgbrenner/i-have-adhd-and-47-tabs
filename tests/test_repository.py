from __future__ import annotations

import re
import struct
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
SOCIAL_PREVIEW = ROOT / "assets" / "social-preview.png"


class RepositoryContractTests(unittest.TestCase):
    def test_required_repository_files_exist(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "LICENSE",
            ROOT / "NOTICE.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            ROOT / "CHANGELOG.md",
            ROOT / "CITATION.cff",
            ROOT / "PUBLISH.md",
            ROOT / "VERSION",
            ROOT / "docs" / "DIRECTORY_SUBMISSIONS.md",
            ROOT / "docs" / "DISCUSSION_SEEDS.md",
            ROOT / "docs" / "releases" / "1.1.0.md",
            ROOT / "scripts" / "publish_to_github.sh",
            ROOT / ".github" / "workflows" / "release.yml",
            ROOT / ".github" / "workflows" / "seed-discussions.yml",
            ROOT / ".github" / "workflows" / "codeql.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "behavior-improvement.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "platform-compatibility.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "ideas.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "q-a.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "show-and-tell.yml",
            SOCIAL_PREVIEW,
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
            SKILL_DIR / "references" / "examples.md",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")
        self.assertFalse((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse(ROOT_ZIP.exists(), "Only the dist/ ZIP should be tracked")
        self.assertFalse((ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists())
        self.assertFalse((ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").exists())

    def test_versions_are_synchronized(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        release_notes = ROOT / "docs" / "releases" / f"{version}.md"

        self.assertIn(f'version: "{version}"', skill)
        self.assertIn(f"version: {version}", citation)
        self.assertIn(f"## {version}", changelog)
        self.assertTrue(release_notes.is_file())

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

    def test_readme_has_distribution_and_platform_paths(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in [
            "I Have ADHD and 47 Tabs",
            "Claude",
            "ChatGPT",
            "Custom GPT",
            "Codex",
            "GitHub Copilot",
            "gh skill install",
            "npx skills add",
            "releases/latest/download/i-have-adhd-and-47-tabs.zip",
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

    def test_security_and_support_routes_are_explicit(self) -> None:
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("security/advisories/new", security)
        self.assertIn("Private vulnerability reporting", security)
        self.assertIn("Discussions", support)
        self.assertIn("medical", support.lower())

    def test_issue_and_discussion_forms_are_structured(self) -> None:
        bug = (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml").read_text(encoding="utf-8")
        discussion = (ROOT / ".github" / "DISCUSSION_TEMPLATE" / "q-a.yml").read_text(encoding="utf-8")
        seed = (ROOT / ".github" / "workflows" / "seed-discussions.yml").read_text(encoding="utf-8")
        self.assertIn("type: dropdown", bug)
        self.assertIn("required: true", bug)
        self.assertIn("type: textarea", discussion)
        self.assertIn("discussions: write", seed)
        self.assertIn("Welcome to I Have ADHD and 47 Tabs", seed)
        self.assertIn("Which language should we translate next?", seed)

    def test_release_workflow_publishes_versioned_assets(self) -> None:
        text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("sha256sum", text)
        self.assertIn("gh release create", text)
        self.assertIn("dist/i-have-adhd-and-47-tabs.zip", text)
        self.assertIn("dist/SHA256SUMS", text)
        self.assertIn('docs/releases/$VERSION.md', text)

    def test_social_preview_has_recommended_dimensions(self) -> None:
        data = SOCIAL_PREVIEW.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1280, 640))

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
