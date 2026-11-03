# =============================================================================
# EH3D-DOCS - tools/test_shared_round2.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""README badge and Version row against the manifest, the manifest of the updater of the family, banners with <tspan>, and the bump tool on large trees."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"eh3d_{name}", TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATE = load("ci_validate")
BANNER = load("banner_check")


class ReadmeVersionPlaces(unittest.TestCase):
    def test_the_badge_and_the_row_are_read(self):
        text = "![v](https://img.shields.io/badge/Version-0.1.2-blue)\n\n| Version | `0.1.2` |\n| Tests | `358` |\n"
        self.assertEqual(VALIDATE.readme_version_places(text), ["0.1.2", "0.1.2"])

    def test_a_stale_badge_is_found_even_when_the_version_is_quoted_elsewhere(self):
        text = "![v](https://img.shields.io/badge/Version-0.1.1-blue)\n\nSee `0.1.2` in the changelog.\n"
        self.assertEqual(VALIDATE.readme_version_places(text), ["0.1.1"])


class UpdaterManifest(unittest.TestCase):
    def test_the_manifest_of_the_updater_of_the_family_is_known(self):
        self.assertIn("electro-hobby-3d.project.json", VALIDATE.MANIFEST_NAMES)

    def test_the_banner_check_reads_that_manifest(self):
        svg = '<svg><text font-size="22">ELECTRO-HOBBY-3D-UPDATER</text></svg>'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "images").mkdir()
            (root / "images" / "Project_BANNER.svg").write_text(svg, encoding="utf-8")
            (root / "electro-hobby-3d.project.json").write_text(json.dumps({"name": "OTHER-NAME", "role": "tool", "technologies": []}), encoding="utf-8")
            self.assertTrue(BANNER.problems(root), "the banner must be compared with the manifest of the updater")


class BannerText(unittest.TestCase):
    def test_a_tspan_inside_a_text_is_part_of_its_content(self):
        svg = '<svg><text x="1" font-size="22">Hello <tspan font-weight="bold">world</tspan></text></svg>'
        self.assertEqual(BANNER.texts(svg), [({"x": "1", "font-size": "22"}, "Hello world")])

    def test_a_banner_file_is_found_whatever_its_case(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "images").mkdir()
            (root / "images" / "x_Banner.SVG").write_text("<svg/>", encoding="utf-8")
            (root / "images" / "other.svg").write_text("<svg/>", encoding="utf-8")
            self.assertEqual([p.name for p in BANNER.banner_files(root)], ["x_Banner.SVG"])


if __name__ == "__main__":
    unittest.main()
