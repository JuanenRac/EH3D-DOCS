# =============================================================================
# @@name@@ - tools/test_repository.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The base of the repository: the version is the same everywhere it is written, and the eight README files exist."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_FILES = ("README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md")


class BaseTests(unittest.TestCase):
    def test_the_version_is_the_same_in_the_manifest_the_version_file_and_the_changelog(self) -> None:
        manifest = json.loads((ROOT / "eh3d.project.json").read_text(encoding="utf-8"))
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), manifest["version"])
        newest = re.search(r"(?m)^## \[(\d[^\]]*)\]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(newest)
        self.assertEqual(newest.group(1), manifest["version"])

    def test_the_manifest_names_the_folder_of_the_repository(self) -> None:
        manifest = json.loads((ROOT / "eh3d.project.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], ROOT.name)

    def test_the_eight_readme_files_exist_and_show_the_version(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        for name in README_FILES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn(f"`{version}`", text, name)


if __name__ == "__main__":
    unittest.main()
