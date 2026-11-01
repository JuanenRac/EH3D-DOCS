# =============================================================================
# EH3D-DOCS - tools/test_suite_contract.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check that the repositories of the suite fit each other (tools/suite_contract.py)."""
from __future__ import annotations

import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
