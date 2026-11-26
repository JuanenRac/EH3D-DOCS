# The key that signs the releases of EH3D

The programs, the firmware images and the packages of a release are signed with an OpenSSH key (ED25519). This page holds its public half, so that anybody can check a download before running it. The private half never leaves the computer of the owner and is never sent to a build.

* Namespace of the signatures: `eh3d-release`
* Fingerprint: `SHA256:yUsqDokXpCjmjnMQZIe1rTF3a7xAejiP9KhRLI5hqKo`

## The file of allowed signers

Save this single line as `allowed_signers`:

```
eh3d-release ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILidTpyj1I0Eegn/A2tt+ATI9kbY74PhtPxKbQfszYHl
```

## Checking a download

1. The sum: `sha256sum -c <package>.sha256` (Linux and macOS: `shasum -a 256 -c`), or `Get-FileHash <package>` on Windows and compare it with the `.sha256` file.
2. The signature, with the `.sig` file that is published next to the package:

```
ssh-keygen -Y verify -f allowed_signers -I eh3d-release -n eh3d-release -s <package>.sig < <package>
```

The answer must be `Good "eh3d-release" signature`. Any other answer means that the file is not the one that was published: do not run it.

The builds of the programs also carry an attestation of GitHub that ties each file to the workflow and the commit that built it: `gh attestation verify <package> --repo JuanenRac/<repository>`.

The key is changed only with a notice in the changelog of this repository and in the release notes; an older release stays valid with the key it was signed with.

## The record of a release

A signature of a file does not say what the file is, and every repository is signed with this same key. So a release also publishes its record, `eh3d-release.json`, signed the same way (`eh3d-release.json.sig`):

```json
{"format": "eh3d-release", "format_version": 1, "repository": "JuanenRac/<repository>", "version": "X.Y.Z",
 "files": [{"name": "<package>", "arch": "linux-x86_64", "size": 0, "sha256": "..."}]}
```

* Check the record like any file: `ssh-keygen -Y verify -f allowed_signers -I eh3d-release -n eh3d-release -s eh3d-release.json.sig < eh3d-release.json`.
* Check that it names the repository and the version you wanted, and your package with its SHA-256.

`tools/verify_release.py` does all these checks. A release that has a record must be checked against it. The releases published before the record existed have only the `.sig` of each file and stay valid; the tool keeps, for each repository, the last version published without a record, and for any later version a missing record is a failure.
