# The release chain, the binaries and what the CI has taught us

[RELEASING.md](RELEASING.md) says how a version is raised and a release is written. This page is the rest of the chain: how the binaries come to exist and are signed, the rules that decide what may be released, and the rules about the CI that the repositories learned the hard way.

## From main to a signed binary

1. **The commit of the release is main.** What is compiled and signed is the commit that is the tip of `main` when the release is made. A release is never made from a side branch, and a tag is never moved to a commit that was compiled without it. A tool that starts a build refuses when the reference it was given is not the tip of main, and a run that was started on a commit that main has left behind fails by design: do not push to main while a release build runs.
2. **The version is raised before anything is compiled.** Firmware, packages and the Android application carry the version inside. After the build, look for the new number inside the binary (a string in the firmware, the version code of the package); a binary with the old number is not a release.
3. **The build is made in GitHub Actions**, never on a development PC, in the workflow of the repository (a desktop program for each operating system, the firmware of each node, the Android package). Heavy builds are run one at a time.
4. **The binaries are downloaded and signed on the machine of the maintainer.** The helper that does it (`fetch_and_sign_eh3d.py`) downloads the artifacts of the run of that exact commit, checks that they are the ones expected for the repository (the list of packages of each repository), writes the SHA-256 of each file and signs it with the key of the releases (OpenSSH signature, namespace `eh3d-release`; the public half is in [RELEASE_KEY.md](RELEASE_KEY.md)). The private key never leaves that machine and never enters a repository.
5. **The release is a draft first**, with the notes of the version, the binaries, the checksums and the signatures; it is published when `tools/verify_release.py` and the check of the signatures pass. Only the newest release of a repository is kept on GitHub; the older ones are deleted and their tags stay.
6. **The tag is annotated and signed.** A release created with a target makes a lightweight tag on the server; create and push the tag first and let the release use it.
7. **The updaters read what the release carries.** A release that has no binary where its workflow promises one is a failure, not a release.

Libraries (COMMON, CORE-LIBS, this hub) and the repositories that are only code (the satellites, the iPhone app) carry no binaries: their release is a tag and the notes. The nodes carry firmware only after the firmware build has run for all the nodes of the group, and the firmware built on a PC is never the one that is signed.

## What may be released

* A repository is released when its work is done, not for each fix: at least five entries in `[Unreleased]` (thirty for the three large design programs), the documents, the counts of tests, the pictures and the screenshots up to date, and no pending item that could be done. An emergency or an explicit decision of the maintainer is the exception.
* The manifest says what is true: `scaffolding`, `functional`, and the evidence `simulator`, `host-test`, `bench` or `field`. The evidence goes up only after a person has tried it, and `bench` and `field` are never set by a script.
* Every release renews the screenshots of the README (taken from the signed binary with its own `--shot`, or from the simulator or the command line for libraries and servers).
* `SUITE_MAP.md` is brought to the published releases (`tools/suite_contract.py --write-map` reads the tags) at the end of each round of releases, and the check of the contract fails when the map is behind a release.

## The lessons of the CI, in short

Each line is a red CI that happened and the rule that prevents it.

* **Run the exact check of the CI before every push**, with the same versions and the same rules (the linter with the same selection of rules, the type checker, `cargo fmt --check` and `cargo clippy -D warnings`, the repository's validator with and without the variable of the CI). Condition the commit on the line that says PASS, not on a pipe.
* **Upload in the order of the dependencies:** the common repository, then the documents, then the server, then the studio and the clients. The shared tools go to every repository in the same batch or the weekly sync check turns red. An API change in a library goes in the same batch as the change of its callers, tried before on a temporary branch.
* **Generated files are generated:** the READMEs, the counts of tests, the tables of error codes, the contract of the settings and the OpenAPI are written by their scripts from their sources; edit the source and run the script. Never edit a generated file by hand, and run the script that updates counts last, because every change of a test changes a count.
* **A new tracked file** is added to `docs/structure.json` (eight languages) and the picture and the tree of the eight READMEs are drawn again.
* **A pull request that changes many things does not touch the READMEs:** the counts are written once, at the end, by one change, or the next pull request conflicts.
* **A test that reads a file that is not in the package, a clock, the network or the speed of the runner is not a test of the CI:** make it skip cleanly or make it deterministic. Wait for a condition, with a limit, never for a fixed number of turns. Temporary files have a name that is unique to the call.
* **A new script of a repository** answers `--help` with exit code 0, a wrong option with 64, and is listed where the tests of the exit codes look.
* **A new workflow cannot be run until it is on the default branch;** a macOS or Windows runner that was not acquired is the infrastructure: rerun, do not edit the code.
* **Binaries and images have a size limit:** the pictures of a README are at most 400 KiB (reduce the palette before uploading) and the SVG pictures are validated and rendered and looked at before they are published.
* **Names that look secret in a test** (password, token, secret) written to a temporary file trip the security scan: use neutral names and build the values at run time.
* **A script that must run on Linux is committed with the executable bit.** Windows does not keep it.
* **A constant has one source:** a port, a version, a language list or a table of codes that is copied is checked against its source by a test, and a change goes to the source first.
* **A red CI of main is fixed or reverted in minutes**, and a new cause of a red CI is written here, with the check that would have caught it.
