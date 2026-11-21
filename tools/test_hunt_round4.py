# =============================================================================
# EH3D-DOCS - tools/test_hunt_round4.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Edge cases of the version odometer, the changelog tools and the link check: damaged text, other scripts' digits, long walks and round trips."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import changelog_tools as ct
import check_links as cl
import version_places as vp

CHANGELOG = "# C\n\n## [Unreleased]\n\n- a\n- b\n\n## [0.1.0] - x\n\n- c\n"


class VersionParseTests(unittest.TestCase):
    def test_a_trailing_newline_is_not_part_of_a_version(self):
        with self.assertRaises(vp.VersionError):
            vp.parse("0.1.2\n")

    def test_digits_of_other_scripts_are_not_versions(self):
        with self.assertRaises(vp.VersionError):
            vp.parse("٠.١.٢")

    def test_fullwidth_digits_are_not_versions(self):
        with self.assertRaises(vp.VersionError):
            vp.parse("０.１.２")

    def test_five_numbers_two_numbers_and_empty_are_refused(self):
        for text in ("1.2.3.4.5", "1.2", "", "1", "..", "1..2"):
            with self.subTest(text=text):
                with self.assertRaises(vp.VersionError):
                    vp.parse(text)

    def test_spaces_signs_and_a_leading_v_are_refused(self):
        for text in (" 1.2.3", "1.2.3 ", "v1.2.3", "-1.2.3", "+1.2.3", "1.2.3-rc1", "1.2.x"):
            with self.subTest(text=text):
                with self.assertRaises(vp.VersionError):
                    vp.parse(text)

    def test_three_and_four_numbers_are_read(self):
        self.assertEqual(vp.parse("0.0.0"), (0, 0, 0))
        self.assertEqual(vp.parse("1.2.3.4"), (1, 2, 3, 4))

    def test_check_digits_refuses_a_number_with_two_digits(self):
        with self.assertRaises(vp.VersionError):
            vp.check_digits("0.0.10")
        vp.check_digits("9.9.9.9")


class OdometerTests(unittest.TestCase):
    def test_the_documented_steps(self):
        steps = {"0.0.9": "0.1.0", "0.7.9": "0.8.0.0", "0.9.9.9": "1.0.0.0", "0.8.0.0": "0.8.0.1", "0.8.9.9": "0.9.0.0", "0.0.0": "0.0.1"}
        for old, new in steps.items():
            with self.subTest(old=old):
                self.assertEqual(vp.next_version(old), new)

    def test_the_odometer_is_full_at_nine_nine_nine(self):
        with self.assertRaises(vp.VersionError):
            vp.next_version("9.9.9")

    def test_a_number_with_two_digits_cannot_be_raised(self):
        with self.assertRaises(vp.VersionError):
            vp.next_version("0.0.10")

    def test_a_long_walk_goes_up_by_one_and_never_writes_two_digits(self):
        version = "0.0.0"
        for _ in range(2500):
            following = vp.next_version(version)
            self.assertEqual(vp.compare(following, version), 1, f"{version} -> {following}")
            self.assertTrue(all(n <= 9 for n in vp.parse(following)), following)
            version = following

    def test_every_step_survives_a_round_trip_through_parse(self):
        version = "0.7.0"
        for _ in range(300):
            version = vp.next_version(version)
            self.assertEqual(".".join(str(n) for n in vp.parse(version)), version)

    def test_three_numbers_become_four_exactly_at_zero_eight(self):
        self.assertEqual(len(vp.parse(vp.next_version("0.7.8"))), 3)
        self.assertEqual(len(vp.parse(vp.next_version("0.7.9"))), 4)

    def test_the_odometer_is_not_recomputed_from_a_string_with_a_newline(self):
        with self.assertRaises(vp.VersionError):
            vp.next_version("0.0.1\n")


class CompareTests(unittest.TestCase):
    def test_zeros_fill_on_the_right(self):
        self.assertEqual(vp.compare("0.1.0", "0.1.0.0"), 0)
        self.assertEqual(vp.compare("0.1.0.1", "0.1.0"), 1)
        self.assertEqual(vp.compare("0.1.0", "0.1.0.1"), -1)

    def test_compare_is_a_numeric_not_a_text_order(self):
        self.assertEqual(vp.compare("0.0.9", "0.0.10"), -1)
        self.assertEqual(vp.compare("0.10.0", "0.9.0"), 1)

    def test_compare_is_antisymmetric_and_transitive_on_a_sample(self):
        sample = ["0.0.1", "0.1.0", "0.1.0.0", "0.1.0.1", "0.8.0.0", "1.0.0", "1.0.0.1", "0.0.0"]
        for a in sample:
            for b in sample:
                self.assertEqual(vp.compare(a, b), -vp.compare(b, a), (a, b))
                for c in sample:
                    if vp.compare(a, b) <= 0 and vp.compare(b, c) <= 0:
                        self.assertLessEqual(vp.compare(a, c), 0, (a, b, c))

    def test_compare_with_a_damaged_version_raises_instead_of_guessing(self):
        with self.assertRaises(vp.VersionError):
            vp.compare("0.1.0", "0.1.٠")


class ChangelogTests(unittest.TestCase):
    def test_promote_moves_the_entries_and_leaves_unreleased_empty(self):
        out = ct.promote(CHANGELOG, "0.1.1", "T")
        self.assertEqual(ct.unreleased_body(out), "")
        section = ct.find(out, "0.1.1")
        self.assertIsNotNone(section)
        self.assertEqual(ct.body(out, section), "- a\n- b")
        self.assertEqual(section.title, "T")

    def test_promote_keeps_the_older_sections_unchanged(self):
        out = ct.promote(CHANGELOG, "0.1.1", "T")
        self.assertTrue(out.endswith("## [0.1.0] - x\n\n- c\n"))

    def test_promote_without_a_trailing_newline_still_ends_a_heading_with_one(self):
        out = ct.promote("## [Unreleased]\n- a", "0.1.1", "T")
        self.assertIn("## [0.1.1] - T\n\n- a\n", out)

    def test_promote_twice_is_refused_because_nothing_is_left(self):
        once = ct.promote(CHANGELOG, "0.1.1", "T")
        with self.assertRaises(ct.ChangelogError):
            ct.promote(once, "0.1.2", "T")

    def test_promote_an_existing_version_is_refused(self):
        with self.assertRaises(ct.ChangelogError):
            ct.promote(CHANGELOG, "0.1.0", "T")

    def test_promote_without_the_unreleased_heading_is_refused(self):
        with self.assertRaises(ct.ChangelogError):
            ct.promote("# C\n\n## [0.1.0] - x\n\n- c\n", "0.1.1", "T")

    def test_promote_refuses_a_title_of_several_lines_or_blank(self):
        for title in ("a\nb", "", "   ", "\n"):
            with self.subTest(title=title):
                with self.assertRaises(ct.ChangelogError):
                    ct.promote(CHANGELOG, "0.1.1", title)

    def test_the_title_is_stripped_and_a_dash_in_it_survives(self):
        out = ct.promote(CHANGELOG, "0.1.1", "  Fast - and safe  ")
        self.assertEqual(ct.find(out, "0.1.1").title, "Fast - and safe")

    def test_counting_the_entries_ignores_nested_lines_and_a_missing_space(self):
        self.assertEqual(ct.count_entries("- a\n  - nested\n* b\n-c\n"), 2)
        self.assertEqual(ct.count_entries(""), 0)

    def test_the_newest_release_skips_unreleased(self):
        self.assertEqual(ct.newest_release(CHANGELOG).version, "0.1.0")
        self.assertIsNone(ct.newest_release("## [Unreleased]\n"))

    def test_unreleased_is_found_whatever_its_case(self):
        self.assertEqual(ct.unreleased_body("## [UNRELEASED]\n\n- a\n"), "- a")
        self.assertIsNone(ct.unreleased_body("# nothing here\n"))

    def test_an_empty_text_has_no_sections(self):
        self.assertEqual(ct.sections(""), [])
        self.assertIsNone(ct.find("", "0.1.0"))

    def test_a_heading_at_the_very_end_has_an_empty_body(self):
        section = ct.sections("## [Unreleased]")[0]
        self.assertEqual(ct.body("## [Unreleased]", section), "")

    def test_the_bodies_of_all_sections_cover_the_text_without_overlap(self):
        found = ct.sections(CHANGELOG)
        for left, right in zip(found, found[1:], strict=False):
            self.assertEqual(left.end, right.heading_start)
            self.assertLessEqual(left.body_start, left.end)

    def test_a_version_with_unicode_text_in_the_title_is_kept(self):
        out = ct.promote(CHANGELOG, "0.1.1", "バージョン 中文 éà")
        self.assertEqual(ct.find(out, "0.1.1").title, "バージョン 中文 éà")


class LinkTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        (self.root / "docs").mkdir()
        (self.root / "docs" / "Guide.md").write_text("x", encoding="utf-8")
        (self.root / "docs" / "with space.md").write_text("x", encoding="utf-8")
        (self.root / "README.md").write_text("x", encoding="utf-8")
        self._old = cl.ROOT
        cl.ROOT = self.root

    def tearDown(self):
        cl.ROOT = self._old
        self._tmp.cleanup()

    def test_the_case_must_match_exactly(self):
        self.assertTrue(cl.exists_exactly(self.root / "docs", "Guide.md"))
        self.assertFalse(cl.exists_exactly(self.root / "docs", "guide.md"))

    def test_a_folder_in_the_wrong_case_is_missing(self):
        self.assertFalse(cl.exists_exactly(self.root, "Docs/Guide.md"))

    def test_an_anchor_or_a_query_does_not_count_and_an_empty_target_is_fine(self):
        self.assertTrue(cl.exists_exactly(self.root / "docs", "Guide.md#top"))
        self.assertTrue(cl.exists_exactly(self.root / "docs", "Guide.md?x=1"))
        self.assertTrue(cl.exists_exactly(self.root / "docs", "#only-an-anchor"))

    def test_percent_encoding_is_decoded(self):
        self.assertTrue(cl.exists_exactly(self.root / "docs", "with%20space.md"))

    def test_parent_folders_and_dot_segments_resolve(self):
        self.assertTrue(cl.exists_exactly(self.root / "docs", "../README.md"))
        self.assertTrue(cl.exists_exactly(self.root / "docs", "./Guide.md"))
        self.assertFalse(cl.exists_exactly(self.root / "docs", "../Readme.md"))

    def test_an_absolute_link_is_read_from_the_root_of_the_repository(self):
        self.assertTrue(cl.exists_exactly(self.root / "docs", "/README.md"))
        self.assertFalse(cl.exists_exactly(self.root / "docs", "/docs/missing.md"))

    def test_a_backslash_is_taken_as_a_separator(self):
        self.assertTrue(cl.exists_exactly(self.root, "docs\\Guide.md"))

    def test_a_missing_file_inside_a_missing_folder_is_missing(self):
        self.assertFalse(cl.exists_exactly(self.root, "nope/deeper/file.md"))

    def test_a_link_in_a_code_span_is_not_a_target_and_an_image_is(self):
        self.assertEqual(cl.targets_in("see [a](x.md) and `[b](y.md)` and ![i](p.png)"), ["x.md", "p.png"])

    def test_a_reference_definition_is_a_target(self):
        self.assertEqual(cl.targets_in("[ref]: ./a.md"), ["./a.md"])

    def test_a_line_without_links_has_no_targets(self):
        self.assertEqual(cl.targets_in(""), [])
        self.assertEqual(cl.targets_in("plain text with [brackets] and (parentheses)"), [])


if __name__ == "__main__":
    unittest.main()
