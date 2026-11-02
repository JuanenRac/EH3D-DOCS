# =============================================================================
# EH3D-DOCS - tools/test_readme_staleness.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/readme_staleness.py on a toy repository whose commits have chosen times."""
from __future__ import annotations

import contextlib
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import _toy_repo as toy
import readme_staleness as rs

DAY = 86400
START = 1_700_000_000


def commit(repo: Path, message: str, at: int) -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME="Toy", GIT_AUTHOR_EMAIL="toy@example.invalid", GIT_COMMITTER_NAME="Toy",
               GIT_COMMITTER_EMAIL="toy@example.invalid", GIT_AUTHOR_DATE=f"{at} +0000", GIT_COMMITTER_DATE=f"{at} +0000")
    subprocess.run(["git", "add", "-A"], cwd=repo, env=env, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", message], cwd=repo, env=env, check=True, capture_output=True)


def edit(repo: Path, name: str, old: str, new: str) -> None:
    path = repo / name
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


class StalenessTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = toy.make_repo(Path(self._tmp.name))
        toy.git(self.repo, "init", "-b", "main")
        commit(self.repo, "start", START)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_translations_written_together_are_not_stale(self) -> None:
        findings, notes = rs.staleness(self.repo)
        self.assertEqual((findings, notes), ([], []))

    def test_a_section_changed_only_in_english_is_told_for_every_other_language(self) -> None:
        edit(self.repo, "README.md", "| Tests | 5 |", "| Tests | 6 |")
        commit(self.repo, "english only", START + 10 * DAY)
        findings, _ = rs.staleness(self.repo)
        self.assertEqual(len(findings), 7)
        self.assertTrue(all("'\U0001F4CB At a glance'" in f and "10 days older" in f for f in findings), findings)

    def test_a_translation_that_caught_up_is_not_told(self) -> None:
        edit(self.repo, "README.md", "| Tests | 5 |", "| Tests | 6 |")
        commit(self.repo, "english", START + 10 * DAY)
        for name in toy.LANGS:
            if name != "README.md":
                edit(self.repo, name, "| Tests | 5 |", "| Tests | 6 |")
        commit(self.repo, "translations", START + 10 * DAY + 3600)
        self.assertEqual(rs.staleness(self.repo)[0], [])

    def test_one_language_behind_only_names_that_language_and_that_section(self) -> None:
        edit(self.repo, "README.md", "| `key` |", "| `other` |")
        commit(self.repo, "english", START + 5 * DAY)
        for name in toy.LANGS:
            if name not in ("README.md", "README_jpn.md"):
                edit(self.repo, name, "| `key` |", "| `other` |")
        commit(self.repo, "most translations", START + 5 * DAY + 60)
        findings, _ = rs.staleness(self.repo)
        self.assertEqual(len(findings), 1)
        self.assertIn("README_jpn.md", findings[0])
        self.assertIn("'Configuration'", findings[0])

    def test_the_grace_can_be_changed(self) -> None:
        edit(self.repo, "README.md", "| Tests | 5 |", "| Tests | 6 |")
        commit(self.repo, "english", START + 2 * 3600)
        self.assertEqual(rs.staleness(self.repo)[0], [])
        self.assertEqual(len(rs.staleness(self.repo, grace_seconds=60)[0]), 7)

    def test_other_structures_are_noted_not_compared(self) -> None:
        edit(self.repo, "README_spa.md", "## Configuration", "## Configuration\n\n## Extra")
        commit(self.repo, "extra", START + DAY)
        findings, notes = rs.staleness(self.repo)
        self.assertEqual(findings, [])
        self.assertTrue(any("README_spa.md" in n and "cannot be compared" in n for n in notes), notes)

    def test_it_never_fails_and_works_without_git(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bare = toy.make_repo(Path(tmp), name="EH3D-NOGIT")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = rs.main([str(bare)])
            self.assertEqual(code, 0)
            self.assertIn("README_STALENESS sections=0", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
