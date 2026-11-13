# =============================================================================
# EH3D-DOCS - tools/test_changed_paths_workflow.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The reusable workflow .github/workflows/changed-paths.yml, its trial workflow and its guide agree (the text is read)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
GUIDE = ROOT / "docs" / "REUSABLE_VALIDATION.md"


class ChangedPathsWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = (WORKFLOWS / "changed-paths.yml").read_text(encoding="utf-8")
        self.trial = (WORKFLOWS / "test-changed-paths.yml").read_text(encoding="utf-8")
        self.guide = GUIDE.read_text(encoding="utf-8")

    def test_it_only_reads_and_is_bounded(self) -> None:
        self.assertIn("workflow_call:", self.text)
        self.assertNotIn("secrets:", self.text)
        self.assertRegex(self.text, r"(?m)^permissions:\n  contents: read$")
        self.assertRegex(self.text, r"(?m)^    timeout-minutes: \d+$")
        self.assertIn("fetch-depth: 2", self.text)
        self.assertIn("sparse-checkout: .github", self.text)
        self.assertIn("persist-credentials: false", self.text)

    def test_inputs_and_outputs_are_the_documented_ones(self) -> None:
        for name in ("paths", "label"):
            self.assertRegex(self.text, rf"(?m)^      {name}:$")
            self.assertRegex(self.guide, rf"(?m)^\| `{name}` \|")
        for name in ("matched", "reason"):
            self.assertRegex(self.text, rf"(?m)^      {name}:$")
            self.assertRegex(self.guide, rf"(?m)^\| `{name}` \|")
        self.assertRegex(self.text, r"(?ms)paths:\n.*?required: true")

    def test_every_reason_the_engine_gives_is_in_the_guide(self) -> None:
        engine = re.search(r"# engine:begin\n(.*?)# engine:end", self.text, re.S)
        self.assertIsNotNone(engine)
        reasons = set(re.findall(r'answer\((?:True|False), "([a-z-]+)"\)', engine.group(1)))
        self.assertEqual(reasons, {"label", "manual", "unknown-base", "paths", "no-paths"})
        for reason in reasons:
            self.assertIn(f"`{reason}`", self.guide)

    def test_the_engine_does_not_skip_when_it_cannot_tell(self) -> None:
        engine = re.search(r"# engine:begin\n(.*?)# engine:end", self.text, re.S).group(1)
        self.assertEqual(engine.count('answer(True, "unknown-base")'), 2)
        self.assertNotIn("answer(False", engine.split("def main")[0])

    def test_user_text_reaches_the_engine_through_the_environment(self) -> None:
        run = self.text.split("run: |", 1)[1]
        self.assertNotIn("${{", run)

    def test_the_trial_covers_the_cases_and_calls_the_workflow(self) -> None:
        for case in ("pull_request_that_touches", "pull_request_that_does_not_touch", "label_forces_true", "push_that_touches", "manual_and_scheduled", "the_patterns"):
            self.assertIn(case, self.trial)
        self.assertIn("uses: ./.github/workflows/changed-paths.yml", self.trial)
        self.assertRegex(self.trial, r"(?m)^    timeout-minutes: \d+$")


if __name__ == "__main__":
    unittest.main()
