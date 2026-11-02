# =============================================================================
# EH3D-DOCS - tools/test_vendored_tools_report.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/vendored_tools_report.py on a toy workspace."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import _toy_repo as toy
import vendored_tools_report as vtr


class VendoredToolsTests(unittest.TestCase):
    def make(self, tmp: str) -> Path:
        repo = toy.make_repo(Path(tmp))
        toy.write(repo, ".github/workflows/ci.yml", "steps:\n  - run: python -I tools/ci_validate.py\n  - run: python tools/make_pictures.py --check\n")
        toy.write(repo, "tools/ci_validate.py", "import helper_lib\n")
        toy.write(repo, "tools/helper_lib.py", "X = 1\n")
        toy.write(repo, "tools/make_pictures.py", "print(1)\n")
        toy.write(repo, "tools/by_script.py", "print(2)\n")
        toy.write(repo, "run.sh", "python tools/by_script.py\n")
        toy.write(repo, "tools/only_tested.py", "Y = 1\n")
        toy.write(repo, "tools/test_only_tested.py", "import only_tested\n")
        toy.write(repo, "tools/only_documented.py", "print(3)\n")
        toy.write(repo, "docs/NOTES.md", "Run `tools/only_documented.py` by hand.\n")
        toy.write(repo, "tools/forgotten.py", "print(4)\n")
        toy.write(repo, "tools/chain_a.py", "import chain_b\n")
        toy.write(repo, "tools/chain_b.py", "print(5)\n")
        toy.write(repo, "tools/__init__.py", "")
        return repo

    def test_what_a_workflow_a_script_or_a_used_tool_names_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = vtr.analyse(self.make(tmp))
            self.assertEqual(result["used"], ["by_script.py", "ci_validate.py", "helper_lib.py", "make_pictures.py"])

    def test_the_rest_says_what_still_names_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unreached = vtr.analyse(self.make(tmp))["unreached"]
            self.assertEqual(sorted(unreached), ["chain_a.py", "chain_b.py", "forgotten.py", "only_documented.py", "only_tested.py"])
            self.assertEqual(unreached["only_tested.py"], ["tests"])
            self.assertEqual(unreached["only_documented.py"], ["documents"])
            self.assertEqual(unreached["forgotten.py"], [])
            self.assertEqual(unreached["chain_b.py"], ["tool chain_a.py"])

    def test_the_report_lists_without_deleting_and_is_the_same_twice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make(tmp)
            before = sorted(p.name for p in (repo / "tools").iterdir())
            text, total = vtr.report(Path(tmp))
            again, _ = vtr.report(Path(tmp))
            self.assertEqual(text, again)
            self.assertEqual(total, 5)
            self.assertIn("| EH3D-TOY | 9 | 4 | 5 |", text)
            self.assertIn("| `forgotten.py` | nothing |", text)
            self.assertEqual(before, sorted(p.name for p in (repo / "tools").iterdir()))

    def test_write_puts_the_report_in_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.make(tmp)
            target = Path(tmp) / "report.md"
            self.assertEqual(vtr.main(["--workspace", tmp, "--write", str(target)]), 0)
            self.assertTrue(target.read_text(encoding="utf-8").startswith("# Vendored tools that nothing uses"))

    def test_a_workspace_without_unused_tools_says_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp))
            toy.write(repo, "tools/ci_validate.py", "print(1)\n")
            toy.write(repo, ".github/workflows/ci.yml", "run: python tools/ci_validate.py\n")
            text, total = vtr.report(Path(tmp))
            self.assertEqual(total, 0)
            self.assertIn("None.", text)


if __name__ == "__main__":
    unittest.main()
