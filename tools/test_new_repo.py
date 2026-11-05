# =============================================================================
# EH3D-DOCS - tools/test_new_repo.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/new_repo.py: the folder it makes passes the checks of the suite. Everything happens in a temporary folder."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_new_repo", TOOLS / "new_repo.py")
NEW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NEW
SPEC.loader.exec_module(NEW)

README_FILES = [file for _code, file, _flag, _label in NEW.LANGUAGES]


class MadeRepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.mkdtemp(prefix="eh3d_new_repo_")
        cls.repo = NEW.create(Path(cls.tmp), "EH3D-NEW-THING", role="library", stack="rust", version="0.0.2", description="A toy library for the tests")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_base_files_are_there(self) -> None:
        for rel in ("eh3d.project.json", "VERSION", "CHANGELOG.md", "LICENSE", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md", ".gitignore",
                    ".github/workflows/ci.yml", ".github/workflows/dashboard-dispatch.yml", ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug-report.yml",
                    ".github/ISSUE_TEMPLATE/config.yml", "docs/architecture.json", "docs/structure.json", "images/architecture.svg", "images/repository-structure.svg",
                    "images/EH3D_NEW_THING_BANNER.svg", "tools/ci_validate.py", "tools/make_structure.py", "tools/make_architecture.py", "tools/_readme_svg.py",
                    "tools/status_lights.py", "tools/universal_readme_check.py", "tools/test_repository.py", *README_FILES):
            self.assertTrue((self.repo / rel).is_file(), rel)

    def test_the_manifest_has_what_was_asked_and_the_version_is_the_same_everywhere(self) -> None:
        manifest = json.loads((self.repo / "eh3d.project.json").read_text(encoding="utf-8"))
        self.assertEqual((manifest["name"], manifest["role"], manifest["stack"], manifest["version"], manifest["maturity"]), ("EH3D-NEW-THING", "library", "rust", "0.0.2", "scaffolding"))
        self.assertEqual((self.repo / "VERSION").read_text(encoding="utf-8").strip(), "0.0.2")
        self.assertIn("## [0.0.2]", (self.repo / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_the_workflow_calls_the_reusable_validation_fixed_to_a_full_commit(self) -> None:
        text = (self.repo / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertRegex(text, r"uses: JuanenRac/EH3D-DOCS/\.github/workflows/validate\.yml@[0-9a-f]{40}\s")
        self.assertIn("run-tool-tests: true", text)
        for line in text.splitlines():
            if "uses: actions/" in line:
                self.assertRegex(line, r"@[0-9a-f]{40} # v", line)

    def test_nothing_of_the_template_is_left_unfilled(self) -> None:
        for path in self.repo.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".yml", ".svg", ".py", ".txt", ""}:
                text = path.read_text(encoding="utf-8", errors="replace")
                self.assertNotIn("@@", text, str(path.relative_to(self.repo)))
                if path.name.startswith("README"):
                    self.assertNotIn("{name}", text)
                    self.assertNotIn("{tests}", text)
                    self.assertNotIn("{version}", text)

    def test_the_readme_files_share_one_structure_and_the_english_one_has_the_description(self) -> None:
        def headings(text: str) -> list[str]:
            return [line.split(" ", 2)[1] for line in text.splitlines() if line.startswith("## ")]

        english = (self.repo / "README.md").read_text(encoding="utf-8")
        self.assertIn("A toy library for the tests", english)
        for name in README_FILES[1:]:
            self.assertEqual(headings((self.repo / name).read_text(encoding="utf-8")), headings(english), name)

    def test_no_light_is_green_because_nothing_ran_on_hardware(self) -> None:
        for name in README_FILES:
            text = (self.repo / name).read_text(encoding="utf-8")
            status = text.split("## 🚦")[1].split("\n## ")[0]
            rows = [line for line in status.splitlines() if line.startswith("| ") and "|---" not in line][1:]
            self.assertEqual(len(rows), 3, name)
            self.assertFalse(any("🟢" in row for row in rows), name)

    def test_it_passes_the_checks_of_the_suite_and_its_own_tests(self) -> None:
        self.assertEqual(NEW.check(self.repo), [])
        result = NEW.run_tool(self.repo, "-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 3 tests", result.stderr)

    def test_the_shared_tools_are_the_code_of_this_hub_with_the_header_of_the_new_repository(self) -> None:
        sync = NEW._sync_module()
        for tool in ("ci_validate.py", "make_structure.py", "make_architecture.py", "_readme_svg.py", "status_lights.py", "universal_readme_check.py"):
            mine = (self.repo / "tools" / tool).read_text(encoding="utf-8")
            self.assertIn("EH3D-NEW-THING - tools/" + tool, mine)
            self.assertEqual(sync.split_header(mine)[1], sync.split_header((TOOLS / tool).read_text(encoding="utf-8"))[1], tool)
        self.assertIn("# canonical: EH3D-DOCS tools", (self.repo / "tools" / "ci_validate.py").read_text(encoding="utf-8"))

    def test_it_leaves_no_caches_behind(self) -> None:
        self.assertEqual(list(self.repo.rglob("__pycache__")), [])


class TemplateTests(unittest.TestCase):
    def test_the_texts_exist_for_the_eight_languages_with_the_same_keys(self) -> None:
        texts = json.loads((NEW.TEMPLATE / "readme_texts.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(texts), sorted(code for code, *_ in NEW.LANGUAGES))
        keys = set(texts["en"])
        for code, body in texts.items():
            self.assertEqual(set(body), keys, code)
            self.assertTrue(all(isinstance(v, str) and v.strip() for v in body.values()), code)

    def test_every_token_of_the_readme_template_has_a_text(self) -> None:
        texts = json.loads((NEW.TEMPLATE / "readme_texts.json").read_text(encoding="utf-8"))
        tokens = set(re.findall(r"@@(\w+)@@", (NEW.TEMPLATE / "README.md.tpl").read_text(encoding="utf-8")))
        computed = {"banner_file", "language_bar", "jump_links", "tree"}
        self.assertEqual(tokens - computed - set(texts["en"]), set())

    def test_the_anchor_is_what_github_makes_of_a_heading(self) -> None:
        self.assertEqual(NEW.anchor("Quick start"), "#-quick-start")
        self.assertEqual(NEW.anchor("Estructura del repositorio"), "#-estructura-del-repositorio")
        self.assertEqual(NEW.anchor("快速开始"), "#-快速开始")


class UsageTests(unittest.TestCase):
    def run_main(self, *argv: str) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = NEW.main(list(argv))
            except SystemExit as stop:
                code = stop.code
        return code, out.getvalue() + err.getvalue()

    def test_a_name_that_is_not_of_the_suite_is_a_wrong_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("new-thing", "EH3D-", "EH3D-lower", "OTHER-THING", "../EH3D-X"):
                self.assertEqual(self.run_main(name, "--dest", tmp)[0], 64, name)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_a_wrong_role_or_version_is_a_wrong_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main("EH3D-X", "--dest", tmp, "--role", "wizard")[0], 64)
            self.assertEqual(self.run_main("EH3D-X", "--dest", tmp, "--version", "1.0")[0], 64)

    def test_an_existing_folder_is_never_written_into(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "EH3D-X").mkdir()
            (Path(tmp) / "EH3D-X" / "mine.txt").write_text("keep", encoding="utf-8")
            code, text = self.run_main("EH3D-X", "--dest", tmp)
            self.assertEqual(code, 1)
            self.assertIn("nothing was written", text)
            self.assertEqual([p.name for p in (Path(tmp) / "EH3D-X").iterdir()], ["mine.txt"])

    def test_the_command_makes_a_folder_that_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, text = self.run_main("EH3D-TOY-ONE", "--dest", tmp)
            self.assertEqual(code, 0, text)
            self.assertIn("NEW_REPO=PASS", text)


if __name__ == "__main__":
    unittest.main()
