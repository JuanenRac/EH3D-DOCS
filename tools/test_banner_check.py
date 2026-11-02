# =============================================================================
# EH3D-DOCS - tools/test_banner_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check of the text of the banners against the manifest (tools/banner_check.py)."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_banner_check", TOOLS / "banner_check.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)

MANIFEST = {"name": "EH3D-TEST", "role": "tool", "technologies": ["Rust", "Gerber & Drill"]}


def banner(tag="EH3D · TOOL", title="EH3D-TEST", line="RUST · GERBER &amp; DRILL", pills=("RUST", "GERBER &amp; DRILL"), badge="TOOL", slogan="A SLOGAN"):
    rows = [f'<text x="12" y="-2" font-size="11" letter-spacing="2.5">{tag}</text>',
            f'<text x="0" y="142" font-size="56" letter-spacing="5">{title}</text>',
            f'<text x="0" y="182" font-size="22" letter-spacing="4">{slogan}</text>',
            f'<text x="0" y="212" font-size="12" letter-spacing="1.5">{line}</text>']
    rows += [f'<text x="22" y="15" font-size="10" letter-spacing="0.5">{p}</text>' for p in pills]
    rows.append(f'<text x="14" y="2" font-size="11" letter-spacing="1">{badge}</text>')
    return "<svg>" + "".join(rows) + "</svg>"


class BannerTests(unittest.TestCase):
    def test_a_banner_that_matches_the_manifest_passes(self):
        self.assertEqual(CHECK.problems_of(banner(), MANIFEST, "b.svg"), [])

    def test_the_name_of_another_repository_is_found(self):
        found = CHECK.problems_of(banner(title="EH3D-OTHER"), MANIFEST, "b.svg")
        self.assertEqual(len(found), 1)
        self.assertIn("EH3D-TEST", found[0])

    def test_the_role_in_the_tag_and_in_the_badge_is_found(self):
        found = CHECK.problems_of(banner(tag="EH3D · SERVER", badge="SERVER"), MANIFEST, "b.svg")
        self.assertEqual(len(found), 2)

    def test_the_technologies_and_the_pills_are_found(self):
        found = CHECK.problems_of(banner(line="RUST", pills=("RUST",)), MANIFEST, "b.svg")
        self.assertEqual(len(found), 2)

    def test_a_banner_without_tagline_is_found(self):
        found = CHECK.problems_of(banner(slogan=""), MANIFEST, "b.svg")
        self.assertTrue(any("tagline" in line for line in found))

    def test_only_the_first_four_technologies_become_pills(self):
        manifest = dict(MANIFEST, technologies=["A", "B", "C", "D", "E"])
        found = CHECK.problems_of(banner(line="A · B · C · D · E", pills=("A", "B", "C", "D")), manifest, "b.svg")
        self.assertEqual(found, [])

    def test_the_plain_banner_of_a_new_repository_is_checked_for_its_name_only(self):
        plain = '<svg><text font-size="60">EH3D-TEST</text><text font-size="24">EH3D FABRICATION SUITE</text></svg>'
        self.assertEqual(CHECK.problems_of(plain, MANIFEST, "b.svg"), [])
        self.assertEqual(len(CHECK.problems_of(plain.replace("EH3D-TEST", "EH3D-OTHER"), MANIFEST, "b.svg")), 1)

    def test_a_repository_without_banner_has_nothing_to_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "eh3d.project.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
            self.assertEqual(CHECK.problems(root), [])

    def test_the_files_of_the_images_folder_are_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "images").mkdir()
            (root / "eh3d.project.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
            (root / "images" / "EH3D_BANNER.svg").write_text(banner(title="EH3D-OLD"), encoding="utf-8")
            self.assertEqual(len(CHECK.run_in_ci(root)), 1)

    def test_a_wrong_option_ends_with_64_and_help_with_0(self):
        self.assertEqual(CHECK.main(["--nope"]), 64)
        self.assertEqual(CHECK.main(["--help"]), 0)


if __name__ == "__main__":
    unittest.main()
