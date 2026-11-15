# =============================================================================
# EH3D-DOCS - tools/test_universal_readme_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/universal_readme_check.py: the reading of a README, the parity of the eight files of this repository and the verdict line."""
from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

import universal_readme_check as urc

ROOT = Path(__file__).resolve().parents[1]


def verdict(problems: list[str], **kwargs) -> tuple[int, str]:
    out = io.StringIO()
    code = urc.report(problems, stream=out, **kwargs)
    return code, out.getvalue()


class ReadmeParsingTests(unittest.TestCase):
    TEXT = (
        "# Title\n\nintro\n\n## \U0001F4CB At a glance\n\n| a | b |\n\n### Sub one\n\n```\n## \U0001F6A6 not a heading\n```\n\n"
        "## \U0001F6A6️ Project status\n\n### Sub two\n### Sub three\n\n## ❓ Free text\n"
    )

    def test_sections_split_at_level_two_headings_and_keep_the_header(self) -> None:
        readme = urc.Readme(self.TEXT)
        self.assertEqual([s["title"] for s in readme.sections], ["At a glance", "Project status", "Free text"])
        self.assertEqual(readme.header[0], "# Title")

    def test_the_icon_picks_the_section_and_the_variation_selector_is_ignored(self) -> None:
        readme = urc.Readme(self.TEXT)
        self.assertEqual([s["id"] for s in readme.sections], ["glance", "status", None])
        self.assertIs(readme.section("status"), readme.sections[1])
        self.assertIsNone(readme.section("license"))

    def test_a_heading_inside_a_code_block_is_not_a_section(self) -> None:
        readme = urc.Readme(self.TEXT)
        self.assertEqual(len(readme.sections), 3)
        self.assertNotIn("not a heading", [s["title"] for s in readme.sections])

    def test_sub_sections_are_counted_for_each_section(self) -> None:
        readme = urc.Readme(self.TEXT)
        self.assertEqual([s["h3"] for s in readme.sections], [1, 2, 0])

    def test_windows_line_ends_read_the_same(self) -> None:
        self.assertEqual([s["id"] for s in urc.Readme(self.TEXT.replace("\n", "\r\n")).sections], ["glance", "status", None])

    def test_the_twenty_two_sections_have_one_icon_each_and_fourteen_are_required(self) -> None:
        self.assertEqual(len(urc.SECTIONS), 22)
        self.assertEqual(len({icon for _, icon in urc.SECTIONS}), 22)
        self.assertEqual(len(urc.REQUIRED), 14)
        self.assertEqual(urc.ORDER[0], "glance")
        self.assertEqual(urc.ORDER[-1], "license")

    def test_every_language_names_every_section(self) -> None:
        self.assertEqual(set(urc.NAMES), {language for language, _ in urc.LANGUAGE_FILES})
        for language, names in urc.NAMES.items():
            with self.subTest(language=language):
                self.assertEqual(set(names), set(urc.ORDER))


class TestCountTests(unittest.TestCase):
    def test_the_badge_and_the_glance_table_both_state_the_count(self) -> None:
        text = "# T\n![x](https://img.shields.io/badge/Tests-306-green)\n\n## \U0001F4CB At a glance\n\n| | |\n|---|---|\n| Tests | 306 |\n"
        self.assertEqual(urc.tests_in_readme(urc.Readme(text)), {306})

    def test_a_count_with_a_thousands_separator_is_read(self) -> None:
        text = "# T\n\n## \U0001F4CB At a glance\n\n| | |\n|---|---|\n| Tests | 1,234 |\n"
        self.assertEqual(urc.tests_in_readme(urc.Readme(text)), {1234})

    def test_the_translated_row_names_are_read(self) -> None:
        for name in ("Pruebas", "Testes", "テスト", "测试", "Test"):
            with self.subTest(name=name):
                text = f"# T\n\n## \U0001F4CB At a glance\n\n| | |\n|---|---|\n| {name} | 42 |\n"
                self.assertEqual(urc.tests_in_readme(urc.Readme(text)), {42})

    def test_two_different_counts_are_both_returned_so_the_check_can_object(self) -> None:
        text = "# T\n![x](https://img.shields.io/badge/Tests-10-green)\n\n## \U0001F4CB At a glance\n\n| | |\n|---|---|\n| Tests | 11 |\n"
        self.assertEqual(urc.tests_in_readme(urc.Readme(text)), {10, 11})

    def test_no_count_gives_an_empty_set(self) -> None:
        self.assertEqual(urc.tests_in_readme(urc.Readme("# T\n\n## Other\n")), set())


class RepositoryTests(unittest.TestCase):
    def test_this_repository_follows_the_layout_in_the_eight_languages(self) -> None:
        self.assertEqual(urc.check_repository(ROOT), [])

    def test_a_missing_translation_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text((ROOT / "README.md").read_text(encoding="utf-8"), encoding="utf-8")
            problems = urc.check_repository(root)
        self.assertIn("README_spa.md: missing", problems)
        self.assertIn("README_por.md: missing", problems)
        self.assertEqual(len([p for p in problems if p.endswith(": missing")]), 7)

    def test_an_empty_folder_has_eight_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            problems = urc.check_repository(Path(folder))
        self.assertEqual(len(problems), 8)

    def test_a_readme_without_the_layout_is_told_what_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for _, name in urc.LANGUAGE_FILES:
                (root / name).write_text("just words\n", encoding="utf-8")
            problems = urc.check_repository(root)
        self.assertTrue(any("no banner image" in p for p in problems))
        self.assertTrue(any("no title" in p for p in problems))
        self.assertTrue(any("language bar" in p for p in problems))

    def test_a_translation_with_a_section_less_is_told_apart_from_the_english(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for _, name in urc.LANGUAGE_FILES:
                (root / name).write_text((ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")
            broken = (ROOT / "README_spa.md").read_text(encoding="utf-8")
            starts = [m for m in range(len(broken)) if broken.startswith(chr(10) + "## ", m)]
            (root / "README_spa.md").write_text(broken[: starts[2]] + broken[starts[3] :], encoding="utf-8")
            problems = urc.check_repository(root)
        self.assertTrue(any(p.startswith("README_spa.md") for p in problems))
        self.assertFalse(any(p.startswith("README_por.md") for p in problems))

    def test_run_tests_gives_none_without_a_tests_folder(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(urc.run_tests(Path(folder)))


class VerdictTests(unittest.TestCase):
    def test_no_problem_passes(self) -> None:
        self.assertEqual(verdict([]), (0, "UNIVERSAL_README=PASS\n"))

    def test_a_problem_warns_and_only_a_strict_run_fails(self) -> None:
        code, out = verdict(["a: x"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("UNIVERSAL_README=WARN 1"))
        code, out = verdict(["a: x"], strict=True)
        self.assertEqual(code, 1)
        self.assertTrue(out.startswith("UNIVERSAL_README=FAIL 1"))

    def test_the_list_is_cut_at_the_limit_and_says_how_many_more(self) -> None:
        code, out = verdict([f"p{i}" for i in range(20)], limit=3)
        self.assertEqual(code, 0)
        self.assertIn("p2", out)
        self.assertNotIn("p3", out)
        self.assertIn("and 17 more", out)

    def test_a_console_that_cannot_show_the_icons_still_gets_the_line(self) -> None:
        class Ascii(io.StringIO):
            def write(self, text: str) -> int:
                text.encode("ascii")
                return super().write(text)

        out = Ascii()
        urc.report(["café problem"], stream=out)
        self.assertIn("problem", out.getvalue())

    def test_the_environment_can_force_strict_on_or_off(self) -> None:
        saved = os.environ.get("UNIVERSAL_README_STRICT")
        self.addCleanup(lambda: os.environ.pop("UNIVERSAL_README_STRICT", None) if saved is None else os.environ.__setitem__("UNIVERSAL_README_STRICT", saved))
        os.environ.pop("UNIVERSAL_README_STRICT", None)
        self.assertFalse(urc.strict_requested())
        self.assertTrue(urc.strict_requested(True))
        for value, expected in (("1", True), ("yes", True), ("0", False), ("false", False), ("no", False)):
            os.environ["UNIVERSAL_README_STRICT"] = value
            with self.subTest(value=value):
                self.assertEqual(urc.strict_requested(not expected), expected)

    def test_the_family_comes_from_the_name_of_the_folder(self) -> None:
        for name, family in (("EH3D-DOCS", "EH3D"), ("ELECTRO-HOBBY-3D-UPDATER", "EH3D"), ("armor-server", "ARMOR"), ("URTC-COMMON", "URTC"), ("HYDRA-UMC-SDK", "HYDRA"), ("other", "")):
            with self.subTest(name=name):
                self.assertEqual(urc.family_of(Path(name)), family)

    def test_every_family_is_strict_in_its_ci(self) -> None:
        self.assertEqual(set(urc.FAMILY_STRICT), {"ARMOR", "URTC", "HYDRA", "EH3D"})
        self.assertTrue(all(urc.FAMILY_STRICT.values()))

    def test_the_ci_gate_passes_on_this_repository_and_fails_on_a_broken_one(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(urc.run_in_ci(ROOT), [])
            with tempfile.TemporaryDirectory() as folder:
                root = Path(folder) / "EH3D-TOY"
                root.mkdir()
                found = urc.run_in_ci(root)
        self.assertEqual(len(found), 1)

    def test_a_fault_of_the_check_never_fails_the_ci(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(urc.run_in_ci(None), [])   # type: ignore[arg-type]
        self.assertIn("UNIVERSAL_README=ERROR", out.getvalue())

    def test_main_prints_the_verdict_for_a_repository(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = urc.main(["--repo", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertIn("UNIVERSAL_README=PASS", out.getvalue())

    def test_main_strict_fails_on_an_empty_folder(self) -> None:
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(urc.main(["--repo", folder, "--strict"]), 1)


class RuleTests(unittest.TestCase):
    def test_the_date_rule_sees_the_usual_shapes(self) -> None:
        for text in ("2026-11-13", "13.11.2026", "13/11/2026", "November 13, 2026", "13 Nov 2026"):
            with self.subTest(text=text):
                self.assertIsNotNone(urc.DATE.search(text))
        for text in ("version 0.1.0", "2019-01-01", "port 18200"):
            with self.subTest(text=text):
                self.assertIsNone(urc.DATE.search(text))

    def test_the_private_rule_sees_ids_of_the_form_xxx_yy_123(self) -> None:
        self.assertIsNotNone(urc.PRIVATE.search("see ABC-DEF-123 for it"))
        self.assertIsNone(urc.PRIVATE.search("the cipher AES-GCM-128 is fine"))


if __name__ == "__main__":
    unittest.main()
