<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### EH3D Fabrication Suite の地図、アーキテクチャ、正直な現状：各リポジトリの目的、テスト済みのもの、まだ機械で動かしていないもの

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Docs-Markdown-blue.svg" alt="Markdown">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**正直さのチェック - 今あるもの：** ドキュメントと2つの小さなチェックです。スイートは最初の一歩の段階で、3つのリポジトリが公開されています（プロジェクトコンテナの EH3D-COMMON、Gerber、Excellon、G-code のリーダーを持つ EH3D-CORE-LIBS、そして EH3D-UPDATER）。スイートの各プログラムは計画です。公開されているものはすべてコンピューター上でテスト済みですが、機械で動かしたものはありません。

---

> **安全性（safety）とセキュリティの現状：** このリポジトリは機械上で何も実行せず、安全システムでもありません。ここのドキュメントが、機械とそのコントローラーのリミット、インターロック、非常停止に取って代わることはありません。

## 📋 概要

| | |
|---|---|
| バージョン | `0.0.1` |
| 成熟度 | 足場段階 |
| 技術スタック | Markdown / Python 3.10+（チェック用） |
| 実機 | 該当なし：ドキュメント |

## 🎯 概要

* **スイートの地図：** 各リポジトリ、その目的、公開済みか計画のみか。
* **アーキテクチャ：** 共有の2つのライブラリ、それらに依存し互いには依存しないプログラム、すべてのリポジトリが守るルール。
* **能力マトリクス：** コンピューターでテスト済みのものと機械で動かしたもの（まだ何もありません）を示し、誰も推測しなくて済むようにします。
* **規約：** 各リポジトリが持つマニフェスト、リポジトリチェック、8言語の README。
* **2つのチェック：** リポジトリのチェックとドキュメント間のリンクのチェック。どちらも CI で実行されます。

## 📂 リポジトリ構成

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

## 🛠️ ビルドと実行

Python 3.10 以降が必要です。インストールするものはありません。

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
```

## 🔗 関連プロジェクト

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): プロジェクトコンテナとマシンの型
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): Gerber、Excellon、G-code のリーダー
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): スイートのリポジトリをインストール・更新する

## 📚 ドキュメントとコミュニティ

* [スイートの地図](docs/SUITE_MAP.md)、[アーキテクチャ](docs/ARCHITECTURE.md)、[能力マトリクス](docs/CAPABILITY_MATRIX.md)、[規約](docs/CONVENTIONS.md)（英語）。
* [コントリビュート](CONTRIBUTING.md)、[セキュリティポリシー](SECURITY.md)、[サポート](SUPPORT.md)、[行動規範](CODE_OF_CONDUCT.md)。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later。[LICENSE](LICENSE) を参照。
