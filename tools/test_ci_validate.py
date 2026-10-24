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


if __name__ == "__main__":
    unittest.main()
