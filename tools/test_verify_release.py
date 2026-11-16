# =============================================================================
# EH3D-DOCS - tools/test_verify_release.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/verify_release.py: the sum, the signature and the way a folder of packages is judged."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import verify_release as vr


def package(folder: Path, name: str = "tool-1.0.0.zip", data: bytes = b"binary") -> Path:
    path = folder / name
    path.write_bytes(data)
    (folder / (name + ".sha256")).write_text(hashlib.sha256(data).hexdigest() + "  " + name + "\n", encoding="utf-8")
    return path


class SumTests(unittest.TestCase):
    def test_the_sum_is_read_from_the_first_word_and_a_bad_one_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            path = package(folder)
            self.assertEqual(vr.sum_of(path), vr.expected_sum(folder / "tool-1.0.0.zip.sha256"))
            path.write_bytes(b"changed")
            problems = vr.verify_folder(folder, folder / "signers")
            self.assertEqual(len(problems), 1)
            self.assertIn("sum does not match", problems[0])

    def test_a_folder_without_packages_is_a_problem(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            self.assertIn("no package", vr.verify_folder(Path(raw), Path(raw) / "signers")[0])

    def test_a_package_without_a_signature_is_a_problem(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            package(folder)
            problems = vr.verify_folder(folder, folder / "signers")
            self.assertEqual(len(problems), 1)
            self.assertIn("no .sig", problems[0])

    def test_a_wrong_use_exits_with_64_and_the_list_has_twelve_programs(self) -> None:
        self.assertEqual(len(vr.DESKTOP_TOOLS), 12)
        self.assertEqual(vr.main(["--dir", ".", "--signers", "no-such-file"]), 64)


@unittest.skipUnless(shutil.which("ssh-keygen"), "ssh-keygen is not installed")
class SignatureTests(unittest.TestCase):
    def test_a_good_signature_passes_and_another_key_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            keys = []
            for name in ("one", "two"):
                key = folder / name
                subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True)
                keys.append(key)
            pub = (folder / "one.pub").read_text(encoding="utf-8").split()
            (folder / "signers").write_text(f"{vr.NAMESPACE} {pub[0]} {pub[1]}\n", encoding="utf-8")
            work = folder / "release"
            work.mkdir()
            path = package(work)
            subprocess.run(["ssh-keygen", "-Y", "sign", "-q", "-f", str(keys[0]), "-n", vr.NAMESPACE, str(path)], check=True)
            self.assertEqual(vr.verify_folder(work, folder / "signers"), [])
            (work / (path.name + ".sig")).unlink()
            subprocess.run(["ssh-keygen", "-Y", "sign", "-q", "-f", str(keys[1]), "-n", vr.NAMESPACE, str(path)], check=True)
            problems = vr.verify_folder(work, folder / "signers")
            self.assertEqual(len(problems), 1)
            self.assertIn("not a good one", problems[0])


if __name__ == "__main__":
    unittest.main()
