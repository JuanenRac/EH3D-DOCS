# =============================================================================
# EH3D-DOCS - tools/test_suite_contract.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check that the repositories of the suite fit each other (tools/suite_contract.py)."""
from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_suite_contract", TOOLS / "suite_contract.py")
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)


def make(root: Path, name: str, version: str = "0.0.1", cargo: str = "") -> Path:
    repo = root / name
    repo.mkdir()
    (repo / "eh3d.project.json").write_text(json.dumps({"name": name, "version": version}), encoding="utf-8")
    if cargo:
        (repo / "Cargo.toml").write_text(cargo, encoding="utf-8")
    return repo


class SuiteContractTests(unittest.TestCase):
    def run_in(self, root: Path, **kwargs):
        return CONTRACT.run(root, allow_file=root / "none.txt", **kwargs)

    def test_a_suite_that_fits_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-COMMON")
            make(root, "EH3D-AUTOLEVEL", cargo='[dependencies]\neh3d-levelling = { version = ">=0.0.1", path = "../EH3D-COMMON/crates/levelling" }\n')
            ok, found = self.run_in(root)
            self.assertTrue(ok)
            self.assertEqual(found, [])

    def test_a_manifest_that_does_not_fit_its_folder_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make(root, "EH3D-COMMON")
            (repo / "eh3d.project.json").write_text(json.dumps({"name": "EH3D-OTHER", "version": "v1"}), encoding="utf-8")
            ok, found = self.run_in(root, only="manifests")
            self.assertFalse(ok)
            self.assertEqual(len(found), 2)

    def test_a_damaged_manifest_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make(root, "EH3D-COMMON")
            (repo / "eh3d.project.json").write_text("{ not json", encoding="utf-8")
            ok, found = self.run_in(root, only="manifests")
            self.assertFalse(ok)
            self.assertIn("not a JSON object", found[0].text)

    def test_a_path_dependency_with_no_version_is_a_warning_and_fails_only_when_strict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-AUTOLEVEL", cargo='[dependencies]\neh3d-levelling = { path = "../EH3D-COMMON/crates/levelling" }\nserde = { version = "1", features = ["derive"] }\n')
            ok, found = self.run_in(root, only="paths")
            self.assertTrue(ok)
            self.assertEqual([f.level for f in found], ["WARNING"])
            self.assertIn("eh3d-levelling", found[0].text)
            ok, _ = self.run_in(root, only="paths", strict=True)
            self.assertFalse(ok)

    def test_the_version_of_the_map_is_the_one_of_the_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-COMMON", version="0.1.0")
            make(root, "EH3D-DOCS", version="0.0.4")
            docs = root / "EH3D-DOCS" / "docs"
            docs.mkdir()
            (docs / "SUITE_MAP.md").write_text(
                "| Repository | Kind | State | Release | What |\n|---|---|---|---|---|\n"
                "| [EH3D-COMMON](https://example.invalid/EH3D-COMMON) | Library | Published | 0.0.8 | x |\n"
                "| [EH3D-DOCS](https://example.invalid/EH3D-DOCS) | Documentation | Published | 0.0.4 | x |\n"
                "| [EH3D-NOTHERE](https://example.invalid/EH3D-NOTHERE) | Library | Started | none | x |\n",
                encoding="utf-8",
            )
            _, found = self.run_in(root, only="versions")
            self.assertEqual(len(found), 1)
            self.assertIn("0.0.8", found[0].text)
            self.assertIn("0.1.0", found[0].text)

    def test_the_release_column_is_written_from_the_manifests_and_nothing_else_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-COMMON", version="0.1.0")
            make(root, "EH3D-DOCS", version="0.0.4")
            docs = root / "EH3D-DOCS" / "docs"
            docs.mkdir()
            table = (
                "# The map\n\nWords that are a person's | with a bar.\n\n| Repository | Kind | State | Release | What |\n|---|---|---|---|---|\n"
                "| [EH3D-COMMON](https://example.invalid/EH3D-COMMON) | Library | Published | 0.0.8 | what it is `x` |\n"
                "| [EH3D-DOCS](https://example.invalid/EH3D-DOCS) | Documentation | Published | 0.0.4 | This hub. |\n"
                "| [EH3D-NOTHERE](https://example.invalid/EH3D-NOTHERE) | Library | Started | - | x |\n"
            )
            (docs / "SUITE_MAP.md").write_bytes(table.replace("\n", "\r\n").encode("utf-8"))
            # asking changes nothing
            self.assertEqual(CONTRACT.write_map(root, write=False), ["EH3D-COMMON: 0.0.8 -> 0.1.0"])
            self.assertIn(b"0.0.8", (docs / "SUITE_MAP.md").read_bytes())
            # writing changes the one cell, keeps the line ends and the rest of the words
            self.assertEqual(CONTRACT.write_map(root), ["EH3D-COMMON: 0.0.8 -> 0.1.0"])
            after = (docs / "SUITE_MAP.md").read_bytes().decode("utf-8")
            self.assertEqual(after, table.replace("0.0.8", "0.1.0").replace("\n", "\r\n"))
            # it is then in step
            self.assertEqual(CONTRACT.write_map(root), [])
            _, found = self.run_in(root, only="versions")
            self.assertEqual(found, [])

    def test_the_screens_and_the_server_agree_on_the_port(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            server = root / "EH3D-SERVER" / "src"
            server.mkdir(parents=True)
            (server / "config.rs").write_text("/// Where the server listens: the port 18200.\n", encoding="utf-8")
            for name, port in (("EH3D-NODE-BUNGARD-HMI", 18200), ("EH3D-NODE-HMI-GUI", 8080)):
                core = root / name / "core"
                core.mkdir(parents=True)
                (core / "hmi_config.hpp").write_text(f"std::uint16_t server_port = {port};\n", encoding="utf-8")
            ok, found = self.run_in(root, only="ports")
            self.assertFalse(ok)
            self.assertEqual([f.repo for f in found], ["EH3D-NODE-HMI-GUI"])

    def test_the_manifest_has_to_be_accepted_by_the_parser_of_the_updater(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parser = root / "EH3D-UPDATER" / "src" / "eh3d_updater"
            parser.mkdir(parents=True)
            (parser / "project_manifest.py").write_text(
                "def parse_manifest(text, *, expected_name=None):\n"
                "    import json\n"
                "    if 'role' not in json.loads(text):\n"
                "        raise ValueError('missing field(s): role')\n",
                encoding="utf-8",
            )
            repo = make(root, "EH3D-COMMON")
            _, found = self.run_in(root, only="manifests")
            self.assertEqual([f.level for f in found], ["ERROR"])
            self.assertIn("rejects the manifest", found[0].text)
            (repo / "eh3d.project.json").write_text(json.dumps({"name": "EH3D-COMMON", "version": "0.0.1", "role": "library"}), encoding="utf-8")
            self.assertEqual(self.run_in(root, only="manifests")[1], [])

    def test_without_the_updater_the_parser_check_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-COMMON")
            self.assertEqual(self.run_in(root, only="manifests")[1], [])

    def test_a_repository_with_another_validator_is_a_warning_and_never_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, body, tools_version in (("EH3D-DOCS", "print(1)\n", "1"), ("EH3D-SERVER", "print(2)\n", "0")):
                repo = make(root, name)
                (repo / "tools").mkdir()
                (repo / "tools" / "ci_validate.py").write_text(f"# ====\n# canonical: EH3D-DOCS tools {tools_version}\n{body}", encoding="utf-8")
            ok, found = self.run_in(root, only="tools")
            self.assertTrue(ok)
            self.assertEqual({f.repo for f in found}, {"EH3D-SERVER"})
            self.assertEqual({f.level for f in found}, {"WARNING"})
            ok, _ = self.run_in(root, only="tools", strict=True)
            self.assertFalse(ok)

    def test_a_known_exception_is_left_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-AUTOLEVEL", cargo='eh3d-levelling = { path = "../EH3D-COMMON/crates/levelling" }\n')
            allow = root / "allow.txt"
            allow.write_text("# known\npaths EH3D-AUTOLEVEL\n", encoding="utf-8")
            ok, found = CONTRACT.run(root, only="paths", strict=True, allow_file=allow)
            self.assertTrue(ok)
            self.assertEqual(found, [])

    def test_an_empty_workspace_has_nothing_to_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ok, found = self.run_in(Path(tmp))
            self.assertTrue(ok)
            self.assertEqual(found, [])


SUITE = {
    "server": {"port": 18200},
    "manifest": {"ecosystem": "EH3D", "schema_versions": ["1.0", "1.1"]},
    "languages": [{"readme": "README.md"}, {"readme": "README_spa.md"}, {"readme": "README_deu.md"}],
    "spindle_rpm": {"field_min": 0, "field_max": 65535},
    "version": {"pattern": r"^\d+\.\d+\.\d+(\.\d+)?$"},
}


class ConstantsTests(unittest.TestCase):
    def workspace(self, root: Path, suite: dict | None = None) -> None:
        docs = make(root, "EH3D-DOCS")
        (docs / "docs").mkdir()
        (docs / "docs" / "suite.json").write_text(json.dumps(suite or SUITE), encoding="utf-8")

    def put(self, root: Path, repo: str, rel: str, text: str) -> None:
        path = root / repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def readmes(self, root: Path, repo: str) -> None:
        self.put(root, repo, "README.md", "[es](README_spa.md) [de](README_deu.md)\n")
        self.put(root, repo, "README_spa.md", "x")
        self.put(root, repo, "README_deu.md", "x")

    def run_constants(self, root: Path):
        return CONTRACT.run(root, only="constants", allow_file=root / "none.txt")

    def test_without_a_suite_json_there_is_nothing_to_compare(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS")
            ok, found = self.run_constants(root)
            self.assertTrue(ok)
            self.assertEqual(found, [])

    def test_a_suite_that_agrees_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root)
            self.readmes(root, "EH3D-DOCS")
            make(root, "EH3D-SERVER")
            self.readmes(root, "EH3D-SERVER")
            self.put(root, "EH3D-SERVER", "server.cfg.example", "# c\nlisten = 0.0.0.0:18200\n")
            self.put(root, "EH3D-STUDIO", "run.sh", 'EH3D_SERVER="${1:-http://127.0.0.1:18200}"\n')
            self.put(root, "EH3D-COMMON", "firmware_base/core/keyboard.hpp", '{"spindle_max_rpm", FieldKind::Number, 0, 65535, 0},\n')
            ok, found = self.run_constants(root)
            self.assertEqual([str(f) for f in found], [])

    def test_a_port_that_differs_is_a_warning_not_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root, {**SUITE, "languages": []})
            self.put(root, "EH3D-STUDIO", "run.sh", 'EH3D_SERVER="${1:-http://127.0.0.1:9999}"\n')
            self.put(root, "EH3D-DRILLPRO", "config/machine.cfg.example", "server_address = 192.168.0.200:18200\n")
            ok, found = self.run_constants(root)
            self.assertTrue(ok)
            self.assertEqual([(f.repo, f.level) for f in found], [("EH3D-STUDIO", "WARNING")])
            self.assertIn("9999", found[0].text)
            ok, _ = CONTRACT.run(root, only="constants", strict=True, allow_file=root / "none.txt")
            self.assertFalse(ok)

    def test_the_rpm_field_of_the_panel_is_compared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root, {**SUITE, "languages": []})
            self.put(root, "EH3D-COMMON", "firmware_base/core/keyboard.hpp", '{"spindle_max_rpm", FieldKind::Number, 0, 30000, 0},\n')
            ok, found = self.run_constants(root)
            self.assertEqual(len(found), 1)
            self.assertIn("0..30000", found[0].text)

    def test_missing_readme_languages_and_a_missing_link_are_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root)
            self.readmes(root, "EH3D-DOCS")
            make(root, "EH3D-SERVER")
            self.put(root, "EH3D-SERVER", "README.md", "no links here\n")
            self.put(root, "EH3D-SERVER", "README_spa.md", "x")
            ok, found = self.run_constants(root)
            texts = sorted(f.text for f in found)
            self.assertEqual(len(texts), 2)
            self.assertTrue(any("README_deu.md is missing" in t for t in texts))
            self.assertTrue(any("no link to README_spa.md" in t for t in texts))

    def test_a_manifest_that_leaves_the_schema_or_the_version_shape_is_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root, {**SUITE, "languages": []})
            repo = make(root, "EH3D-ODD", version="v1")
            (repo / "eh3d.project.json").write_text(json.dumps({"name": "EH3D-ODD", "version": "v1", "ecosystem": "ARMOR", "schema_version": "3.0"}), encoding="utf-8")
            ok, found = self.run_constants(root)
            self.assertEqual(len(found), 3)
            self.assertTrue(all(f.level == "WARNING" for f in found))

    def test_the_suite_json_of_this_repository_is_well_formed(self) -> None:
        suite = json.loads((TOOLS.parent / "docs" / "suite.json").read_text(encoding="utf-8"))
        self.assertEqual(suite["server"]["port"], 18200)
        self.assertEqual([lang["readme"] for lang in suite["languages"]][0], "README.md")
        self.assertEqual(len(suite["languages"]), 8)
        self.assertEqual(suite["manifest"]["file"], "eh3d.project.json")
        self.assertTrue(re.match(suite["version"]["pattern"], "0.8.0.1") and re.match(suite["version"]["pattern"], "0.4.9"))
        self.assertIsNone(re.match(suite["version"]["pattern"], "1.2"))


class TemplatesTests(unittest.TestCase):
    SUITE = {"github_templates": [".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug-report.yml"]}

    def workspace(self, root: Path) -> None:
        docs = make(root, "EH3D-DOCS")
        (docs / "docs").mkdir()
        (docs / "docs" / "suite.json").write_text(json.dumps(self.SUITE), encoding="utf-8")

    def fill(self, repo: Path, *names: str) -> None:
        for rel in names:
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / rel).write_text("name: x\n", encoding="utf-8")

    def test_a_repository_with_the_templates_has_no_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root)
            for name in ("EH3D-DOCS", "EH3D-SERVER"):
                self.fill(root / name if (root / name).exists() else make(root, name), *self.SUITE["github_templates"])
            ok, found = CONTRACT.run(root, only="templates", allow_file=root / "none.txt")
            self.assertTrue(ok)
            self.assertEqual(found, [])

    def test_a_missing_or_empty_template_is_a_warning_that_names_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root)
            self.fill(root / "EH3D-DOCS", *self.SUITE["github_templates"])
            server = make(root, "EH3D-SERVER")
            self.fill(server, ".github/PULL_REQUEST_TEMPLATE.md")
            (server / ".github" / "ISSUE_TEMPLATE").mkdir()
            (server / ".github" / "ISSUE_TEMPLATE" / "bug-report.yml").write_text("  \n", encoding="utf-8")
            ok, found = CONTRACT.run(root, only="templates", allow_file=root / "none.txt")
            self.assertTrue(ok)
            self.assertEqual([(f.repo, f.level) for f in found], [("EH3D-SERVER", "WARNING")])
            self.assertIn("bug-report.yml", found[0].text)
            self.assertNotIn("PULL_REQUEST", found[0].text)

    def test_the_updater_of_the_family_is_looked_at_too(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root)
            self.fill(root / "EH3D-DOCS", *self.SUITE["github_templates"])
            (root / "ELECTRO-HOBBY-3D-UPDATER").mkdir()
            ok, found = CONTRACT.run(root, only="templates", allow_file=root / "none.txt")
            self.assertEqual([f.repo for f in found], ["ELECTRO-HOBBY-3D-UPDATER"])

    def test_the_repository_itself_has_every_template_it_asks_for(self) -> None:
        suite = json.loads((TOOLS.parent / "docs" / "suite.json").read_text(encoding="utf-8"))
        self.assertEqual(len(suite["github_templates"]), 6)
        for rel in suite["github_templates"]:
            self.assertTrue((TOOLS.parent / rel).read_text(encoding="utf-8").strip(), rel)


if __name__ == "__main__":
    unittest.main()
