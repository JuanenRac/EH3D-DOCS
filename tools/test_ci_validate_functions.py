# =============================================================================
# EH3D-DOCS - tools/test_ci_validate_functions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The small functions of tools/ci_validate.py one by one: what they read from a README, a manifest or a Cargo.toml and what they refuse."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import ci_validate as cv

LIGHTS = "\U0001F7E2 \U0001F7E1 \U0001F7E0 \U0001F534"


def status_section(rows: list[str], heading: str = "## \U0001F6A6 Project status") -> str:
    return f"## First\n\ntext\n\n{heading}\n\n{LIGHTS}\n\n| Area | State | Meaning |\n|---|---|---|\n" + "\n".join(rows) + "\n\n## Last\n"


class VersionPlacesTests(unittest.TestCase):
    def test_the_first_badge_and_the_first_row_are_read(self) -> None:
        text = "![v](https://img.shields.io/badge/Version-1.2.3-blue) ![w](https://img.shields.io/badge/Version-9.9.9-blue)\n| Version | `1.2.3` |\n| Other | `4.5.6` |\n"
        self.assertEqual(cv.readme_version_places(text), ["1.2.3", "1.2.3"])

    def test_a_four_component_version_is_read(self) -> None:
        self.assertEqual(cv.readme_version_places("| Version | `0.8.0.9` |\n"), ["0.8.0.9"])

    def test_a_row_with_other_text_in_the_cell_is_not_a_version_row(self) -> None:
        self.assertEqual(cv.readme_version_places("| Version | `1.2.3` and more |\n"), [])
        self.assertEqual(cv.readme_version_places("| Version | 1.2.3 |\n"), [])

    def test_a_text_without_versions_gives_nothing(self) -> None:
        self.assertEqual(cv.readme_version_places("# Title\n"), [])

    def test_the_header_version_is_read_from_the_comment_lines_only(self) -> None:
        self.assertEqual(cv.header_version("#!/usr/bin/env python3\n# canonical: EH3D-DOCS tools 6\nimport os\n"), "6")
        self.assertEqual(cv.header_version("# a\r\n# canonical: EH3D-DOCS tools 12\r\n"), "12")
        self.assertIsNone(cv.header_version("# nothing\nimport os\n# canonical: EH3D-DOCS tools 6\n"))
        self.assertIsNone(cv.header_version(""))

    def test_this_file_of_the_hub_carries_the_version_of_its_code(self) -> None:
        self.assertEqual(cv.header_problems(), [])

    def test_a_copy_with_another_version_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            copy = Path(folder) / "ci_validate.py"
            copy.write_text("# canonical: EH3D-DOCS tools 1\n", encoding="utf-8")
            found = cv.header_problems(copy)
        self.assertEqual(len(found), 1)
        self.assertIn("says canonical tools 1", found[0])


class HeadingTests(unittest.TestCase):
    def test_levels_are_listed_in_order(self) -> None:
        self.assertEqual(cv.headings("# A\n## B\n### C\n## D\n"), [1, 2, 3, 2])

    def test_a_heading_inside_a_code_block_is_not_one(self) -> None:
        self.assertEqual(cv.headings("# A\n```\n## not\n```\n## B\n"), [1, 2])

    def test_a_hash_without_a_space_is_not_a_heading(self) -> None:
        self.assertEqual(cv.headings("#tag\n# real\n"), [1])

    def test_seven_hashes_are_not_a_heading(self) -> None:
        self.assertEqual(cv.headings("####### too deep\n"), [])


class StatusLightTests(unittest.TestCase):
    def test_the_lights_of_the_table_are_returned_in_order(self) -> None:
        text = status_section(["| a | \U0001F7E1 | x |", "| b | \U0001F7E0 | y |", "| c | \U0001F7E2 | z |"])
        self.assertEqual(cv.status_lights(text), ["\U0001F7E1", "\U0001F7E0", "\U0001F7E2"])

    def test_the_section_has_to_be_the_second_heading_and_have_the_traffic_light_icon(self) -> None:
        text = status_section(["| a | \U0001F7E1 | x |"] * 3, heading="## Project status")
        self.assertIsNone(cv.status_lights(text))

    def test_fewer_than_three_rows_is_not_a_table(self) -> None:
        self.assertIsNone(cv.status_lights(status_section(["| a | \U0001F7E1 | x |", "| b | \U0001F7E1 | y |"])))

    def test_a_cell_that_is_not_a_light_makes_the_table_malformed(self) -> None:
        self.assertIsNone(cv.status_lights(status_section(["| a | ok | x |"] + ["| b | \U0001F7E1 | y |"] * 2)))

    def test_an_empty_meaning_makes_the_table_malformed(self) -> None:
        self.assertIsNone(cv.status_lights(status_section(["| a | \U0001F7E1 |  |"] + ["| b | \U0001F7E1 | y |"] * 2)))

    def test_the_legend_has_to_show_the_four_lights(self) -> None:
        text = status_section(["| a | \U0001F7E1 | x |"] * 3).replace(LIGHTS, "legend")
        self.assertIsNone(cv.status_lights(text))

    def test_a_text_with_one_heading_has_no_section(self) -> None:
        self.assertIsNone(cv.status_lights("## Only\n\n| a | b |\n"))

    def test_the_real_readme_has_a_table(self) -> None:
        lights = cv.status_lights((Path(cv.ROOT) / "README.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(lights)
        self.assertGreaterEqual(len(lights), 3)


class TreeTests(unittest.TestCase):
    TREE = "```text\nrepo/\n├── README.md\n├── docs/\n├── tools/\n├── src/, lib/\n└── .github/workflows/\n```\n"

    def test_the_first_level_names_are_collected(self) -> None:
        self.assertEqual(cv.tree_names(self.TREE), {"README.md", "docs", "tools", "src", "lib", ".github"})

    def test_the_block_with_the_most_rows_is_the_tree(self) -> None:
        text = "```\n├── only.txt\n```\n\n" + self.TREE
        self.assertIn("docs", cv.tree_names(text))
        self.assertNotIn("only.txt", cv.tree_names(text))

    def test_a_text_without_a_tree_gives_none(self) -> None:
        self.assertIsNone(cv.tree_names("# No tree\n\n```\ncode\n```\n"))

    def test_joined_names_are_split(self) -> None:
        self.assertEqual(cv.tree_names("```\n├── a.py + b.py\n└── c / d\n```\n"), {"a.py", "b.py", "c", "d"})

    def test_the_exempt_names_are_the_usual_files_and_hidden_ones(self) -> None:
        for name in ("README.md", "README_spa.md", "LICENSE", "CHANGELOG.md", "VERSION", "eh3d.project.json", "images", ".gitignore", "build.sh", "run.bat",
                     "test.sh", "dev.sh", "bump.py", "Cargo.lock", "Cargo.toml", "package.json", "package-lock.json", "pyproject.toml", "x.toml"):
            with self.subTest(name=name):
                self.assertRegex(name, cv.TREE_EXEMPT)
        for name in ("src", "docs", "tools", "main.py", "README_xx.md"):
            with self.subTest(name=name):
                self.assertNotRegex(name, cv.TREE_EXEMPT)


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "tools").mkdir()

    def write(self, text: str) -> None:
        (self.root / "tools" / "ci_config.json").write_text(text, encoding="utf-8")

    def test_no_file_means_no_config_and_no_problem(self) -> None:
        self.assertEqual(cv.load_config(self.root), ({}, []))

    def test_a_good_file_is_returned(self) -> None:
        self.write('{"skip_dirs": ["vendor"], "skip_checks": ["x"]}')
        config, problems = cv.load_config(self.root)
        self.assertEqual(problems, [])
        self.assertEqual(config["skip_dirs"], ["vendor"])

    def test_text_that_is_not_json_is_reported(self) -> None:
        self.write("{")
        config, problems = cv.load_config(self.root)
        self.assertEqual(config, {})
        self.assertIn("not valid JSON", problems[0])

    def test_an_array_is_not_a_config(self) -> None:
        self.write("[]")
        self.assertEqual(cv.load_config(self.root)[1], ["tools/ci_config.json must hold an object"])

    def test_a_list_of_names_must_hold_only_strings(self) -> None:
        for key in ("skip_dirs", "skip_checks"):
            for value in ('"text"', "[1]", '{"a": 1}'):
                with self.subTest(key=key, value=value):
                    self.write('{"%s": %s}' % (key, value))
                    self.assertIn(f"{key} must be a list of names", cv.load_config(self.root)[1][0])

    def test_the_folders_to_skip_add_to_the_default_ones(self) -> None:
        self.assertEqual(cv.skip_dirs({}), {"target", ".git"})
        self.assertEqual(cv.skip_dirs({"skip_dirs": ["vendor"]}), {"target", ".git", "vendor"})


class NativeVersionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def test_the_default_reads_the_version_of_a_pyproject(self) -> None:
        (self.root / "pyproject.toml").write_text('[project]\nversion = "1.2.3"\n', encoding="utf-8")
        self.assertEqual(cv.native_version(self.root, {}), ("1.2.3", "pyproject.toml"))

    def test_a_pattern_with_groups_joins_them_with_dots(self) -> None:
        (self.root / "VERSION").write_text("0.8.0.9\n", encoding="utf-8")
        self.assertEqual(cv.native_version(self.root, {"file": "VERSION", "pattern": r"^(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?"}), ("0.8.0.9", "VERSION"))
        self.assertEqual(cv.native_version(self.root, {"file": "VERSION", "pattern": r"^(\d+)\.(\d+)"}), ("0.8", "VERSION"))

    def test_a_pattern_given_per_component(self) -> None:
        (self.root / "v.h").write_text("#define MAJOR 1\n#define MINOR 2\n#define PATCH 3\n#define BUILD 4\n", encoding="utf-8")
        pattern = {"major": r"MAJOR (\d+)", "minor": r"MINOR (\d+)", "patch": r"PATCH (\d+)", "build": r"BUILD (\d+)"}
        self.assertEqual(cv.native_version(self.root, {"file": "v.h", "pattern": pattern})[0], "1.2.3.4")
        del pattern["build"]
        self.assertEqual(cv.native_version(self.root, {"file": "v.h", "pattern": pattern})[0], "1.2.3")
        del pattern["patch"]
        self.assertEqual(cv.native_version(self.root, {"file": "v.h", "pattern": pattern})[0], "?")

    def test_a_missing_file_a_pattern_that_does_not_match_and_a_bad_pattern_give_a_question_mark(self) -> None:
        self.assertEqual(cv.native_version(self.root, {"file": "none.txt"}), ("?", "none.txt"))
        (self.root / "a.txt").write_text("nothing here", encoding="utf-8")
        self.assertEqual(cv.native_version(self.root, {"file": "a.txt", "pattern": r"(\d+)"})[0], "?")
        self.assertEqual(cv.native_version(self.root, {"file": "a.txt", "pattern": "("})[0], "?")

    def test_the_hub_reads_its_own_version_file(self) -> None:
        manifest = json.loads((cv.ROOT / "eh3d.project.json").read_text(encoding="utf-8"))
        version, name = cv.native_version(cv.ROOT, manifest["native_version"])
        self.assertEqual(version, manifest["version"])
        self.assertEqual(name, "VERSION")


class ProjectYmlTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def test_a_repository_without_the_file_has_nothing_to_check(self) -> None:
        self.assertEqual(cv.project_yml_problems(self.root, "1.0.0"), [])

    def test_the_marketing_version_and_the_bundle_have_to_follow_the_manifest(self) -> None:
        (self.root / "project.yml").write_text('MARKETING_VERSION: "1.0.0"\nCFBundleShortVersionString: "$(MARKETING_VERSION)"\n', encoding="utf-8")
        self.assertEqual(cv.project_yml_problems(self.root, "1.0.0"), [])
        found = cv.project_yml_problems(self.root, "1.0.1")
        self.assertEqual(len(found), 1)
        self.assertIn("is not the version 1.0.1", found[0])

    def test_a_literal_bundle_version_and_a_missing_marketing_version_are_reported(self) -> None:
        (self.root / "project.yml").write_text('CFBundleShortVersionString: "1.0.0"\n', encoding="utf-8")
        found = cv.project_yml_problems(self.root, "1.0.0")
        self.assertEqual(len(found), 2)
        self.assertIn("MARKETING_VERSION (none)", found[0])


class DependsOnTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def cargo(self, text: str, where: str = ".") -> None:
        folder = self.root / where
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "Cargo.toml").write_text(text, encoding="utf-8")

    def test_no_dependency_and_none_declared_is_fine(self) -> None:
        self.cargo('[package]\nname = "x"\n')
        self.assertEqual(cv._depends_on_problems(self.root, {"name": "EH3D-X"}), [])

    def test_a_path_dependency_has_to_be_declared(self) -> None:
        self.cargo('[dependencies]\ncommon = { path = "../EH3D-COMMON/crates/a" }\n')
        found = cv._depends_on_problems(self.root, {"name": "EH3D-X", "schema_version": "1.1"})
        self.assertEqual(len(found), 1)
        self.assertIn("['EH3D-COMMON']", found[0])

    def test_a_declared_dependency_is_fine_with_schema_1_1(self) -> None:
        self.cargo('[dependencies]\ncommon = { path = "../../EH3D-COMMON/crates/a" }\n')
        self.assertEqual(cv._depends_on_problems(self.root, {"name": "EH3D-X", "schema_version": "1.1", "depends_on": ["EH3D-COMMON"]}), [])

    def test_a_declared_dependency_needs_schema_1_1(self) -> None:
        self.cargo('[dependencies]\ncommon = { path = "../EH3D-COMMON" }\n')
        found = cv._depends_on_problems(self.root, {"name": "EH3D-X", "schema_version": "1.0", "depends_on": ["EH3D-COMMON"]})
        self.assertEqual(found, ["depends_on needs schema_version 1.1"])

    def test_the_repository_itself_and_build_folders_are_not_dependencies(self) -> None:
        self.cargo('[dependencies]\nself = { path = "../EH3D-X" }\n')
        self.cargo('[dependencies]\nold = { path = "../EH3D-OLD" }\n', where="target/debug")
        self.cargo('[dependencies]\nold = { path = "../EH3D-OLD" }\n', where="node_modules/x")
        self.assertEqual(cv._depends_on_problems(self.root, {"name": "EH3D-X"}), [])

    def test_a_dependency_declared_but_not_used_is_reported(self) -> None:
        self.cargo('[package]\nname = "x"\n')
        found = cv._depends_on_problems(self.root, {"name": "EH3D-X", "schema_version": "1.1", "depends_on": ["EH3D-COMMON"]})
        self.assertEqual(len(found), 1)


class PrivacyRuleTests(unittest.TestCase):
    def test_the_forbidden_words_are_matched_as_whole_words_in_any_case(self) -> None:
        for text in ("by Claude", "ANTHROPIC", "a sonnet here"):
            with self.subTest(text=text):
                self.assertIsNotNone(cv.FORBIDDEN.search(text))
        for text in ("claudette", "sonnets", "nothing"):
            with self.subTest(text=text):
                self.assertIsNone(cv.FORBIDDEN.search(text))

    def test_private_and_build_files_are_recognised(self) -> None:
        for name in (".env", ".env.local", "id_rsa", "keystore.properties", "local.properties", "key.pem", "a/b/server.p12", "secrets.json", "x.log", "m.pyc", ".DS_Store", "google-services.json"):
            with self.subTest(name=name):
                self.assertIsNotNone(cv.PRIVATE_FILES.search(name))
        for name in (".env.example", "README.md", "src/main.rs", "docs/secrets-policy.md"):
            with self.subTest(name=name):
                self.assertIsNone(cv.PRIVATE_FILES.search(name))

    def test_the_required_keys_of_the_manifest_include_the_version_and_the_build(self) -> None:
        for key in ("schema_version", "ecosystem", "name", "version", "maturity", "native_version", "build"):
            self.assertIn(key, cv.REQUIRED)

    def test_the_eight_language_files_are_listed(self) -> None:
        self.assertEqual(set(cv.LANGUAGES.values()), {"en", "es", "de", "fr", "it", "ja", "zh", "pt"})


if __name__ == "__main__":
    unittest.main()
