# =============================================================================
# EH3D-DOCS - tools/test_version_places_round2.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Native versions given as one regex per number, a manifest that is not an object, the folders the file search never enters and the writes of a bump."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import _toy_repo as toy
import version_places as vp


def with_parts(root: Path) -> Path:
    repo = toy.make_repo(root, version="0.8.0.1")
    manifest = json.loads((repo / "eh3d.project.json").read_text(encoding="utf-8"))
    manifest["native_version"] = {"file": "version.h", "pattern": {k: rf"#define {k.upper()} (\d+)" for k in ("major", "minor", "patch", "build")}}
    (repo / "eh3d.project.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (repo / "version.h").write_text("#define MAJOR 0\n#define MINOR 8\n#define PATCH 0\n#define BUILD 1\n", encoding="utf-8")
    return repo


class ComponentPatternTests(unittest.TestCase):
    def test_a_pattern_given_per_number_is_checked_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = vp.Repo(with_parts(Path(tmp)))
            self.assertEqual([p for p in vp.check(repo) if "version.h" in p], [])
            (Path(tmp) / "EH3D-TOY" / "version.h").write_text("#define MAJOR 0\n#define MINOR 8\n#define PATCH 0\n#define BUILD 9\n", encoding="utf-8")
            problems = vp.check(vp.Repo(Path(tmp) / "EH3D-TOY"))
            self.assertTrue(any("native version build is 9" in p for p in problems), problems)

    def test_a_bump_writes_every_number_of_the_new_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = with_parts(Path(tmp))
            repo = vp.Repo(root)
            problems, changed = vp.apply(repo, "0.8.0.1", "0.8.1.0")
            self.assertEqual(problems, [])
            repo.commit()
            text = (root / "version.h").read_text(encoding="utf-8")
            self.assertIn("MINOR 8", text)
            self.assertIn("PATCH 1", text)
            self.assertIn("BUILD 0", text)


class RobustnessTests(unittest.TestCase):
    def test_a_manifest_that_is_not_an_object_is_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = toy.make_repo(Path(tmp))
            (root / "eh3d.project.json").write_text("[1]", encoding="utf-8")
            try:
                vp.scan(vp.Repo(root))
            except vp.VersionError:
                pass  # a clear error is fine; a TypeError or AttributeError is not

    def test_the_search_for_files_never_enters_build_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = toy.make_repo(Path(tmp), python=True)
            (root / "node_modules" / "deep").mkdir(parents=True)
            (root / "node_modules" / "deep" / "pyproject.toml").write_text("x", encoding="utf-8")
            self.assertEqual(vp.Repo(root).files("pyproject.toml"), ["pyproject.toml"])

    def test_a_commit_leaves_no_temporary_file_and_replaces_the_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = toy.make_repo(Path(tmp))
            repo = vp.Repo(root)
            repo.write("eh3d.project.json", '{"version": "9"}\n')
            repo.commit()
            self.assertEqual((root / "eh3d.project.json").read_text(encoding="utf-8"), '{"version": "9"}\n')
            self.assertEqual([p.name for p in root.rglob("*.bump-tmp")], [])


if __name__ == "__main__":
    unittest.main()
