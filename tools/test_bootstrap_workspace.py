# =============================================================================
# EH3D-DOCS - tools/test_bootstrap_workspace.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/bootstrap_workspace.py on toy repositories: the needs are read from the files, with no list of repositories."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from _toy_repo import git, write

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_bootstrap", TOOLS / "bootstrap_workspace.py")
BOOT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BOOT  # the dataclasses of the module look themselves up here
SPEC.loader.exec_module(BOOT)

CARGO = '[dependencies]\nlib = {{ version = ">=0.0.1", path = "../{dep}/crates/lib" }}\n'


def toy(root: Path, name: str, cargo: str = "", npm: str = "", depends_on: list[str] | None = None, commit: bool = False) -> Path:
    repo = root / name
    write(repo, "README.md", f"# {name}\n")
    if cargo:
        write(repo, "Cargo.toml", cargo)
    if npm:
        write(repo, "package.json", npm)
    manifest = {"name": name, "version": "0.0.1"}
    if depends_on:
        manifest["depends_on"] = depends_on
    write(repo, "eh3d.project.json", json.dumps(manifest))
    if commit:
        git(repo, "init", "-q", "-b", "main")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "first")
    return repo


def run_main(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = BOOT.main(list(argv))
        except SystemExit as exit_:
            code = exit_.code
    return code, out.getvalue(), err.getvalue()


class NeedsTests(unittest.TestCase):
    def test_a_cargo_path_in_any_folder_of_the_repository_is_a_need(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = toy(root, "EH3D-APP", cargo='[package]\nname = "app"\n')
            write(repo, "crates/inner/Cargo.toml", CARGO.format(dep="EH3D-COMMON").replace('"../', '"../../../'))
            write(repo, "crates/inner/other.toml", "ignored")
            self.assertEqual(BOOT.needs_of(repo, root), {"EH3D-COMMON": "Cargo.toml"})

    def test_a_path_that_stays_inside_the_repository_is_not_a_need(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = toy(root, "EH3D-APP", cargo='lib = { path = "crates/lib" }\nother = { path = "../EH3D-APP/crates/x" }\n')
            self.assertEqual(BOOT.needs_of(repo, root), {})

    def test_package_json_file_link_and_portal_references_and_the_manifest_are_needs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            npm = '{"dependencies": {"a": "file:../EH3D-A", "b": "link:../EH3D-B/pkg", "c": "portal:../EH3D-C", "d": "^1.0.0"}}'
            repo = toy(root, "EH3D-APP", npm=npm, depends_on=["EH3D-M"])
            self.assertEqual(BOOT.needs_of(repo, root), {"EH3D-A": "package.json", "EH3D-B": "package.json", "EH3D-C": "package.json", "EH3D-M": "eh3d.project.json"})

    def test_build_folders_are_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = toy(root, "EH3D-APP")
            write(repo, "target/debug/Cargo.toml", CARGO.format(dep="EH3D-GHOST"))
            write(repo, "node_modules/x/package.json", '{"a": "file:../../../EH3D-GHOST"}')
            self.assertEqual(BOOT.needs_of(repo, root), {})

    def test_a_path_that_leaves_the_workspace_is_not_a_need(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ws"
            root.mkdir()
            repo = toy(root, "EH3D-APP", cargo='lib = { path = "../../elsewhere" }\n')
            self.assertEqual(BOOT.needs_of(repo, root), {})


class WalkTests(unittest.TestCase):
    def test_the_walk_is_recursive_lists_each_repository_once_and_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            toy(root, "EH3D-APP", cargo=CARGO.format(dep="EH3D-MID"), depends_on=["EH3D-MID"])
            toy(root, "EH3D-MID", cargo=CARGO.format(dep="EH3D-LEAF") + CARGO.format(dep="EH3D-APP"))
            toy(root, "EH3D-LEAF")
            before = sorted(p.name for p in root.iterdir())
            plan = BOOT.bootstrap(root, "EH3D-APP")
            self.assertEqual([(r.name, r.status) for r in plan.repos], [("EH3D-APP", "present"), ("EH3D-MID", "present"), ("EH3D-LEAF", "present")])
            self.assertEqual(sorted(p.name for p in root.iterdir()), before)

    def test_dry_run_is_the_default_and_names_what_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            toy(root, "EH3D-APP", cargo=CARGO.format(dep="EH3D-MID"))
            code, out, _ = run_main("EH3D-APP", "--workspace", str(root))
            self.assertEqual(code, 0)
            self.assertIn("EH3D-MID", out)
            self.assertIn("missing", out)
            self.assertIn("BOOTSTRAP=PLAN repos=2 present=1 missing=1 cloned=0 failed=0", out)
            self.assertFalse((root / "EH3D-MID").exists())

    def test_clone_fetches_the_missing_ones_level_by_level_with_a_shallow_clone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = Path(tmp) / "remote", Path(tmp) / "work"
            remote.mkdir()
            work.mkdir()
            toy(remote, "EH3D-MID", cargo=CARGO.format(dep="EH3D-LEAF"), commit=True)
            toy(remote, "EH3D-LEAF", commit=True)
            toy(work, "EH3D-APP", cargo=CARGO.format(dep="EH3D-MID"))
            code, out, _ = run_main("EH3D-APP", "--workspace", str(work), "--clone", "--url-template", remote.as_uri() + "/{name}")
            self.assertEqual(code, 0, out)
            self.assertIn("BOOTSTRAP=DONE repos=3 present=1 missing=0 cloned=2 failed=0", out)
            self.assertTrue((work / "EH3D-LEAF" / "README.md").is_file())
            self.assertTrue((work / "EH3D-LEAF" / ".git" / "shallow").is_file())

    def test_the_command_given_to_git_is_a_depth_one_clone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            toy(root, "EH3D-APP", cargo=CARGO.format(dep="EH3D-MID"))
            calls = []

            def fake(command, **kwargs):
                calls.append(command)
                (Path(command[-1])).mkdir()

                class Done:
                    returncode, stderr = 0, ""

                return Done()

            BOOT.bootstrap(root, "EH3D-APP", clone=True, run=fake)
            self.assertEqual(calls[0][:5], ["git", "clone", "--depth", "1", "--quiet"])
            self.assertEqual(calls[0][5], "https://github.com/JuanenRac/EH3D-MID.git")

    def test_a_failed_clone_is_reported_and_ends_with_1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = Path(tmp) / "remote", Path(tmp) / "work"
            remote.mkdir()
            work.mkdir()
            toy(work, "EH3D-APP", cargo=CARGO.format(dep="EH3D-NOWHERE"))
            code, out, _ = run_main("EH3D-APP", "--workspace", str(work), "--clone", "--url-template", remote.as_uri() + "/{name}")
            self.assertEqual(code, 1)
            self.assertIn("failed=1", out)

    def test_an_existing_folder_is_used_as_it_is(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            toy(root, "EH3D-APP", cargo=CARGO.format(dep="EH3D-MID"))
            (root / "EH3D-MID").mkdir()
            (root / "EH3D-MID" / "mine.txt").write_text("keep", encoding="utf-8")
            plan = BOOT.bootstrap(root, "EH3D-APP", clone=True, run=lambda *a, **k: self.fail("it must not clone"))
            self.assertEqual([r.status for r in plan.repos], ["present", "present"])
            self.assertEqual((root / "EH3D-MID" / "mine.txt").read_text(encoding="utf-8"), "keep")

    def test_a_start_that_is_not_there_ends_with_2_and_cloning_it_works(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote, work = Path(tmp) / "remote", Path(tmp) / "work"
            remote.mkdir()
            work.mkdir()
            toy(remote, "EH3D-APP", commit=True)
            code, out, _ = run_main("EH3D-APP", "--workspace", str(work))
            self.assertEqual(code, 2)
            code, out, _ = run_main("EH3D-APP", "--workspace", str(work), "--clone", "--url-template", remote.as_uri() + "/{name}")
            self.assertEqual(code, 0)
            self.assertTrue((work / "EH3D-APP").is_dir())


class UsageTests(unittest.TestCase):
    def test_wrong_use_ends_with_64(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for argv in (["EH3D-APP"], ["EH3D-APP", "--workspace", tmp, "--clone", "--dry-run"], ["../x", "--workspace", tmp], ["EH3D-APP", "--workspace", tmp, "--url-template", "nothing"]):
                self.assertEqual(run_main(*argv)[0], 64, argv)

    def test_a_workspace_that_does_not_exist_is_an_error_for_a_listing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run_main("EH3D-APP", "--workspace", str(Path(tmp) / "gone"))[0], 1)


if __name__ == "__main__":
    unittest.main()
