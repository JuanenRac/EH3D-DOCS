<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### The map, the architecture and the honest status of the EH3D Fabrication Suite: what each repository is for, what has been tested and what has not been run on a machine yet

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** documents and the tools of the suite, which run on a computer and nowhere else (the repository check and the drawers of the pictures that every repository carries, the contract between the repositories, the scripts that raise a version and prepare a release, the script that sets up a workspace and the one that makes a new repository). The suite is at its first steps: twenty-seven repositories are published (the libraries, the Bungard programs, the server and Studio, the nodes and touch screens, the phone apps, the CAM and utility programs, the updaters and this one), two have started with code and tests and no release (the main project of electronic design and its test laboratory) and eleven are only planned (the pendant for small touch screens and ten repositories of the electronic design project and its bridges). Everything published has been tested on a computer, and the interfaces speak 37 languages; of the whole suite only the serial protocol of EH3D-DRILLPRO has moved a real machine (the reference run and the moves of each axis on one Bungard CCD MTC), and no whole job has run on a machine yet. 14 tests cover the repository check.

---

> **Safety and security status:** this repository runs nothing on a machine and is not a safety system. A document here never replaces the limits, interlocks and emergency stop of the machine and its controller.

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.6` |
| Maturity | Functional |
| Tests | 151 |
| Stack | Markdown, with Python 3.10+ tools |
| On real hardware | Not applicable: documentation |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Repository checks | 🟡 | The repository check, the check of the links between the documents and the tests of the tools run in CI and pass. |
| Tests | 🟠 | 151 tests of the tools pass on a computer, some of them on small toy repositories; the documents and the claims in them are read and checked by hand and by the scripts. |
| Suite contract | 🟡 | The contract between the repositories reads every manifest with the parser of the Updater and warns about drift (ports, README languages, shared tools, issue forms); it runs every day in CI as a warning, and the repositories it names are brought up to date one by one. |
| Version and release tools | 🟠 | The scripts that raise a version, write the notes and check a release, and the reusable validation workflow, are tested on toy repositories; no repository has published a release with them yet. |
| Workspace and new repositories | 🟠 | The scripts that list and clone what a repository needs and that make a new repository are tested on toy repositories in a temporary folder; neither has set up a real workspace or created a real repository yet. |
| Map and capability matrix | 🟡 | The suite map, the architecture notes and the capability matrix cover the forty repositories: the twenty-seven published ones with the release of each, two started ones (code with tests and no release) and eleven planned ones (a written scope and no code); they are written by hand and can fall behind the repositories. |
| Real hardware | 🟡 | Not applicable: documentation, nothing here runs on hardware. |
| Documentation | 🟡 | README in eight languages, checked against the manifest and the changelog on every change. |

## 🎯 Overview

* **The map of the suite:** every repository, what it is for, and whether it is published, started (code with tests and no release yet) or only planned.
* **The architecture:** the two shared libraries, the programs that are meant to depend on them and never on each other, the node and the server that reach the machine, and the rules every repository follows.
* **The capability matrix:** what is tested on a computer and what has been run on a machine (only the protocol of EH3D-DRILLPRO, on one machine), so nobody has to guess.
* **The conventions:** the manifest every repository carries, the repository check and the eight-language README files.
* **The checks and the tools:** the repository check, the check of the links between the documents, the drawers of the two README pictures and the status lights, copied into every repository from this one (`tools/sync_shared_tools.py` says who is behind), and the checker of the exit-code convention; `banner_check.py` checks that the text of each banner says what the manifest says, and `docs/vendored.lock` records the origin and the version of every shared tool.
* **The suite contract:** `tools/suite_contract.py` checks the relations that no repository can check by itself: every manifest is readable with the parser of the Updater and carries the name of its folder, a dependency on a sibling by path says which version it needs, the versions of the map are the manifests', the screens and the server agree on the port, the shared validator is the same everywhere, `docs/suite.json` matches the places that repeat its values, and every repository has the issue forms. It only warns.
* **Versions, releases and new work:** `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py` and `vendored_tools_report.py` ([docs/RELEASING.md](docs/RELEASING.md)), a reusable validation workflow ([docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)), `bootstrap_workspace.py` to fetch what a repository needs and `new_repo.py` to make a new repository. `bump_version.py` also raises the internal dependencies that ask for a minimum version, the `Cargo.lock` entries of the packages of a workspace and the manifest of the updater of the whole family.
* **How it is updated:** the CM5 of the workshop is updated **by releases** (`deploy/eh3d-update.py` of EH3D-SERVER downloads the release of GitHub into `/opt`); EH3D-UPDATER is for **development PCs, by git** ([docs/UPDATING.md](docs/UPDATING.md)).

## 🧩 Role in EH3D

EH3D-DOCS is where the suite is described as a whole. Each repository describes itself in its own README; this one says how they fit together, which exist, and what has really been run.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="EH3D-DOCS architecture: who uses it, what it holds and what it depends on" width="100%">
</p>

How the parts of this repository fit together: who uses it, what it holds and what it depends on. The picture is drawn from `docs/architecture.json` and checked against the code.

## 🔒 Security & Safety

This repository has no program that takes input from outside; what it defends is the accuracy and the cleanliness of what it publishes.

| Threat | Defense |
|---|---|
| A claim that the suite does more than it does | the capability matrix separates "tested on a computer" from "run on a machine", and a repository is listed as planned until it has code that anybody can run |
| A private reference, a person or a tool that must not be public | `tools/ci_validate.py` fails on the words that must never appear in a public file, in every text file |
| A broken link between the documents | `tools/check_links.py` fails when a relative link of a Markdown file points at a file that does not exist |
| One README language drifting from the others | the check compares the heading structure, the traffic lights of Project status and the version in the eight files |
| Files that must not be versioned (builds, keys, logs, big files) | the repository check refuses tracked build folders, private folders, key and log files, and files over 1.5 MB |

## 🔌 Interfaces

| Interface | What it is | Where |
|---|---|---|
| The documents | Markdown: the map, the architecture, the capability matrix, the conventions and the guides to updating and releasing | [docs/](docs/SUITE_MAP.md) |
| The repository check | `python -I tools/ci_validate.py` prints `CI_VALIDATION=PASS` or lists what fails | `tools/ci_validate.py` |
| The link check | `python -I tools/check_links.py` prints `LINKS=PASS` or lists the broken links | `tools/check_links.py` |
| The tests of the check | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| The suite contract | `python -I tools/suite_contract.py --workspace ..` prints `SUITE_CONTRACT=PASS` or lists the findings; `--write-map` puts the manifest versions in the map | `tools/suite_contract.py` |
| The shared tools | `python -I tools/sync_shared_tools.py` says which repositories hold a different copy | `tools/sync_shared_tools.py` |
| Versions and releases | `bump_version.py`, `release_notes.py`, `prerelease_check.py`, `readme_staleness.py`, `vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| The reusable workflow | validation with `on: workflow_call`, for the repositories to call | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| The workspace | `bootstrap_workspace.py` lists and clones what a repository needs; `new_repo.py` makes a new repository | `tools/bootstrap_workspace.py`, `tools/new_repo.py` |
| The exit codes | `0`, `1`, `2`, `10` and `64`; `exit_conventions.py` checks the tools against them | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ Configuration

The tools need Python 3.10 or newer and no installation, and they read the files of the repository they live in. The rules they enforce are in the code of `tools/ci_validate.py`, and the values of the suite that several repositories repeat are in `docs/suite.json`:

| Rule | Limit | Where |
|---|---|---|
| Size of a versioned file | at most 1,500,000 bytes | `MAX_TRACKED_BYTES` |
| Languages of the README | eight files, with the same heading structure and the same traffic lights | `LANGUAGES` |
| Manifest fields | the 14 fields of `REQUIRED`; the version of the manifest equals the one in `VERSION` (`native_version`) and in the newest changelog entry | `REQUIRED` |
| The constants of the suite | the port of the server, the manifest schema, the eight README languages, the rpm field, the shape of a version, the issue forms | `docs/suite.json` |
| Known exceptions of the contract | one `check repository` per line, removed when the cause is fixed | `docs/suite_contract_allow.txt` |
| What a repository adds to the check | for example the folders the scan for forbidden words skips | `tools/ci_config.json` of each repository |

## 🚀 Quick start

You need Python 3.10 or newer; there is nothing to install.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

To read the documents, start with [the map of the suite](docs/SUITE_MAP.md).

## 🧪 Testing

The tools have 151 tests (`python -I -m unittest discover -s tools -p "test_*.py"`), and they pass. The CI runs the repository check (`tools/ci_validate.py`), the check of the links between the documents (`tools/check_links.py`), the checks of the two pictures and those tests; a daily workflow runs the suite contract. The documents themselves have no test beyond that: what they claim is kept honest by the capability matrix and by reading them.

## 🏗️ Build & Release

The version lives in the `VERSION` file and in `eh3d.project.json`, and each version has its entry in [CHANGELOG.md](CHANGELOG.md). There is nothing to build; releases are published on GitHub.

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of EH3D-DOCS" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             every repository and whether it exists yet
│   ├── ARCHITECTURE.md                          the layers and the rules
│   ├── CAPABILITY_MATRIX.md                     what has been tested and what has been run on a machine
│   ├── CONVENTIONS.md                           the manifest, the check, the README files
│   ├── UPDATING.md                              how the CM5 and a PC are updated
│   ├── RELEASING.md                             raise a version and publish a release with the scripts
│   ├── REUSABLE_VALIDATION.md                   the validation workflow that the repositories can call
│   ├── VENDORED_TOOLS_REPORT.md                 the tools copied into the repositories that nothing uses
│   ├── suite.json                               the constants of the suite
│   ├── suite_contract_allow.txt                 the known exceptions of the contract
│   ├── templates/                               the template of a new repository
│   └── architecture.json structure.json         the data of the two pictures
├── tools/                                       the checks, the contract, the version and release scripts, and their tests
├── registry/                                    the registry of container codes (EH3D-PKG) and its coherence test
├── images/                                      banner and the Architecture and Repository Structure pictures
├── .github/                                     CI and dashboard workflows, issue and pull-request templates
├── eh3d.project.json                            manifest: version, role, maturity and build command
├── VERSION                                      the version of the documents
├── CHANGELOG.md                                 what changed in each version
├── SECURITY.md SUPPORT.md                       how to report a vulnerability and where to ask
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   how to contribute, the code of conduct and the licence
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* The map, the architecture notes and the capability matrix are written by hand; nothing checks them against the manifests of the repositories, so they can fall behind.
* Only the published repositories are described in detail; the programs that have started and the planned ones are a line of the map each, marked as such.
* The documents have no test of their own beyond the repository check and the link check.
* The release, workspace and new-repository scripts have been tried on toy repositories only; none has been used for a real release or to create a real repository yet.
* The suite contract only warns, and several repositories still hold an older copy of the shared validator.

**Next**

* Keep the map and the capability matrix in step with each repository as it is published or changes.
* Check the map against the manifests of the repositories, so that a new repository cannot be missing from it.
* Use the scripts for the next real release, adopt the reusable workflow in the repositories, and make the suite contract blocking once its known findings are gone.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): the project container, the machine types and the firmware base of the nodes
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): the readers of Gerber, Excellon and G-code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) and [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO): the drilling and routing programs
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) and [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC): the modern interface of the Bungard machines, and the machine-control program
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) and [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD): the center of the programs and the node that reaches the machine
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO), [EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) and [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX): the configuration panel of the server (with its updates from GitHub), the touch screen of the machine, and the node of the drill head (camera as RTSP and ONVIF, laser that measures the table, speed and temperature of the spindle)
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) and [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): install and update the repositories
* [EH3D-PHOENIX-PCB](https://github.com/JuanenRac/EH3D-PHOENIX-PCB) and the eleven other repositories of the electronic design project and its bridges (the laboratory, the verifier, the thermal laboratory, the adapter to HYDRA-UMC): started or planned, with no release yet

## 📚 Documentation

* [The map of the suite](docs/SUITE_MAP.md), [the architecture](docs/ARCHITECTURE.md), [the capability matrix](docs/CAPABILITY_MATRIX.md) and [the conventions](docs/CONVENTIONS.md).
* [Releasing a version](docs/RELEASING.md), [how the machines are kept up to date](docs/UPDATING.md) and [the reusable validation](docs/REUSABLE_VALIDATION.md).
* [Changelog](CHANGELOG.md)

## 🤝 Contributing & Community

* Before a pull request run `python -I tools/ci_validate.py`, `python -I tools/check_links.py` and the tests of the tools: all must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files, and the two pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`.
* Do not describe as working on a machine what has only been tried on a computer: the capability matrix says which is which.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE). Hardware designs of the suite use CERN OHL-S.
