# =============================================================================
# EH3D-DOCS - tools/test_make_structure_ci.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The file tree of the READMEs and the Repository Structure picture are checked by the validator through make_structure.run_in_ci."""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
SPEC = importlib.util.spec_from_file_location("eh3d_make_structure_ci", TOOLS / "make_structure.py")
STRUCTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STRUCTURE)


def _copy_docs(target: Path) -> None:
    (target / "docs").mkdir()
    (target / "images").mkdir()
    shutil.copy(ROOT / "docs" / "structure.json", target / "docs" / "structure.json")
    for readme in ROOT.glob("README*.md"):
        shutil.copy(readme, target / readme.name)
    for svg in (ROOT / "images").glob("repository-structure*.svg"):
        shutil.copy(svg, target / "images" / svg.name)


class RunInCiTests(unittest.TestCase):
    def test_this_repository_passes(self):
        self.assertEqual(STRUCTURE.run_in_ci(ROOT), [])

    def test_a_repository_without_a_spec_has_no_tree_to_keep(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(STRUCTURE.run_in_ci(Path(folder)), [])

    def test_a_malformed_spec_is_a_reason_and_not_a_crash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "docs").mkdir()
            (root / "docs" / "structure.json").write_text("{}", encoding="utf-8")
            problems = STRUCTURE.run_in_ci(root)
            self.assertEqual(len(problems), 1)
            self.assertIn("docs/structure.json", problems[0])

    def test_a_readme_without_the_tree_of_its_language_is_a_reason(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            _copy_docs(root)
            path = root / "README_por.md"
            text = path.read_text(encoding="utf-8")
            first = STRUCTURE.render_tree(STRUCTURE.load_spec(root / "docs" / "structure.json"), "pt").splitlines()[1]
            self.assertIn(first, text)
            path.write_text(text.replace(first, "├── old-folder/"), encoding="utf-8")
            self.assertTrue(any("README_por.md does not carry the tree" in p for p in STRUCTURE.run_in_ci(root)))

    def test_a_picture_that_does_not_match_the_spec_is_a_reason(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            _copy_docs(root)
            picture = root / "images" / "repository-structure.svg"
            picture.write_text(picture.read_text(encoding="utf-8").replace("<svg", "<svg data-old=\"1\"", 1), encoding="utf-8")
            self.assertTrue(any("repository-structure.svg does not match" in p for p in STRUCTURE.run_in_ci(root)))


if __name__ == "__main__":
    unittest.main()
