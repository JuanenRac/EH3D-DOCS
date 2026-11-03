"""Tests of tools/changelog_pr_check.py on small throwaway git repositories."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import changelog_pr_check as check  # noqa: E402

EMPTY = "# Changelog\n\n## [Unreleased]\n\n## [0.1.0] - First\n\n- First release.\n"
WITH_LINE = "# Changelog\n\n## [Unreleased]\n\n- Fix the thing.\n\n## [0.1.0] - First\n\n- First release.\n"
RELEASED = "# Changelog\n\n## [Unreleased]\n\n## [0.1.1] - Next\n\n- Fix the thing.\n\n## [0.1.0] - First\n\n- First release.\n"


def run(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], cwd=root, check=True, capture_output=True)


class ChangelogPrCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        run(self.root, "init", "-q", "-b", "main")
        (self.root / "CHANGELOG.md").write_text(EMPTY, encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src" / "a.rs").write_text("fn a() {}\n", encoding="utf-8")
        run(self.root, "add", "CHANGELOG.md", "src/a.rs")
        run(self.root, "commit", "-q", "-m", "base")
        run(self.root, "checkout", "-q", "-b", "topic")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, files: dict):
        for name, text in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            run(self.root, "add", str(path.relative_to(self.root)))
        run(self.root, "commit", "-q", "-m", "change")

    def test_code_without_line_fails(self):
        self.commit({"src/a.rs": "fn a() { 1; }\n"})
        self.assertEqual(len(check.problems(self.root, "main")), 1)
        self.assertEqual(check.main(["--base", "main", "--root", str(self.root)]), 1)

    def test_code_with_line_passes(self):
        self.commit({"src/a.rs": "fn a() { 1; }\n", "CHANGELOG.md": WITH_LINE})
        self.assertEqual(check.problems(self.root, "main"), [])

    def test_docs_only_needs_no_line(self):
        self.commit({"README.md": "text\n"})
        self.assertEqual(check.problems(self.root, "main"), [])

    def test_release_heading_counts(self):
        self.commit({"src/a.rs": "fn a() { 1; }\n", "CHANGELOG.md": RELEASED})
        self.assertEqual(check.problems(self.root, "main"), [])

    def test_warn_only_exits_zero(self):
        self.commit({"src/a.rs": "fn a() { 1; }\n"})
        self.assertEqual(check.main(["--base", "main", "--root", str(self.root), "--warn-only"]), 0)

    def test_unknown_base_is_a_usage_error(self):
        self.assertEqual(check.main(["--base", "nope", "--root", str(self.root)]), 64)

    def test_entries_are_counted_under_unreleased_only(self):
        self.assertEqual(check.unreleased_entries(EMPTY), 0)
        self.assertEqual(check.unreleased_entries(WITH_LINE), 1)


if __name__ == "__main__":
    unittest.main()
