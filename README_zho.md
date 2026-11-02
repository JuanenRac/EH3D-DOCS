<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### EH3D Fabrication Suite 的地图、架构和如实的现状：每个仓库的用途、已测试的内容，以及尚未在机床上运行的内容

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.5-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实性核对 - 今天真正能运行的内容：** 文档和套件的工具，它们只在计算机上运行（每个仓库都带的仓库检查和图片绘制工具、仓库之间的契约、提升版本并准备发布的脚本、准备工作区的脚本，以及创建新仓库的脚本）。套件处于最初阶段：已发布二十七个仓库（库、Bungard 程序、服务器和 Studio、节点和触摸屏、手机应用、CAM 和实用程序、更新器以及本仓库），只有用于小型触摸屏的手持控制器仍然只是计划。已发布的内容都在计算机上测试过，界面支持 37 种语言；整个套件中只有 EH3D-DRILLPRO 的串行协议让真实机床动过（在一台 Bungard CCD MTC 上做了参考运行和各轴运动），还没有任何完整作业在机床上运行过。5 个测试覆盖仓库检查。

---

> **安全（safety）与信息安全现状：** 本仓库不在机床上运行任何东西，也不是安全系统（safety）。这里的任何文档都绝不能取代机床及其控制器的限位、联锁和急停。

## 📋 速览

| | |
|---|---|
| 版本 | `0.0.5` |
| 成熟度 | 脚手架 |
| 测试 | 126 |
| 技术栈 | Markdown，附带 Python 3.10+ 工具 |
| 真实硬件 | 不适用：文档 |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [快速开始](#-快速开始) · [测试](#-测试) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 仓库检查 | 🟡 | 仓库检查、文档之间的链接检查以及工具的测试都在 CI 中运行并通过。 |
| 测试 | 🟠 | 工具的 126 个测试在计算机上通过，其中一些在小型玩具仓库上运行；文档及其中的说法靠手工和脚本阅读与核对。 |
| 套件契约 | 🟡 | 仓库之间的契约用 Updater 的解析器读取每个清单，并对偏差发出警告（端口、README 语言、共享工具、问题表单）；它每天在 CI 中作为警告运行，被点名的仓库会逐个更新。 |
| 版本与发布工具 | 🟠 | 提升版本、撰写说明和检查发布的脚本，以及可复用的验证工作流，都在玩具仓库上测试过；还没有任何仓库用它们发布过版本。 |
| 工作区与新仓库 | 🟠 | 列出并克隆仓库所需内容的脚本和创建新仓库的脚本，都在临时文件夹中的玩具仓库上测试过；两者都还没有建立过真实的工作区或创建过真实的仓库。 |
| 地图与能力矩阵 | 🟡 | 套件地图、架构说明和能力矩阵涵盖二十七个已发布的仓库及各自的版本，并把仍是计划的那一个程序列为计划中；它们由人工编写，可能落后于仓库。 |
| 真实硬件 | 🟡 | 不适用：文档，这里的内容不会在硬件上运行。 |
| 文档 | 🟡 | 八种语言的 README，每次更改都会与清单和变更日志对照。 |

## 🎯 概述

* **套件地图：** 每个仓库、它的用途，以及它是已发布、已开始（有代码和测试但尚无发行版）还是仅为计划。
* **架构：** 两个共享库、计划依赖它们且彼此从不依赖的程序、通往机床的节点和服务器，以及每个仓库遵循的规则。
* **能力矩阵：** 哪些已在计算机上测试，哪些在机床上运行过（只有 EH3D-DRILLPRO 的协议，在一台机床上），让人无需猜测。
* **约定：** 每个仓库携带的清单、仓库检查和八种语言的 README 文件。
* **检查与工具：** 仓库检查、文档之间的链接检查、两张 README 图片的绘制工具和状态灯，由本仓库复制到每个仓库（`tools/sync_shared_tools.py` 会指出谁落后了），以及退出码约定的检查器。
* **套件契约：** `tools/suite_contract.py` 检查任何单个仓库都无法自行检查的关系：每个清单都能被 Updater 的解析器读取并带有其文件夹的名称，按路径依赖同级仓库时要写明所需版本，地图中的版本与清单一致，屏幕和服务器在端口上一致，共享验证器处处相同，`docs/suite.json` 与重复其取值的位置一致，并且每个仓库都有问题表单。它只发出警告。
* **版本、发布与新工作：** `bump_version.py`、`release_notes.py`、`prerelease_check.py`、`readme_staleness.py` 和 `vendored_tools_report.py`（[docs/RELEASING.md](docs/RELEASING.md)），可复用的验证工作流（[docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)），用于获取仓库所需内容的 `bootstrap_workspace.py`，以及用于创建新仓库的 `new_repo.py`。
* **如何更新：** 车间的 CM5 **通过发布版本**更新（EH3D-SERVER 的 `deploy/eh3d-update.py` 把 GitHub 的发布版本下载到 `/opt`）；EH3D-UPDATER 供**开发电脑使用，通过 git**（[docs/UPDATING.md](docs/UPDATING.md)）。

## 🧩 在 EH3D 中的角色

EH3D-DOCS 是整体描述套件的地方。每个仓库在自己的 README 中描述自己；这里则说明它们如何配合、哪些存在，以及真正运行过什么。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="EH3D-DOCS 的架构：谁在使用、包含什么、依赖什么" width="100%">
</p>

本仓库各部分如何协作：谁在使用它、它包含什么、它依赖什么。图片由 `docs/architecture.json` 绘制，并与代码核对。

## 🔒 安全与防护

本仓库没有接收外部输入的程序；它守护的是所发布内容的准确与洁净。

| 威胁 | 防御 |
|---|---|
| 声称套件的能力超过实际 | 能力矩阵把“在计算机上测试”与“在机床上运行”分开，在有任何人都能运行的代码之前，仓库一律列为计划中 |
| 不该公开的私有引用、人员或工具 | `tools/ci_validate.py` 会在每个文本文件中检查绝不能出现在公开文件里的词，并使检查失败 |
| 文档之间的失效链接 | 当某个 Markdown 文件的相对链接指向不存在的文件时，`tools/check_links.py` 会失败 |
| 某种语言的 README 与其他语言偏离 | 检查会比较八个文件的标题结构、项目状态的信号灯和版本 |
| 不该纳入版本控制的文件（构建产物、密钥、日志、大文件） | 仓库检查会拒绝被跟踪的构建文件夹、私有文件夹、密钥和日志文件，以及超过 1.5 MB 的文件 |

## 🔌 接口

| 接口 | 内容 | 位置 |
|---|---|---|
| 文档 | Markdown：地图、架构、能力矩阵和约定 | [docs/](docs/SUITE_MAP.md) |
| 仓库检查 | `python -I tools/ci_validate.py` 输出 `CI_VALIDATION=PASS`，或列出失败项 | `tools/ci_validate.py` |
| 链接检查 | `python -I tools/check_links.py` 输出 `LINKS=PASS`，或列出失效链接 | `tools/check_links.py` |
| 检查的测试 | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| 套件契约 | `python -I tools/suite_contract.py --workspace ..` 输出 `SUITE_CONTRACT=PASS` 或列出发现的问题；`--write-map` 把清单中的版本写入地图 | `tools/suite_contract.py` |
| 共享工具 | `python -I tools/sync_shared_tools.py` 指出哪些仓库的副本不同 | `tools/sync_shared_tools.py` |
| 版本与发布 | `bump_version.py`、`release_notes.py`、`prerelease_check.py`、`readme_staleness.py`、`vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| 可复用工作流 | 使用 `on: workflow_call` 的验证，供各仓库调用 | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| 工作区 | `bootstrap_workspace.py` 列出并克隆仓库所需内容；`new_repo.py` 创建新仓库 | `tools/bootstrap_workspace.py`、`tools/new_repo.py` |
| 退出码 | `0`、`1`、`2`、`10` 和 `64`；`exit_conventions.py` 据此检查各工具 | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ 配置

这些工具需要 Python 3.10 或更高版本，无需安装，并读取它们所在仓库的文件。它们执行的规则在 `tools/ci_validate.py` 的代码中，多个仓库重复使用的套件取值在 `docs/suite.json` 中：

| 规则 | 限制 | 位置 |
|---|---|---|
| 受版本控制文件的大小 | 最多 1,500,000 字节 | `MAX_TRACKED_BYTES` |
| README 的语言 | 八个文件，标题结构和信号灯相同 | `LANGUAGES` |
| 清单字段 | `REQUIRED` 中的 14 个字段；清单的版本与 `VERSION`（`native_version`）和最新的变更日志条目一致 | `REQUIRED` |
| 套件常量 | 服务器端口、清单架构、八种 README 语言、转速字段、版本的格式、问题表单 | `docs/suite.json` |
| 契约的已知例外 | 每行一个 `check 仓库`，原因解决后删除 | `docs/suite_contract_allow.txt` |
| 仓库对检查的补充 | 例如扫描禁用词时跳过的文件夹 | 各仓库的 `tools/ci_config.json` |

## 🚀 快速开始

需要 Python 3.10 或更高版本；无需安装任何东西。

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

阅读文档请从[套件地图](docs/SUITE_MAP.md)开始。

## 🧪 测试

工具有 126 个测试（`python -I -m unittest discover -s tools -p "test_*.py"`），并且都通过。CI 运行仓库检查（`tools/ci_validate.py`）、文档之间的链接检查（`tools/check_links.py`）、两张图片的检查和这些测试；每日工作流运行套件契约。文档本身除此之外没有测试：它们的说法靠能力矩阵和人工阅读来保持诚实。

## 🏗️ 构建与发布

版本号位于 `VERSION` 文件和 `eh3d.project.json`，每个版本在 [CHANGELOG.md](CHANGELOG.md) 中都有条目。没有需要构建的东西；版本发布在 GitHub 上。

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="EH3D-DOCS 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             每个仓库及其是否已存在
│   ├── ARCHITECTURE.md                          分层和规则
│   ├── CAPABILITY_MATRIX.md                     已测试的内容和在机床上运行过的内容
│   ├── CONVENTIONS.md                           清单、检查和 README
│   ├── UPDATING.md                              CM5 与电脑的更新方式
│   ├── RELEASING.md                             用脚本提升版本并发布
│   ├── REUSABLE_VALIDATION.md                   各仓库可调用的验证工作流
│   ├── VENDORED_TOOLS_REPORT.md                 复制到各仓库但无人使用的工具
│   ├── suite.json                               套件常量
│   ├── suite_contract_allow.txt                 契约的已知例外
│   ├── templates/                               新仓库的模板
│   └── architecture.json structure.json         两张图的数据
├── tools/                                       检查、契约、版本与发布脚本及其测试
├── images/                                      横幅图以及架构和仓库结构图片
├── .github/                                     CI 与仪表板工作流、Issue 和 PR 模板
├── eh3d.project.json                            清单：版本、角色、成熟度和构建命令
├── VERSION                                      文档的版本
├── CHANGELOG.md                                 每个版本的变更
├── SECURITY.md SUPPORT.md                       如何报告漏洞及在哪里提问
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   参与贡献、行为准则和许可证
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* 地图、架构说明和能力矩阵由人工编写；没有任何东西把它们与各仓库的清单对照，因此可能落后。
* 只有已发布的仓库有详细描述；已开始的程序和计划中的程序在地图上各占一行，并标明其状态。
* 除仓库检查和链接检查外，文档本身没有测试。
* 发布、工作区和新仓库脚本只在玩具仓库上试过；还没有用于真实的发布或创建真实的仓库。
* 套件契约只发出警告，仍有几个仓库保留着较旧的共享验证器副本。

**下一步**

* 每个仓库发布或变更时，让地图和能力矩阵同步更新。
* 把地图与各仓库的清单对照，使新仓库不会漏掉。
* 在下一次真实发布中使用这些脚本，在各仓库中采用可复用工作流，并在已知问题消失后让套件契约具有阻断作用。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、汉语、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)：项目容器、机床类型和节点的固件基础
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)：Gerber、Excellon 和 G 代码的读取库
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) 和 [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)：钻孔和铣削程序
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) 和 [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)：Bungard 机床的现代界面和机床控制程序
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) 和 [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)：程序的中心和通往机床的节点
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)、[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI) 和 [EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX)：服务器的配置面板（含来自 GitHub 的更新）、机床的触摸屏，以及钻头上的节点（RTSP 与 ONVIF 摄像头、测量工作台的激光、主轴转速和温度）
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) 和 [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)：安装和更新这些仓库

## 📚 文档

* [套件地图](docs/SUITE_MAP.md)、[架构](docs/ARCHITECTURE.md)、[能力矩阵](docs/CAPABILITY_MATRIX.md)和[约定](docs/CONVENTIONS.md)。
* [发布版本](docs/RELEASING.md)和[可复用的验证](docs/REUSABLE_VALIDATION.md)。
* [变更日志](CHANGELOG.md)

## 🤝 参与贡献与社区

* 提交 pull request 之前运行 `python -I tools/ci_validate.py`、`python -I tools/check_links.py` 和工具的测试：必须全部通过。见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 有八种语言：修改文字时要同步修改全部八个文件，两张图片由 `tools/make_architecture.py` 和 `tools/make_structure.py` 根据 `docs/architecture.json` 和 `docs/structure.json` 绘制。
* 不要把只在计算机上试过的内容描述为能在机床上工作：能力矩阵会说明哪个是哪个。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later。见 [LICENSE](LICENSE)。套件的硬件设计使用 CERN OHL-S。
