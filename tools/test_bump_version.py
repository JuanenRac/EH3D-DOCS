# =============================================================================
# EH3D-DOCS - tools/test_bump_version.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The odometer, the places of the version and tools/bump_version.py, on toy repositories in temporary folders."""
from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

import _toy_repo as toy
import bump_version
import changelog_tools
import version_places as vp

FULL = dict(cargo=True, npm=True, python=True, gradle=True, ios=True)


def run(args: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = bump_version.main(args)
    return code, buffer.getvalue()


def text(repo: Path, rel: str) -> str:
    return (repo / rel).read_bytes().decode("utf-8")


class OdometerTests(unittest.TestCase):
    def test_every_number_goes_to_nine_and_carries(self) -> None:
        for old, new in (("0.0.0", "0.0.1"), ("0.0.9", "0.1.0"), ("0.4.9", "0.5.0"), ("0.7.8", "0.7.9"), ("0.7.9", "0.8.0.0"),
                         ("0.8.0.0", "0.8.0.1"), ("0.8.0.9", "0.8.1.0"), ("0.8.9.9", "0.9.0.0"), ("0.9.9.9", "1.0.0.0"), ("1.0.0.9", "1.0.1.0")):
            self.assertEqual(vp.next_version(old), new, old)

    def test_a_number_never_has_two_digits(self) -> None:
        with self.assertRaises(vp.VersionError):
            vp.check_digits("0.0.10")
        with self.assertRaises(vp.VersionError):
            vp.next_version("0.10.0")
        with self.assertRaises(vp.VersionError):
            vp.next_version("9.9.9.9")
        with self.assertRaises(vp.VersionError):
            vp.parse("0.1")

    def test_four_components_are_greater_than_three_with_the_same_start(self) -> None:
        self.assertEqual(vp.compare("0.8.0.1", "0.8.0"), 1)
        self.assertEqual(vp.compare("0.8.0.0", "0.8.0"), 0)
        self.assertEqual(vp.compare("0.1.0", "0.0.9"), 1)


class BumpTests(unittest.TestCase):
    def test_every_place_gets_the_new_version_and_the_old_one_is_left_nowhere_but_in_the_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), **FULL)
            code, out = run([str(repo), "next", "The second", "--workspace", tmp])
            self.assertEqual(code, 0, out)
            self.assertIn("BUMP=PASS", out)
            self.assertEqual(vp.check(vp.Repo(repo)), [])
            self.assertEqual(json.loads(text(repo, "eh3d.project.json"))["version"], "0.1.0")
            self.assertIn("Scaffolding v0.1.0:", text(repo, "eh3d.project.json"))
            self.assertIn('name = "toy"\nversion = "0.1.0"', text(repo, "Cargo.lock"))
            self.assertIn('name = "serde"\nversion = "1.0.1"', text(repo, "Cargo.lock"))
            self.assertIn('serde = { version = "1" }', text(repo, "Cargo.toml"))
            self.assertIn('versionCode = 8; versionName = "0.1.0"', text(repo, "app/build.gradle.kts"))
            self.assertIn('MARKETING_VERSION: "0.1.0"', text(repo, "project.yml"))
            self.assertIn('CURRENT_PROJECT_VERSION: "7"', text(repo, "project.yml"))
            self.assertIn('__version__ = "0.1.0"', text(repo, "src/toy/__init__.py"))
            self.assertIn('version = "0.1.0"', text(repo, "pyproject.toml"))
            for rel in toy.LANGS:
                page = text(repo, rel)
                self.assertIn("Version-0.1.0-", page, rel)
                self.assertIn("`0.1.0` |", page, rel)
                self.assertNotIn("0.0.9", page, rel)
            # nothing but the history of the CHANGELOG still says 0.0.9
            for path in repo.rglob("*"):
                if path.is_file() and path.name != "CHANGELOG.md" and path.name != "Cargo.lock":
                    self.assertNotIn("0.0.9", path.read_text(encoding="utf-8"), str(path.relative_to(repo)))

    def test_package_json_and_its_lock_are_updated_and_stay_equal_to_the_manifest(self) -> None:
        """A release once shipped with the old number inside because package.json was left behind: the files must follow the manifest."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), npm=True)
            code, out = run([str(repo), "0.1.0", "The second"])
            self.assertEqual(code, 0, out)
            package = json.loads(text(repo, "package.json"))
            lock = json.loads(text(repo, "package-lock.json"))
            manifest = json.loads(text(repo, "eh3d.project.json"))["version"]
            self.assertEqual((package["version"], lock["version"], lock["packages"][""]["version"]), (manifest,) * 3)
            self.assertEqual(lock["packages"]["node_modules/left"]["version"], "1.0.0")
            self.assertEqual(package["dependencies"], {"left": "1.0.0"})

    def test_a_file_left_behind_is_found_by_the_check_and_stops_the_bump(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), npm=True)
            toy.write(repo, "package.json", text(repo, "package.json").replace("0.0.9", "0.0.8"))
            problems = vp.check(vp.Repo(repo))
            self.assertTrue(any("package.json" in p and "0.0.8" in p for p in problems), problems)
            code, out = run([str(repo), "next", "T"])
            self.assertEqual(code, 1)
            self.assertIn("package.json", out)
            self.assertIn("0.0.9", json.loads(text(repo, "eh3d.project.json"))["version"])  # nothing was written
            code, out = run([str(repo), "next", "T", "--fix-drift"])
            self.assertEqual(code, 0, out)
            self.assertEqual(vp.check(vp.Repo(repo)), [])

    def test_a_missing_file_that_should_carry_the_version_fails_with_a_clear_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), cargo=True)
            (repo / "README_por.md").unlink()
            code, out = run([str(repo), "next", "T"])
            self.assertEqual(code, 1)
            self.assertIn("README_por.md is missing", out)
            repo2 = toy.make_repo(Path(tmp), name="EH3D-TOY2", cargo=True)
            toy.write(repo2, "Cargo.lock", '[[package]]\nname = "other"\nversion = "0.0.9"\n')
            code, out = run([str(repo2), "next", "T"])
            self.assertEqual(code, 1)
            self.assertIn("Cargo.lock has no entry of the package toy", out)
            repo3 = toy.make_repo(Path(tmp), name="EH3D-TOY3")
            toy.write(repo3, "README_ita.md", text(repo3, "README_ita.md").replace("`0.0.9`", "`nine`"))
            code, out = run([str(repo3), "next", "T"])
            self.assertEqual(code, 1)
            self.assertIn('README_ita.md has no version in the "Version" row', out)

    def test_the_odometer_decides_unless_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp))
            code, out = run([str(repo), "0.0.10", "T"])
            self.assertEqual(code, 1)
            self.assertIn("two digits", out)
            code, out = run([str(repo), "0.0.8", "T"])
            self.assertEqual((code, "not greater" in out), (1, True))
            code, out = run([str(repo), "0.2.0", "T"])
            self.assertEqual(code, 1)
            self.assertIn("odometer gives 0.1.0", out)
            code, out = run([str(repo), "0.2.0", "T", "--explicit"])
            self.assertEqual(code, 0, out)
            self.assertEqual(json.loads(text(repo, "eh3d.project.json"))["version"], "0.2.0")

    def test_four_components_start_at_0_8_0_0(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), version="0.7.9", cargo=True)
            code, out = run([str(repo), "next", "T"])
            self.assertEqual(code, 0, out)
            self.assertIn("0.7.9 -> 0.8.0.0", out)
            self.assertIn('version = "0.8.0.0"', text(repo, "Cargo.toml"))
            toy.write(repo, "CHANGELOG.md", text(repo, "CHANGELOG.md").replace("## [Unreleased]\n", "## [Unreleased]\n\n- **More:** one.\n", 1))
            code, out = run([str(repo), "0.8.0.1", "T2"])
            self.assertEqual(code, 0, out)
            repo4 = toy.make_repo(Path(tmp), name="EH3D-FOUR", version="0.8.0.9")
            code, out = run([str(repo4), "next", "T"])
            self.assertEqual(code, 0, out)
            self.assertIn("0.8.1.0", out)

    def test_dry_run_writes_nothing_and_shows_the_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), **FULL)
            before = {p: p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            code, out = run([str(repo), "next", "T", "--dry-run"])
            self.assertEqual(code, 0, out)
            self.assertIn("DRY-RUN", out)
            self.assertIn("+++ b/Cargo.toml", out)
            self.assertIn('+version = "0.1.0"', out)
            self.assertEqual(before, {p: p.read_bytes() for p in repo.rglob("*") if p.is_file()})

    def test_the_line_ends_of_each_file_are_kept(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            crlf = toy.make_repo(Path(tmp), name="EH3D-CRLF", crlf=True, **FULL)
            lf = toy.make_repo(Path(tmp), name="EH3D-LF", **FULL)
            self.assertEqual(run([str(crlf), "next", "T"])[0], 0)
            self.assertEqual(run([str(lf), "next", "T"])[0], 0)
            for path in crlf.rglob("*"):
                if path.is_file():
                    raw = path.read_bytes()
                    self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"), path.name)
            for path in lf.rglob("*"):
                if path.is_file():
                    self.assertNotIn(b"\r", path.read_bytes(), path.name)
            self.assertEqual(vp.check(vp.Repo(crlf)), [])

    def test_a_mixed_workspace_keeps_each_file_as_it_was(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), cargo=True)
            toy.write(repo, "Cargo.toml", text(repo, "Cargo.toml"), crlf=True)
            self.assertEqual(run([str(repo), "next", "T"])[0], 0)
            self.assertIn(b"\r\n", (repo / "Cargo.toml").read_bytes())
            self.assertNotIn(b"\r", (repo / "README.md").read_bytes())

    def test_the_changelog_keeps_every_entry_and_the_old_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), entries=4)
            before = text(repo, "CHANGELOG.md")
            self.assertEqual(run([str(repo), "next", "The second one"])[0], 0)
            after = text(repo, "CHANGELOG.md")
            self.assertIn("## [Unreleased]\n\n## [0.1.0] - The second one\n\n- **Change 0:**", after)
            self.assertEqual(changelog_tools.unreleased_body(after), "")
            section = changelog_tools.find(after, "0.1.0")
            self.assertEqual(changelog_tools.count_entries(changelog_tools.body(after, section)), 4)
            self.assertTrue(after.endswith("## [0.0.9] - The first one\n\n- **Start:** it began.\n"))
            for i in range(4):
                self.assertEqual(after.count(f"Change {i}:"), 1)
            self.assertEqual(before.count("Change"), after.count("Change"))

    def test_an_empty_unreleased_or_a_repeated_version_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), entries=0)
            code, out = run([str(repo), "next", "T"])
            self.assertEqual(code, 1)
            self.assertIn("no entries to promote", out)
            with self.assertRaises(changelog_tools.ChangelogError):
                changelog_tools.promote("# C\n\n## [Unreleased]\n\n- a\n\n## [0.1.0] - x\n", "0.1.0", "T")
            with self.assertRaises(changelog_tools.ChangelogError):
                changelog_tools.promote("# C\n\n- a\n", "0.1.0", "T")

    def test_the_file_named_by_native_version_follows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), version="0.0.4", native="VERSION")
            self.assertEqual(run([str(repo), "next", "T"])[0], 0)
            self.assertEqual(text(repo, "VERSION"), "0.0.5\n")

    def test_the_final_check_catches_a_place_that_the_script_cannot_reach(self) -> None:
        """The check at the end is the guarantee: if a file still holds another version, the bump fails and says which."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), npm=True)
            original = vp.apply

            def forgetful(r: vp.Repo, old: str, new: str, fix: bool = False):
                result = original(r, old, new, fix)
                r.write("package.json", (r.read("package.json") or "").replace(new, old))
                return result

            vp.apply = forgetful
            try:
                code, out = run([str(repo), "next", "T"])
            finally:
                vp.apply = original
            self.assertEqual(code, 1)
            self.assertIn("package.json", out)
            self.assertIn("0.0.9", json.loads(text(repo, "package.json"))["version"])  # the failure happened before any write


class ShapeTests(unittest.TestCase):
    def test_no_private_names_in_the_tools_of_this_family(self) -> None:
        words = ["son" + "net", "scratch" + "pad", "c:" + "\\users", "cla" + "ude", "anthro" + "pic"]
        pattern = re.compile("(?i)" + "|".join(re.escape(w) for w in words))
        for name in ("bump_version.py", "version_places.py", "changelog_tools.py", "release_notes.py", "prerelease_check.py"):
            self.assertIsNone(pattern.search((Path(__file__).parent / name).read_text(encoding="utf-8")), name)


if __name__ == "__main__":
    unittest.main()
