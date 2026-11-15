# =============================================================================
# EH3D-DOCS - tools/test_make_release_sbom.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/make_release_sbom.py and the reusable workflow .github/workflows/supply-chain.yml (no YAML library: the text is read)."""
from __future__ import annotations

import hashlib
import json
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import make_release_sbom as sbom

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "supply-chain.yml"
TEST_WORKFLOW = ROOT / ".github" / "workflows" / "supply-chain-test.yml"
GUIDE = ROOT / "docs" / "REUSABLE_VALIDATION.md"


def run(argv: list[str]) -> tuple[int, str]:
    out, err = StringIO(), StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = sbom.main(argv)
    return code, out.getvalue() + err.getvalue()


class BillTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.files = self.dir / "files"
        self.files.mkdir()
        (self.files / "b.bin").write_bytes(b"bbb")
        (self.files / "a.txt").write_bytes(b"aaa")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_it_lists_every_file_with_its_sha256_sorted_by_name(self) -> None:
        out = self.dir / "sbom.json"
        code, _ = run(["--name", "demo", "--version", "1.0.0", "--out", str(out), str(self.files)])
        self.assertEqual(code, 0)
        bom = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual((bom["bomFormat"], bom["specVersion"]), ("CycloneDX", "1.5"))
        self.assertEqual([c["name"] for c in bom["components"]], ["a.txt", "b.bin"])
        self.assertEqual(bom["components"][0]["hashes"], [{"alg": "SHA-256", "content": hashlib.sha256(b"aaa").hexdigest()}])
        self.assertEqual(bom["metadata"]["component"]["version"], "1.0.0")
        self.assertNotIn("timestamp", bom["metadata"])

    def test_the_same_files_give_the_same_bytes(self) -> None:
        one, two = self.dir / "one.json", self.dir / "two.json"
        for target in (one, two):
            self.assertEqual(run(["--name", "demo", "--version", "1.0.0", "--out", str(target), str(self.files)])[0], 0)
        self.assertEqual(one.read_bytes(), two.read_bytes())

    def test_a_changed_file_changes_the_serial_number(self) -> None:
        one, two = self.dir / "one.json", self.dir / "two.json"
        run(["--name", "demo", "--version", "1.0.0", "--out", str(one), str(self.files)])
        (self.files / "a.txt").write_bytes(b"changed")
        run(["--name", "demo", "--version", "1.0.0", "--out", str(two), str(self.files)])
        self.assertNotEqual(json.loads(one.read_text())["serialNumber"], json.loads(two.read_text())["serialNumber"])

    def test_the_output_inside_the_folder_is_not_listed(self) -> None:
        out = self.files / "sbom.cdx.json"
        self.assertEqual(run(["--name", "demo", "--version", "1", "--out", str(out), str(self.files)])[0], 0)
        self.assertEqual(len(json.loads(out.read_text())["components"]), 2)

    def test_a_missing_path_or_an_empty_folder_fails(self) -> None:
        out = self.dir / "x.json"
        self.assertEqual(run(["--name", "d", "--version", "1", "--out", str(out), str(self.dir / "nope")])[0], 64)
        empty = self.dir / "empty"
        empty.mkdir()
        self.assertEqual(run(["--name", "d", "--version", "1", "--out", str(out), str(empty)])[0], 1)

    def test_two_files_with_one_name_fail(self) -> None:
        other = self.dir / "other"
        other.mkdir()
        (other / "a.txt").write_bytes(b"x")
        code, text = run(["--name", "d", "--version", "1", "--out", str(self.dir / "x.json"), str(self.files / "a.txt"), str(other / "a.txt")])
        self.assertEqual(code, 64)
        self.assertIn("a.txt", text)


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def jobs(self) -> dict[str, str]:
        body = self.text.split("\njobs:\n", 1)[1]
        parts = re.split(r"(?m)^  ([a-z-]+):\n", body)
        return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}

    def test_it_is_off_by_default(self) -> None:
        block = re.search(r"(?ms)^      enabled:\n(.*?)^      \w", self.text).group(1)
        self.assertIn("type: boolean", block)
        self.assertIn("default: false", block)
        for name, job in self.jobs().items():
            self.assertRegex(job, r"(?m)^    if: \$\{\{ inputs\.enabled\b", name)

    def test_the_default_permission_only_reads_and_the_signing_ones_are_in_one_job(self) -> None:
        self.assertRegex(self.text, r"(?m)^permissions:\n  contents: read\n\njobs:")
        holders = [name for name, job in self.jobs().items() if "id-token: write" in job]
        self.assertEqual(holders, ["attest"])
        self.assertEqual([name for name, job in self.jobs().items() if "attestations: write" in job], ["attest"])
        self.assertEqual([name for name, job in self.jobs().items() if "contents: write" in job], ["attach"])

    def test_every_action_is_pinned_to_a_full_commit_with_the_version_in_a_comment(self) -> None:
        for path in (WORKFLOW, TEST_WORKFLOW):
            uses = re.findall(r"(?m)^\s*(?:- )?uses: (\S+)(.*)$", path.read_text(encoding="utf-8"))
            self.assertTrue(uses, path.name)
            for target, rest in uses:
                if target.startswith("./"):
                    continue
                self.assertRegex(target, r"@[0-9a-f]{40}$", f"{path.name}: {target}")
                self.assertRegex(rest, r"# v\d+\.\d+\.\d+", f"{path.name}: {target}")

    def test_every_job_has_a_timeout_and_the_inputs_are_used(self) -> None:
        for name, job in self.jobs().items():
            self.assertIn("timeout-minutes:", job, name)
        for name in re.findall(r"(?m)^      ([a-z-]+):\n        description", self.text):
            self.assertIn(f"inputs.{name}", self.text, name)

    def test_inputs_reach_the_shell_through_the_environment_only(self) -> None:
        run_blocks = re.findall(r"(?ms)^        run: [|>]?.*?(?=^      - |\Z)", self.text)
        for block in run_blocks:
            self.assertNotIn("${{", block)

    def test_the_bill_is_attached_to_a_draft_only(self) -> None:
        attach = self.jobs()["attach"]
        self.assertIn("inputs.attach-to-release", attach)
        self.assertIn(".draft == true", attach)

    def test_the_test_workflow_keeps_it_off_unless_started_by_hand(self) -> None:
        test = TEST_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("uses: ./.github/workflows/supply-chain.yml", test)
        self.assertIn("enabled: ${{ github.event_name == 'workflow_dispatch' && inputs.exercise }}", test)
        self.assertRegex(test, r"(?ms)exercise:.*?default: false")
        self.assertIn("attach-to-release: false", test)

    def test_the_guide_documents_the_inputs_and_the_switch(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        self.assertIn("The supply-chain workflow", guide)
        for name in re.findall(r"(?m)^      ([a-z-]+):\n        description", self.text):
            self.assertRegex(guide, r"(?m)^\| `%s` \|" % re.escape(name), name)


if __name__ == "__main__":
    unittest.main()
