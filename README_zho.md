<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### EH3D Fabrication Suite 的地图、架构和如实的现状：每个仓库的用途、哪些已测试、哪些还没有在机器上运行过

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天有什么：** 文档和两个小检查。套件处于起步阶段：已发布三个仓库（带项目容器的 EH3D-COMMON、带 Gerber、Excellon 和 G-code 读取器的 EH3D-CORE-LIBS，以及 EH3D-UPDATER），套件中的每个程序都只是计划。已发布的内容都在电脑上测试过；没有任何东西在机器上运行过。

---

> **安全（safety）与信息安全状态：** 本仓库不在任何机器上运行任何东西，也不是安全系统。这里的文档绝不能取代机器及其控制器的限位、联锁和紧急停止。

## 📋 概览

| | |
|---|---|
| 版本 | `0.0.1` |
| 成熟度 | 脚手架 |
| 技术栈 | Markdown / Python 3.10+（检查脚本） |
| 真实硬件 | 不适用：文档 |

## 🎯 概述

* **套件地图：** 每个仓库、它的用途，以及它是已发布还是仅为计划。
* **架构：** 两个共享库、依赖它们且彼此从不依赖的程序，以及每个仓库遵循的规则。
* **能力矩阵：** 哪些在电脑上测试过、哪些在机器上运行过（目前没有），免得有人去猜。
* **约定：** 每个仓库携带的清单、仓库检查，以及八种语言的 README。
* **两个检查：** 仓库检查和文档之间的链接检查，都在 CI 中运行。

## 📂 仓库结构

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

## 🛠️ 构建与运行

需要 Python 3.10 或更新版本；无需安装任何东西。

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 相关项目

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): 项目容器和机器类型
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): Gerber、Excellon 和 G-code 的读取库
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): 安装并更新套件的仓库

## 📚 文档与社区

* [套件地图](docs/SUITE_MAP.md)、[架构](docs/ARCHITECTURE.md)、[能力矩阵](docs/CAPABILITY_MATRIX.md)和[约定](docs/CONVENTIONS.md)（英文）。
* [贡献指南](CONTRIBUTING.md)、[安全政策](SECURITY.md)、[支持](SUPPORT.md)和[行为准则](CODE_OF_CONDUCT.md)。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later。参见 [LICENSE](LICENSE)。
