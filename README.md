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
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** documents and two small checks. The suite is at its first steps: eleven repositories are published (EH3D-COMMON, EH3D-CORE-LIBS, EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-BUNGARD-GUI, EH3D-MOTIONCNC, EH3D-SERVER, EH3D-NODE-BUNGARD, EH3D-UPDATER, ELECTRO-HOBBY-3D-UPDATER and this one) and every other program of the suite is a plan. Everything published has been tested on a computer; of the whole suite only the serial protocol of EH3D-DRILLPRO has moved a real machine (the reference run and the moves of each axis on one Bungard CCD MTC), and no whole job has run on a machine yet. 5 tests cover the repository check.

---

> **Safety and security status:** this repository runs nothing on a machine and is not a safety system. A document here never replaces the limits, interlocks and emergency stop of the machine and its controller.

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.1` |
| Maturity | Scaffolding |
| Tests | 5 |
| Stack | Markdown, with two Python 3.10+ checks |
| On real hardware | Not applicable: documentation |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Repository checks | 🟡 | The repository check, the check of the links between the documents and the 5 tests of the repository check run in CI and pass. |
| Tests | 🟠 | Only the repository check has tests (5); the documents and the claims in them are read and checked by hand and by the two scripts. |
| Map and capability matrix | 🟡 | The suite map, the architecture notes and the capability matrix cover the eleven published repositories and list every other program as planned; they are written by hand and can fall behind the repositories. |
| Real hardware | 🟡 | Not applicable: documentation, nothing here runs on hardware. |
| Documentation | 🟡 | README in eight languages, checked against the manifest and the changelog on every change. |

## 🎯 Overview

* **The map of the suite:** every repository, what it is for, and whether it is published or only planned.
* **The architecture:** the two shared libraries, the programs that are meant to depend on them and never on each other, the node and the server that reach the machine, and the rules every repository follows.
* **The capability matrix:** what is tested on a computer and what has been run on a machine (only the protocol of EH3D-DRILLPRO, on one machine), so nobody has to guess.
* **The conventions:** the manifest every repository carries, the repository check and the eight-language README files.
* **Two checks:** the repository check and a check of the links between the documents, both run in CI.

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
| The documents | Markdown: the map, the architecture, the capability matrix and the conventions | [docs/](docs/SUITE_MAP.md) |
| The repository check | `python -I tools/ci_validate.py` prints `CI_VALIDATION=PASS` or lists what fails | `tools/ci_validate.py` |
| The link check | `python -I tools/check_links.py` prints `LINKS=PASS` or lists the broken links | `tools/check_links.py` |
| The tests of the check | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |

## ⚙️ Configuration

There is nothing to configure: the two checks need Python 3.10 or newer and no installation, and they read the files of the repository they live in. The rules they enforce are in the code of `tools/ci_validate.py`:

| Rule | Limit | Where |
|---|---|---|
| Size of a versioned file | at most 1,500,000 bytes | `MAX_TRACKED_BYTES` |
| Languages of the README | eight files, with the same heading structure and the same traffic lights | `LANGUAGES` |
| Manifest fields | the 14 fields of `REQUIRED`; the version of the manifest equals the one in `VERSION` (`native_version`) and in the newest changelog entry | `REQUIRED` |

## 🚀 Quick start

You need Python 3.10 or newer; there is nothing to install.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I -m unittest discover -s tools -p "test_*.py"
```

To read the documents, start with [the map of the suite](docs/SUITE_MAP.md).

## 🧪 Testing

The repository check has 5 tests (`python -I -m unittest discover -s tools -p "test_*.py"`), and they pass. The CI runs the repository check (`tools/ci_validate.py`), the check of the links between the documents (`tools/check_links.py`) and those tests. The documents themselves have no test beyond that: what they claim is kept honest by reading the repositories they describe.

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
│   └── architecture.json structure.json         the data of the two pictures
├── tools/                                       the repository check, the link check, their tests and the picture tools
├── images/                                      banner and the Architecture and Repository Structure pictures
├── .github/                                     CI and release workflows, issue and pull-request templates
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
* Only the published repositories are described in detail; every other program is a line of the map marked as planned.
* The documents have no test of their own beyond the repository check and the link check.

**Next**

* Keep the map and the capability matrix in step with each repository as it is published or changes.
* Check the map against the manifests of the repositories, so that a new repository cannot be missing from it.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): the project container, the machine types and the firmware base of the nodes
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): the readers of Gerber, Excellon and G-code
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) and [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO): the drilling and routing programs
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) and [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC): the modern interface of the Bungard machines, and the machine-control program
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) and [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD): the center of the programs and the node that reaches the machine
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) and [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): install and update the repositories

## 📚 Documentation

* [The map of the suite](docs/SUITE_MAP.md), [the architecture](docs/ARCHITECTURE.md), [the capability matrix](docs/CAPABILITY_MATRIX.md) and [the conventions](docs/CONVENTIONS.md).
* [Changelog](CHANGELOG.md)

## 🤝 Contributing & Community

* Before a pull request run `python -I tools/ci_validate.py`, `python -I tools/check_links.py` and the tests of the check: all must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files, and the two pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`.
* Do not describe as working on a machine what has only been tried on a computer: the capability matrix says which is which.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE). Hardware designs of the suite use CERN OHL-S.
