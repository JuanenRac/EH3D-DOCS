# =============================================================================
# EH3D-DOCS - tools/test_ci_validate.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check that the file tree of every README lists each versioned first-level entry (tools/ci_validate.py)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
SPEC = importlib.util.spec_from_file_location("eh3d_ci_validate", TOOLS / "ci_validate.py")
VALIDATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE)

TREE = "\n".join([
    "## Structure",
    "",
    "```text",
    "EH3D-TEST/",
    "├── src/          the code",
    "├── tools/ci_validate.py, build_test.py  the checks",
    "├── build.sh / build.bat",
    "├── update.sh/.bat  the updater",
    "├── CMakeLists.txt, sdkconfig.board.*  the project",
    "└── eh3d.project.json",
    "```",
    "",
])


class TreeTests(unittest.TestCase):
    def test_the_first_level_names_are_read_from_the_tree(self):
        names = VALIDATE.tree_names(TREE)
        self.assertTrue({"src", "tools", "update.sh", "update.bat", "CMakeLists.txt", "sdkconfig.board.*"} <= names)
        self.assertNotIn("ci_validate.py", names)

    def test_a_readme_without_a_tree_has_no_names(self):
        self.assertIsNone(VALIDATE.tree_names("## Structure\n\nNo tree here.\n"))

    def test_the_tree_is_the_code_block_with_the_most_tree_rows(self):
        names = VALIDATE.tree_names("```text\n├── sample/  one row\n```\n\n" + TREE)
        self.assertIn("tools", names)
        self.assertNotIn("sample", names)

    def test_a_versioned_entry_the_tree_leaves_out_is_named(self):
        with tempfile.TemporaryDirectory() as folder:
            original = VALIDATE.ROOT
            VALIDATE.ROOT = Path(folder)
            try:
                (Path(folder) / "README.md").write_text(TREE, encoding="utf-8")
                tracked = ["src", "tools", "CMakeLists.txt", "sdkconfig.board.s3-eth", "schemas", "partitions.csv", "README.md", ".github", "eh3d.project.json", "Cargo.toml"]
                (problem,) = VALIDATE.tree_problems(tracked)
            finally:
                VALIDATE.ROOT = original
        self.assertIn("README.md file tree does not list: schemas, partitions.csv", problem)

    def test_the_files_of_every_repository_are_not_asked_for(self):
        with tempfile.TemporaryDirectory() as folder:
            original = VALIDATE.ROOT
            VALIDATE.ROOT = Path(folder)
            try:
                (Path(folder) / "README.md").write_text(TREE, encoding="utf-8")
                tracked = ["src", "tools", "CMakeLists.txt", "LICENSE", "CHANGELOG.md", "README_spa.md", ".gitignore", "images", "build_firmware.sh", "Cargo.lock"]
                self.assertEqual(VALIDATE.tree_problems(tracked), [])
            finally:
                VALIDATE.ROOT = original


class CanonicalTests(unittest.TestCase):
    def test_the_version_is_read_where_the_manifest_says(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "Cargo.toml").write_text('[package]\nname = "x"\nversion = "1.2.3"\n', encoding="utf-8")
            (root / "build.gradle").write_text('versionName = "0.0.7"\n', encoding="utf-8")
            (root / "version.h").write_text("#define MAJOR 0\n#define MINOR 8\n#define PATCH 1\n#define BUILD 2\n", encoding="utf-8")
            self.assertEqual(VALIDATE.native_version(root, {"file": "Cargo.toml", "pattern": r'^version\s*=\s*"(\d+\.\d+\.\d+)"'}), ("1.2.3", "Cargo.toml"))
            self.assertEqual(VALIDATE.native_version(root, {"file": "build.gradle", "pattern": r'versionName\s*=\s*"([^"]+)"'}), ("0.0.7", "build.gradle"))
            three = {"file": "Cargo.toml", "pattern": r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"'}
            self.assertEqual(VALIDATE.native_version(root, three)[0], "1.2.3")
            parts = {"file": "version.h", "pattern": {k: rf"#define {k.upper()} (\d+)" for k in ("major", "minor", "patch", "build")}}
            self.assertEqual(VALIDATE.native_version(root, parts)[0], "0.8.1.2")

    def test_a_missing_or_wrong_native_file_gives_a_question_mark_not_a_crash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(VALIDATE.native_version(root, {"file": "nothing.toml"}), ("?", "nothing.toml"))
            (root / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
            self.assertEqual(VALIDATE.native_version(root, {"file": "Cargo.toml", "pattern": r'^version = "(.+)"'})[0], "?")

    def test_the_data_of_a_repository_comes_from_ci_config_json(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(VALIDATE.load_config(root), ({}, []))
            self.assertEqual(VALIDATE.skip_dirs({}), {"target", ".git"})
            (root / "tools").mkdir()
            (root / "tools" / "ci_config.json").write_text('{"skip_dirs": ["local-data", "re"]}', encoding="utf-8")
            config, problems = VALIDATE.load_config(root)
            self.assertEqual(problems, [])
            self.assertEqual(VALIDATE.skip_dirs(config), {"target", ".git", "local-data", "re"})

    def test_a_damaged_ci_config_is_a_problem(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "tools").mkdir()
            for text in ("{ not json", "[1]", '{"skip_dirs": "re"}', '{"skip_dirs": [1]}'):
                (root / "tools" / "ci_config.json").write_text(text, encoding="utf-8")
                config, problems = VALIDATE.load_config(root)
                self.assertEqual(config, {})
                self.assertEqual(len(problems), 1, text)

    def test_the_header_states_the_tools_version_of_the_code(self):
        with tempfile.TemporaryDirectory() as folder:
            copy = Path(folder) / "ci_validate.py"
            copy.write_text(f"#!/usr/bin/env python3\n# EH3D-X\n# canonical: EH3D-DOCS tools {VALIDATE.TOOLS_VERSION}\n\"\"\"x\"\"\"\n", encoding="utf-8")
            self.assertEqual(VALIDATE.header_problems(copy), [])
            copy.write_text("# EH3D-X\n# canonical: EH3D-DOCS tools 0\n\"\"\"x\"\"\"\n", encoding="utf-8")
            self.assertIn("header says canonical tools 0", VALIDATE.header_problems(copy)[0])
            copy.write_text("# EH3D-X\n\"\"\"x\"\"\"\n", encoding="utf-8")
            self.assertIn("header says canonical tools None", VALIDATE.header_problems(copy)[0])
        self.assertEqual(VALIDATE.header_problems(), [])  # this very file

    def test_an_ios_project_shows_the_version_of_the_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(VALIDATE.project_yml_problems(root, "0.0.6"), [])
            (root / "project.yml").write_text('MARKETING_VERSION: "0.0.5"\nCFBundleShortVersionString: "0.0.5"\n', encoding="utf-8")
            self.assertEqual(len(VALIDATE.project_yml_problems(root, "0.0.6")), 2)
            (root / "project.yml").write_text('MARKETING_VERSION: "0.0.6"\nCFBundleShortVersionString: "$(MARKETING_VERSION)"\n', encoding="utf-8")
            self.assertEqual(VALIDATE.project_yml_problems(root, "0.0.6"), [])

    def test_the_last_line_keeps_its_format_and_adds_the_tools_version(self):
        import subprocess
        import sys

        out = subprocess.run([sys.executable, "-I", str(TOOLS / "ci_validate.py")], capture_output=True, text=True, cwd=TOOLS.parent).stdout.strip().splitlines()[-1]
        self.assertRegex(out, r"^CI_VALIDATION=PASS project=EH3D-DOCS version=\d+(\.\d+){2,3} tools=" + VALIDATE.TOOLS_VERSION + "$")

    def test_the_scan_for_forbidden_words_reads_only_the_files_git_tracks(self):
        import subprocess

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "kept.md").write_text("x", encoding="utf-8")
            (root / ".venv").mkdir()
            (root / ".venv" / "package.md").write_text("cl" + "aude", encoding="utf-8")
            subprocess.run(["git", "add", "kept.md"], cwd=root, check=True)
            old = VALIDATE.ROOT
            VALIDATE.ROOT = root
            try:
                self.assertEqual([p.name for p in VALIDATE.scan_files()], ["kept.md"])
                subprocess.run(["git", "rm", "-q", "--cached", "kept.md"], cwd=root, check=True)
                self.assertEqual(VALIDATE.scan_files(), [])
            finally:
                VALIDATE.ROOT = old

    def test_the_scan_falls_back_to_every_file_outside_a_git_checkout(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.md").write_text("x", encoding="utf-8")
            old = VALIDATE.ROOT
            VALIDATE.ROOT = root
            try:
                import unittest.mock as mock
                with mock.patch("subprocess.run", side_effect=OSError):
                    self.assertEqual([p.name for p in VALIDATE.scan_files()], ["a.md"])
            finally:
                VALIDATE.ROOT = old


if __name__ == "__main__":
    unittest.main()
