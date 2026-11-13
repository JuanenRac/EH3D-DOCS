# =============================================================================
# EH3D-DOCS - tools/test_release_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/release_notes.py and tools/prerelease_check.py on toy repositories."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import _toy_repo as toy
import prerelease_check as pc
import release_notes as rn


def run(module, args: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = module.main(args)
    return code, buffer.getvalue()


def release_ready(root: Path, **kwargs) -> Path:
    """A toy repository whose newest CHANGELOG section is the version of the manifest, with 5 entries, and an empty [Unreleased]."""
    repo = toy.make_repo(root, entries=0, **kwargs)
    section = "".join(f"- **Change {i}:** something.\n" for i in range(5))
    toy.write(repo, "CHANGELOG.md", f"# Changelog\n\n## [Unreleased]\n\n## [0.0.9] - The ninth\n\n{section}\n## [0.0.8] - Older\n\n- **Old:** x.\n")
    toy.write(repo, "tools/ci_validate.py", "# a stand-in: the tests give the answer of the validator\n")
    return repo


class ReleaseNotesTests(unittest.TestCase):
    def test_the_title_and_the_notes_of_the_version_of_the_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = release_ready(Path(tmp))
            code, out = run(rn, [str(repo)])
            self.assertEqual(code, 0)
            self.assertTrue(out.startswith("EH3D-TOY 0.0.9 - The ninth\n\n- **Change 0:**"), out)
            self.assertNotIn("Old:", out)
            self.assertEqual(run(rn, [str(repo), "--title"])[1], "EH3D-TOY 0.0.9 - The ninth\n")
            self.assertEqual(run(rn, [str(repo), "0.0.8", "--notes"])[1], "- **Old:** x.\n")

    def test_a_version_without_a_section_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = release_ready(Path(tmp))
            code, out = run(rn, [str(repo), "0.5.0"])
            self.assertEqual(code, 1)
            self.assertIn("no section for 0.5.0", out)

    def test_check_passes_with_five_entries_and_an_empty_unreleased(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = release_ready(Path(tmp))
            self.assertEqual(run(rn, [str(repo), "--check"])[0], 0)

    def test_check_fails_without_the_section_of_the_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), version="0.0.9")
            toy.write(repo, "CHANGELOG.md", "# C\n\n## [Unreleased]\n\n## [0.0.8] - Old\n\n- a\n- b\n- c\n")
            code, out = run(rn, [str(repo), "--check"])
            self.assertEqual(code, 1)
            self.assertIn("no section for the version 0.0.9", out)

    def test_check_fails_when_unreleased_still_holds_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), entries=2)
            code, out = run(rn, [str(repo), "--check"])
            self.assertEqual(code, 1)
            self.assertIn("'## [Unreleased]' still holds 2 entries", out)

    def test_fewer_than_five_entries_is_a_warning_that_can_be_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = toy.make_repo(Path(tmp), entries=0)
            code, out = run(rn, [str(repo), "--check"])
            self.assertEqual(code, 2)
            self.assertIn("WARN the section 0.0.9 has 1 entries", out)
            self.assertEqual(run(rn, [str(repo), "--check", "--allow-short"])[0], 0)


class FakeRunner:
    """Real git, a canned ci_validate and a canned gh."""

    def __init__(self, validate: str = "CI_VALIDATION=PASS", runs: list | None = None, gh_fails: bool = False):
        self.validate, self.runs, self.gh_fails, self.calls = validate, runs, gh_fails, []
        self.remote_tags: tuple[int, str] = (0, "")  # what `git ls-remote --tags` answers; the real remote is never asked

    def __call__(self, cmd: list[str], cwd: Path) -> tuple[int, str]:
        self.calls.append(cmd)
        if cmd[0] == "gh":
            return (1, "not logged in") if self.gh_fails else (0, json.dumps(self.runs or []))
        if cmd[:2] == ["git", "ls-remote"]:
            return self.remote_tags
        if cmd[:2] == [sys.executable, "-I"]:
            return (0 if "PASS" in self.validate else 1), self.validate
        return pc.run(cmd, cwd)


def with_remote(tmp: Path, repo: Path) -> None:
    remote = tmp / "remote.git"
    toy.git(tmp, "init", "--bare", "-b", "main", str(remote))
    toy.git(repo, "init", "-b", "main")
    toy.git(repo, "add", "-A")
    toy.git(repo, "commit", "-m", "start")
    toy.git(repo, "remote", "add", "origin", "https://github.com/Someone/EH3D-TOY.git")
    toy.git(repo, "config", "remote.origin.pushurl", str(remote))
    toy.git(repo, "push", "-u", "origin", "main")


def verdicts(lines: list[str]) -> dict[str, str]:
    return {line.split(":")[0].split()[1]: line.split()[0] for line in lines if ":" in line and line.split()[0] in ("OK", "WARN", "SKIP", "FAIL")}


class PrereleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = release_ready(self.tmp, cargo=True)
        with_remote(self.tmp, self.repo)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def green(self) -> list[dict]:
        return [{"name": "CI", "status": "completed", "conclusion": "success"}]

    def test_a_repository_that_is_ready_passes_every_check(self) -> None:
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertEqual(code, 0, "\n".join(lines))
        self.assertTrue(lines[-1].startswith("PRERELEASE=PASS"))
        self.assertEqual(set(verdicts(lines).values()), {"OK"})
        self.assertEqual(set(verdicts(lines)), {"versions", "changelog", "readmes", "git", "tag", "validate", "ci"})

    def test_a_tag_that_exists_here_or_on_the_remote_fails_and_an_unreachable_remote_only_skips(self) -> None:
        version = pc.vp.manifest_version(pc.vp.Repo(self.repo))
        runner = FakeRunner(runs=self.green())
        runner.remote_tags = (0, f"abc refs/tags/v{version}"+chr(10))
        code, lines = pc.prerelease(self.repo, runner, have_gh=True)
        self.assertEqual((code, verdicts(lines)["tag"]), (1, "FAIL"), chr(10).join(lines))
        runner = FakeRunner(runs=self.green())
        runner.remote_tags = (128, "offline")
        code, lines = pc.prerelease(self.repo, runner, have_gh=True)
        self.assertEqual((code, verdicts(lines)["tag"]), (0, "SKIP"), chr(10).join(lines))
        pc.run(["git", "tag", f"v{version}"], self.repo)
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertEqual((code, verdicts(lines)["tag"]), (1, "FAIL"), chr(10).join(lines))

    def test_a_version_that_one_file_does_not_follow_fails(self) -> None:
        toy.write(self.repo, "Cargo.toml", (self.repo / "Cargo.toml").read_text(encoding="utf-8").replace('version = "0.0.9"', 'version = "0.0.8"', 1))
        toy.git(self.repo, "commit", "-am", "x")
        toy.git(self.repo, "push")
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertEqual(code, 1)
        self.assertTrue(any("Cargo.toml" in line and line.startswith("FAIL") for line in lines), lines)

    def test_a_dirty_tree_and_an_unpushed_commit_fail(self) -> None:
        toy.write(self.repo, "notes.txt", "x")
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertEqual(code, 1)
        self.assertEqual(verdicts(lines)["git"], "FAIL")
        toy.git(self.repo, "add", "notes.txt")
        toy.git(self.repo, "commit", "-m", "more")
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertTrue(any("1 commits are not on the remote" in line for line in lines), lines)

    def test_a_readme_with_other_lights_fails(self) -> None:
        page = (self.repo / "README_deu.md").read_text(encoding="utf-8").replace("| a | \U0001F7E1 |", "| a | \U0001F7E2 |")
        toy.write(self.repo, "README_deu.md", page)
        toy.git(self.repo, "commit", "-am", "x")
        toy.git(self.repo, "push")
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertTrue(any("README_deu.md shows other lights" in line for line in lines), lines)

    def test_a_failed_validator_fails(self) -> None:
        code, lines = pc.prerelease(self.repo, FakeRunner(validate="  FAIL something\nCI_VALIDATION=FAIL"), have_gh=True)
        self.assertEqual(verdicts(lines)["validate"], "FAIL")

    def test_the_ci_of_the_commit_must_exist_and_be_green(self) -> None:
        for runs, expected in (([], "FAIL"), ([{"name": "CI", "status": "in_progress", "conclusion": ""}], "FAIL"),
                               ([{"name": "CI", "status": "completed", "conclusion": "failure"}], "FAIL"), (self.green(), "OK")):
            _, lines = pc.prerelease(self.repo, FakeRunner(runs=runs), have_gh=True)
            self.assertEqual(verdicts(lines)["ci"], expected, runs)

    def test_without_gh_the_ci_is_skipped_and_it_says_so(self) -> None:
        code, lines = pc.prerelease(self.repo, FakeRunner(), have_gh=False)
        self.assertEqual(code, 0, lines)
        self.assertTrue(any(line.startswith("SKIP") and "gh" in line for line in lines), lines)
        _, lines = pc.prerelease(self.repo, FakeRunner(gh_fails=True), have_gh=True)
        self.assertEqual(verdicts(lines)["ci"], "SKIP")

    def test_no_ci_skips_the_question_to_github(self) -> None:
        runner = FakeRunner()
        code, lines = pc.prerelease(self.repo, runner, with_ci=False)
        self.assertEqual(code, 0)
        self.assertFalse(any(call[0] == "gh" for call in runner.calls))

    def test_a_short_changelog_is_a_warning_and_never_fails(self) -> None:
        toy.write(self.repo, "CHANGELOG.md", "# C\n\n## [Unreleased]\n\n## [0.0.9] - T\n\n- one\n")
        toy.git(self.repo, "commit", "-am", "x")
        toy.git(self.repo, "push")
        code, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), have_gh=True)
        self.assertEqual((code, verdicts(lines)["changelog"]), (0, "WARN"))
        _, lines = pc.prerelease(self.repo, FakeRunner(runs=self.green()), allow_short=True, have_gh=True)
        self.assertEqual(verdicts(lines)["changelog"], "OK")


if __name__ == "__main__":
    unittest.main()
