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
