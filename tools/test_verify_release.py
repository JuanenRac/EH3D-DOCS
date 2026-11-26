# =============================================================================
# EH3D-DOCS - tools/test_verify_release.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/verify_release.py: the sum, the signature and the way a folder of packages is judged."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import verify_release as vr


def package(folder: Path, name: str = "eh3d-autolevel-0.1.0-linux-x86_64.tar.gz", data: bytes = b"binary") -> Path:
    path = folder / name
    path.write_bytes(data)
    (folder / (name + ".sha256")).write_text(hashlib.sha256(data).hexdigest() + "  " + name + "\n", encoding="utf-8")
    return path


class SumTests(unittest.TestCase):
    def test_the_sum_is_read_from_the_first_word_and_a_bad_one_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            path = package(folder)
            self.assertEqual(vr.sum_of(path), vr.expected_sum(folder / (path.name + ".sha256")))
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

    def test_the_release_of_a_file_is_read_from_its_name(self) -> None:
        for name, expected in (
            ("eh3d-server-0.2.6-linux-aarch64.tar.gz", ("EH3D-SERVER", "0.2.6")),
            ("routepro-0.1.9-console-windows-x86.zip", ("EH3D-ROUTEPRO", "0.1.9")),
            ("bungard-gui-0.3.1-macos-arm64.tar.gz", ("EH3D-BUNGARD-GUI", "0.3.1")),
            ("eh3d-node-bungard-aux-0.1.1-s3-eth-app.bin", ("EH3D-NODE-BUNGARD-AUX", "0.1.1")),
            ("eh3d-studio-0.8.0.1.tar.gz", ("EH3D-STUDIO", "0.8.0.1")),
            ("EH3D-ANDROID-CONTROL-release.apk", ("EH3D-ANDROID-CONTROL", None)),
            ("tool.zip", (None, None)),
        ):
            self.assertEqual(vr.release_of(name), expected, name)

    def test_a_version_later_than_the_last_one_without_a_record_needs_it(self) -> None:
        for repo, floor in vr.LAST_WITHOUT_RECORD.items():
            self.assertFalse(vr.needs_record(repo, floor), repo)
            self.assertFalse(vr.needs_record(repo, "0.0.1"), repo)
            self.assertTrue(vr.needs_record(repo, floor + ".1"), repo)
            self.assertTrue(vr.needs_record(repo, "1.0.0"), repo)
        self.assertTrue(vr.needs_record("EH3D-NEW-PROGRAM", "0.0.1"))
        self.assertTrue(vr.needs_record("EH3D-SERVER", "nightly"))
        self.assertTrue(set(vr.DESKTOP_TOOLS) <= set(vr.LAST_WITHOUT_RECORD))

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


@unittest.skipUnless(shutil.which("ssh-keygen"), "ssh-keygen is not installed")
class RecordTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.key = self._key("release")
        pub = (self.root / "release.pub").read_text(encoding="utf-8").split()
        self.signers = self.root / "signers"
        self.signers.write_text(f"{vr.NAMESPACE} {pub[0]} {pub[1]}\n", encoding="utf-8")
        self.work = self.root / "release-folder"
        self.work.mkdir()

    def _key(self, name: str) -> Path:
        key = self.root / name
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
        return key

    def _sign(self, path: Path, key: Path | None = None) -> None:
        path.with_name(path.name + ".sig").unlink(missing_ok=True)
        subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(key or self.key), "-n", vr.NAMESPACE, str(path)], check=True, capture_output=True)

    def _package(self, version: str = "0.1.3", signed: bool = True) -> Path:
        path = package(self.work, f"eh3d-autolevel-{version}-linux-x86_64.tar.gz")
        if signed:
            self._sign(path)
        return path

    def _record(self, path: Path, key: Path | None = None, sign: bool = True, version: str = "0.1.3", repository: str = "JuanenRac/EH3D-AUTOLEVEL", **entry) -> None:
        listed = {"name": path.name, "arch": "linux-x86_64", "size": path.stat().st_size, "sha256": vr.sum_of(path), **entry}
        record = self.work / vr.RECORD
        record.write_text(json.dumps({"format": "eh3d-release", "format_version": 1, "repository": repository, "version": version, "files": [listed]}), encoding="utf-8")
        record.with_name(record.name + ".sig").unlink(missing_ok=True)
        if sign:
            self._sign(record, key)

    def _problems(self, **expected) -> str:
        return " | ".join(vr.verify_folder(self.work, self.signers, **expected))

    def test_a_later_version_passes_only_with_a_good_record(self) -> None:
        path = self._package()
        self.assertIn("is published with eh3d-release.json", self._problems())
        self._record(path)
        self.assertEqual(self._problems(), "")
        self.assertEqual(self._problems(repo="EH3D-AUTOLEVEL", version="0.1.3"), "")
        self._record(path, sign=False)
        self.assertIn("eh3d-release.json: no .sig", self._problems())
        self._record(path, key=self._key("thief"))
        self.assertIn("not a good one", self._problems())
        self._record(path)
        (self.work / vr.RECORD).unlink()
        self.assertIn("eh3d-release.json.sig is here", self._problems())

    def test_the_record_must_agree_with_the_files_the_repository_and_the_version(self) -> None:
        path = self._package()
        for change, said in (
            ({"sha256": "0" * 64}, "not the file"),
            ({"name": "another.zip"}, "does not name it"),
            ({"version": "0.1.4"}, "named for the version 0.1.3"),
            ({"repository": "JuanenRac/EH3D-ISOCAM"}, "named for EH3D-AUTOLEVEL"),
        ):
            self._record(path, **change)
            self.assertIn(said, self._problems(), change)
        self._record(path)
        self.assertIn("not of 0.1.4", self._problems(version="0.1.4"))
        self.assertIn("not of JuanenRac/EH3D-ISOCAM", self._problems(repo="EH3D-ISOCAM"))
        record = self.work / vr.RECORD
        record.write_text("[]", encoding="utf-8")
        self._sign(record)
        self.assertIn("not a record", self._problems())

    def test_an_earlier_release_with_only_signatures_passes_and_its_version_is_checked(self) -> None:
        self._package("0.1.2")
        self.assertEqual(self._problems(), "")
        self.assertEqual(self._problems(repo="EH3D-AUTOLEVEL", version="0.1.2"), "")
        # an old package published as a newer release is not the release it is published as
        self.assertIn("named for the version 0.1.2, not for 0.1.5", self._problems(repo="EH3D-AUTOLEVEL", version="0.1.5"))
        self.assertIn("named for EH3D-AUTOLEVEL, not for EH3D-ISOCAM", self._problems(repo="EH3D-ISOCAM", version="0.1.2"))

    def test_an_application_package_is_signed_by_the_record(self) -> None:
        path = package(self.work, "EH3D-ANDROID-CONTROL-release.apk")
        self.assertIn("no .sig", self._problems())
        self._record(path, repository="JuanenRac/EH3D-ANDROID-CONTROL", version="0.1.8", arch="android")
        self.assertEqual(self._problems(repo="EH3D-ANDROID-CONTROL", version="0.1.8"), "")
        self.assertIn("not of 0.1.9", self._problems(repo="EH3D-ANDROID-CONTROL", version="0.1.9"))


if __name__ == "__main__":
    unittest.main()
