# =============================================================================
# EH3D-DOCS - tools/test_docs_contracts.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The documents of the hub as data: the constants of the suite, the map, the capability matrix, the version and the eight READMEs agree with each other."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_FILES = ("README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md")
CELL = re.compile(r"(?<!\\)\|")


def text(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def table(name: str) -> list[list[str]]:
    """The data rows of the first table of a document, as cells."""
    rows = [line for line in text(name).split("\n") if line.startswith("|")]
    return [[cell.strip() for cell in CELL.split(line.strip().strip("|"))] for line in rows[2:]]


def suite() -> dict:
    return json.loads(text("docs/suite.json"))


class SuiteConstantsTests(unittest.TestCase):
    def test_the_file_is_one_json_object_with_the_known_groups(self) -> None:
        self.assertEqual(set(suite()), {"schema", "about", "server", "manifest", "languages", "spindle_rpm", "version", "github_templates"})
        self.assertEqual(suite()["schema"], 1)

    def test_the_server_port_is_a_user_port(self) -> None:
        server = suite()["server"]
        self.assertEqual(server["repository"], "EH3D-SERVER")
        self.assertIsInstance(server["port"], int)
        self.assertTrue(1024 <= server["port"] <= 65535)

    def test_the_eight_languages_are_listed_once_with_their_readme(self) -> None:
        languages = suite()["languages"]
        self.assertEqual([language["code"] for language in languages].count("en"), 1)
        self.assertEqual({language["code"] for language in languages}, {"en", "es", "fr", "it", "de", "pt", "zh", "ja"})
        self.assertEqual({language["readme"] for language in languages}, set(LANGUAGE_FILES))
        for language in languages:
            with self.subTest(language=language["code"]):
                self.assertTrue((ROOT / language["readme"]).is_file())
                self.assertTrue(language["name"])

    def test_portuguese_is_the_european_one(self) -> None:
        portuguese = next(language for language in suite()["languages"] if language["code"] == "pt")
        self.assertEqual(portuguese["locale"], "pt-PT")

    def test_the_spindle_limits_are_in_order(self) -> None:
        spindle = suite()["spindle_rpm"]
        self.assertEqual(spindle["field_min"], 0)
        self.assertLess(0, spindle["vfd_max"])
        self.assertLessEqual(spindle["vfd_max"], spindle["original_max"])
        self.assertLessEqual(spindle["original_max"], spindle["field_max"])
        self.assertLessEqual(spindle["field_max"], 65535)

    def test_the_manifest_rule_names_this_ecosystem_and_the_known_schemas(self) -> None:
        manifest = suite()["manifest"]
        self.assertEqual(manifest["file"], "eh3d.project.json")
        self.assertEqual(manifest["ecosystem"], "EH3D")
        self.assertEqual(manifest["schema_versions"], ["1.0", "1.1"])

    def test_the_version_rule_accepts_this_repository_and_refuses_odd_numbers(self) -> None:
        rule = suite()["version"]
        pattern = re.compile(rule["pattern"])
        self.assertTrue(pattern.match(text("VERSION").strip()))
        for good in ("0.1.0", "0.8.0.9", "10.20.30"):
            self.assertTrue(pattern.match(good), good)
        for bad in ("1.0", "v1.2.3", "1.2.3-beta", "1.2.3.4.5", "a.b.c"):
            self.assertFalse(pattern.match(bad), bad)
        self.assertEqual(rule["components"], [3, 4])
        self.assertEqual(rule["digit_max"], 9)

    def test_every_template_the_contract_asks_for_exists_here(self) -> None:
        for name in suite()["github_templates"]:
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())


class VersionTests(unittest.TestCase):
    def test_the_version_file_the_manifest_and_the_changelog_say_the_same(self) -> None:
        version = text("VERSION").strip()
        manifest = json.loads(text("eh3d.project.json"))
        self.assertEqual(manifest["version"], version)
        first = re.search(r"(?m)^## \[(\d[\d.]*)\]", text("CHANGELOG.md"))
        self.assertIsNotNone(first)
        self.assertEqual(first.group(1), version)

    def test_the_changelog_keeps_an_unreleased_section_above_the_releases(self) -> None:
        changelog = text("CHANGELOG.md")
        self.assertLess(changelog.index("## [Unreleased]"), changelog.index("## [" + text("VERSION").strip() + "]"))

    def test_the_versions_of_the_changelog_go_down_without_repeats(self) -> None:
        found = [tuple(int(part) for part in v.split(".")) for v in re.findall(r"(?m)^## \[(\d[\d.]*)\]", text("CHANGELOG.md"))]
        self.assertEqual(found, sorted(set(found), reverse=True))

    def test_the_manifest_is_valid_for_the_rule_of_the_suite(self) -> None:
        manifest = json.loads(text("eh3d.project.json"))
        self.assertEqual(manifest["ecosystem"], suite()["manifest"]["ecosystem"])
        self.assertIn(manifest["schema_version"], suite()["manifest"]["schema_versions"])
        self.assertEqual(manifest["name"], ROOT.name if ROOT.name.startswith("EH3D-") else "EH3D-DOCS")
        self.assertIn(manifest["evidence"], ("none", "host-test", "simulator", "bench", "field"))
        self.assertIs(manifest["hardware_bound"], False)

    def test_the_readme_badge_of_every_language_carries_the_version(self) -> None:
        version = text("VERSION").strip()
        for name in LANGUAGE_FILES:
            with self.subTest(name=name):
                self.assertRegex(text(name), r"badge/[A-Za-z%0-9_]*-" + re.escape(version) + r"-")


class SuiteMapTests(unittest.TestCase):
    def rows(self) -> list[list[str]]:
        return table("docs/SUITE_MAP.md")

    def test_every_row_has_five_cells(self) -> None:
        for row in self.rows():
            with self.subTest(row=row[0]):
                self.assertEqual(len(row), 5)
                self.assertTrue(all(row))

    def test_a_repository_is_listed_once(self) -> None:
        names = [re.sub(r"[\[\]]|\(.*\)", "", row[0]) for row in self.rows()]
        self.assertEqual(len(names), len(set(names)))

    def test_a_link_points_to_the_repository_it_names(self) -> None:
        for row in self.rows():
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)$", row[0])
            if match:
                with self.subTest(name=match.group(1)):
                    self.assertEqual(match.group(2), f"https://github.com/JuanenRac/{match.group(1)}")

    def test_the_state_is_published_or_planned_and_a_release_is_a_version(self) -> None:
        for row in self.rows():
            name, _kind, state, release, _what = row
            with self.subTest(name=name):
                self.assertIn(state, ("Published", "Planned"))
                self.assertRegex(release, r"^(-|\d+\.\d+\.\d+(\.\d+)?)$")

    def test_a_repository_with_no_release_is_not_published(self) -> None:
        for row in self.rows():
            if row[3] == "-":
                with self.subTest(name=row[0]):
                    self.assertEqual(row[2], "Planned")

    def test_a_published_repository_has_a_link_and_a_release(self) -> None:
        for row in self.rows():
            if row[2] == "Published":
                with self.subTest(name=row[0]):
                    self.assertTrue(row[0].startswith("[") and "](https://github.com/" in row[0])
                    self.assertNotEqual(row[3], "-")

    def test_this_hub_is_in_the_map_at_its_own_version(self) -> None:
        row = next(r for r in self.rows() if r[0].startswith("[EH3D-DOCS]"))
        self.assertEqual(row[3], text("VERSION").strip())

    def test_the_two_counts_the_readme_gives_match_the_map(self) -> None:
        rows = self.rows()
        published = sum(1 for r in rows if r[2] == "Published")
        planned = sum(1 for r in rows if r[2] == "Planned")
        self.assertEqual(published + planned, len(rows))
        self.assertGreaterEqual(published, 30)
        self.assertGreaterEqual(planned, 1)

    def test_the_kinds_are_few_and_named(self) -> None:
        kinds = {row[1] for row in self.rows()}
        self.assertLessEqual(len(kinds), 20)
        self.assertIn("Documentation", kinds)
        self.assertIn("Service", kinds)


class CapabilityMatrixTests(unittest.TestCase):
    def rows(self) -> list[list[str]]:
        return table("docs/CAPABILITY_MATRIX.md")

    def test_every_row_has_five_cells_and_only_a_planned_one_has_no_repository(self) -> None:
        for row in self.rows():
            with self.subTest(row=row[0][:50]):
                self.assertEqual(len(row), 5)
                self.assertTrue(row[0] and row[2] and row[3] and row[4])
                if not row[1]:
                    self.assertEqual((row[2], row[3]), ("No", "No"))
                    self.assertIn("Planned", row[4])

    def test_tested_and_run_say_yes_partly_or_no_and_nothing_else(self) -> None:
        for row in self.rows():
            with self.subTest(row=row[0][:50]):
                self.assertIn(row[2], ("Yes", "Partly", "No"))
                self.assertIn(row[3], ("Yes", "Partly", "No"))

    def test_nothing_is_run_on_a_machine_without_being_tested(self) -> None:
        for row in self.rows():
            if row[3] != "No":
                with self.subTest(row=row[0][:50]):
                    self.assertNotEqual(row[2], "No")

    def test_a_capability_that_ran_on_a_machine_says_what_was_not_run(self) -> None:
        for row in self.rows():
            if row[3] in ("Yes", "Partly"):
                with self.subTest(row=row[0][:50]):
                    self.assertGreater(len(row[4]), 20)

    def test_every_repository_of_the_matrix_is_in_the_map(self) -> None:
        in_map = {re.sub(r"[\[\]]|\(.*\)", "", row[0]) for row in table("docs/SUITE_MAP.md")}
        for row in self.rows():
            named = re.findall(r"(?:EH3D|ELECTRO-HOBBY-3D)-[A-Z0-9-]+", row[1])
            with self.subTest(repository=row[1][:40]):
                if not row[1]:
                    continue
                self.assertTrue(named)
                self.assertLessEqual(set(named), in_map)

    def test_the_matrix_says_in_its_own_words_what_tested_and_run_mean(self) -> None:
        intro = text("docs/CAPABILITY_MATRIX.md").split("| Capability")[0]
        self.assertIn('"Tested"', intro)
        self.assertIn('"Run on a machine"', intro)

    def test_no_capability_is_listed_twice(self) -> None:
        names = [(row[0], row[1]) for row in self.rows()]
        self.assertEqual(len(names), len(set(names)))


class ReadmeParityTests(unittest.TestCase):
    def test_the_eight_files_state_the_same_number_of_tests_in_each_place(self) -> None:
        found = {name: re.findall(r"(?m)^\| [^|]+ \| (\d+) \|$", text(name)) for name in LANGUAGE_FILES}
        self.assertEqual(len({tuple(v) for v in found.values()}), 1, found)
        self.assertTrue(all(found.values()))

    def test_the_count_of_the_readmes_is_the_count_of_the_tests_of_the_tools(self) -> None:
        counted = sum(len(re.findall(r"(?m)^    def test_", path.read_text(encoding="utf-8"))) for path in (ROOT / "tools").glob("test_*.py"))
        stated = {int(n) for n in re.findall(r"(?m)^\| [^|]+ \| (\d+) \|$", text("README.md"))}
        self.assertEqual(stated, {counted}, "update the number of tests in the eight READMEs (the row of At a glance, the row of Project status and the Tests section)")

    def test_the_test_count_is_written_three_times_in_each_language(self) -> None:
        number = re.search(r"(?m)^\| [^|]+ \| (\d+) \|$", text("README.md")).group(1)
        for name in LANGUAGE_FILES:
            with self.subTest(name=name):
                self.assertEqual(len(re.findall(rf"(?<![\d.]){number}(?![\d.])", text(name))), 3)

    def test_the_eight_files_have_the_same_headings_in_the_same_number(self) -> None:
        counts = {name: len(re.findall(r"(?m)^## ", text(name))) for name in LANGUAGE_FILES}
        self.assertEqual(len(set(counts.values())), 1, counts)

    def test_the_eight_files_link_the_same_documents(self) -> None:
        def docs(name: str) -> set[str]:
            return set(re.findall(r"\]\((docs/[A-Za-z_./-]+?\.md)\)", text(name)))
        english = docs("README.md")
        self.assertTrue(english)
        for name in LANGUAGE_FILES[1:]:
            with self.subTest(name=name):
                self.assertEqual(docs(name), english)

    def test_every_document_the_readmes_link_exists(self) -> None:
        for name in LANGUAGE_FILES:
            for target in re.findall(r"\]\((docs/[A-Za-z_./-]+?\.md)\)", text(name)):
                with self.subTest(name=name, target=target):
                    self.assertTrue((ROOT / target).is_file())

    def test_no_readme_keeps_the_marks_of_unfinished_text(self) -> None:
        for name in LANGUAGE_FILES:
            with self.subTest(name=name):
                body = text(name)
                for mark in ("TODO", "FIXME", "XXX", "lorem ipsum"):
                    self.assertNotIn(mark, body)


class VendoredLockTests(unittest.TestCase):
    def lock(self) -> dict:
        return json.loads(text("docs/vendored.lock"))

    def test_the_lock_names_this_hub_as_the_origin(self) -> None:
        self.assertEqual(self.lock()["origin"], "EH3D-DOCS")

    def test_every_tool_of_the_lock_exists_and_has_a_short_hash(self) -> None:
        for name, digest in self.lock()["tools"].items():
            with self.subTest(name=name):
                self.assertTrue((ROOT / "tools" / name).is_file())
                self.assertRegex(digest, r"^[0-9a-f]{10}$")

    def test_the_tools_are_listed_in_order_and_once(self) -> None:
        names = list(self.lock()["tools"])
        self.assertEqual(names, sorted(names))

    def test_a_test_is_never_a_vendored_tool(self) -> None:
        for name in self.lock()["tools"]:
            with self.subTest(name=name):
                self.assertFalse(name.startswith("test_"))


if __name__ == "__main__":
    unittest.main()
