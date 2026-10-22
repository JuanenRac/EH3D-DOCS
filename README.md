<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### The map, the architecture and the honest status of the EH3D Fabrication Suite: what each repository is for, what has been tested and what has not been run on a machine yet

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what is here today:** documents and two small checks. The suite itself is at its first steps: three repositories are published (EH3D-COMMON with the project container, EH3D-CORE-LIBS with readers for Gerber, Excellon and G-code, and EH3D-UPDATER) and every program of the suite is a plan. Everything published has been tested on a computer; nothing has been run on a machine.

---

> **Safety and security status:** this repository runs nothing on a machine and is not a safety system. A document here never replaces the limits, interlocks and emergency stop of the machine and its controller.

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.1` |
| Maturity | Scaffolding |
| Stack | Markdown / Python 3.10+ (the checks) |
| On real hardware | Not applicable: documentation |

## 🎯 Overview

* **The map of the suite:** every repository, what it is for, and whether it is published or only planned.
* **The architecture:** the two shared libraries, the programs that depend on them and never on each other, and the rules every repository follows.
* **The capability matrix:** what is tested on a computer and what has been run on a machine (nothing yet), so nobody has to guess.
* **The conventions:** the manifest every repository carries, the repository check and the eight-language README files.
* **Two checks:** the repository check and a check of the links between the documents, both run in CI.

## 📂 Repository Structure

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md          every repository of the suite and whether it exists yet
│   ├── ARCHITECTURE.md       the layers and the rules
│   ├── CAPABILITY_MATRIX.md  what has been tested and what has been run on a machine
│   └── CONVENTIONS.md        the manifest, the check, the README files
├── tools/
│   ├── ci_validate.py        the repository check
│   └── check_links.py        the links between the documents
├── eh3d.project.json         the manifest of the project
└── VERSION
```

## 🛠️ BUILD & RUN

You need Python 3.10 or newer; there is nothing to install.

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 Related Projects

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): the project container and the machine types
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): the readers of Gerber, Excellon and G-code
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): installs and updates the repositories of the suite

## 📚 Documentation & Community

* [The map of the suite](docs/SUITE_MAP.md), [the architecture](docs/ARCHITECTURE.md), [the capability matrix](docs/CAPABILITY_MATRIX.md) and [the conventions](docs/CONVENTIONS.md).
* [Contributing](CONTRIBUTING.md), [Security policy](SECURITY.md), [Support](SUPPORT.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE).
