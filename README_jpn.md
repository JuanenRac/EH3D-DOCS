<p align="center">
  <img src="images/EH3D_DOCS_BANNER.svg" alt="EH3D-DOCS banner" width="100%">
</p>

# 📚 EH3D-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### EH3D Fabrication Suite の地図、アーキテクチャ、正直な現状：各リポジトリの役割、テスト済みのもの、まだ機械で動かしていないもの

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Markdown%20%2B%20Python-blue.svg" alt="Markdown and Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**正直さの確認 - 今日実際に動くもの：** ドキュメントと 2 つの小さなチェック。スイートはまだ最初の段階です。公開されているリポジトリは 11 件（EH3D-COMMON、EH3D-CORE-LIBS、EH3D-DRILLPRO、EH3D-ROUTEPRO、EH3D-BUNGARD-GUI、EH3D-MOTIONCNC、EH3D-SERVER、EH3D-NODE-BUNGARD、EH3D-UPDATER、ELECTRO-HOBBY-3D-UPDATER、そしてこれ）で、スイートの他のプログラムはすべて計画です。公開済みのものはすべてコンピューター上でテスト済みですが、スイート全体で実機を動かしたのは EH3D-DRILLPRO のシリアル プロトコルだけで（Bungard CCD MTC 1 台での原点復帰と各軸の動き）、ジョブ全体を機械で実行したことはまだありません。5 件のテストがリポジトリ チェックを網羅します。

---

> **安全性とセキュリティの現状：** このリポジトリは機械上では何も実行せず、安全装置でもありません。ここにある文書が、機械とそのコントローラーの上限、インターロック、非常停止の代わりになることは決してありません。

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.0.1` |
| 成熟度 | 足場 |
| テスト | 5 |
| 技術スタック | Markdown と Python 3.10+ の 2 つのチェック |
| 実機での動作 | 該当なし：ドキュメント |

**移動先：** [概要](#-概要) · [アーキテクチャ](#-アーキテクチャ) · [クイックスタート](#-クイックスタート) · [テスト](#-テスト) · [構成](#-リポジトリの構成) · [関連](#-関連プロジェクト)

## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| リポジトリ チェック | 🟡 | リポジトリ チェック、ドキュメント間のリンク チェック、リポジトリ チェックの 5 件のテストは CI で実行され、通っています。 |
| テスト | 🟠 | テストがあるのはリポジトリ チェックだけ（5 件）です。ドキュメントとその主張は、手作業と 2 つのスクリプトで読み、確認します。 |
| 地図と機能マトリクス | 🟡 | スイート マップ、アーキテクチャ ノート、機能マトリクスは公開済みの 11 件のリポジトリを扱い、他のプログラムはすべて計画として載せています。手書きなので、リポジトリより遅れることがあります。 |
| 実機 | 🟡 | 該当なし：ドキュメントで、ここにあるものはハードウェア上では動きません。 |
| ドキュメント | 🟡 | 8 言語の README。変更のたびにマニフェストと変更履歴と照合します。 |

## 🎯 概要

* **スイートの地図：** すべてのリポジトリ、その役割、公開済みか計画のみか。
* **アーキテクチャ：** 共有される 2 つのライブラリ、それらに依存する予定で互いには依存しないプログラム、機械に届くノードとサーバー、すべてのリポジトリが従う規則。
* **機能マトリクス：** コンピューターでテスト済みのものと、機械で動かしたもの（EH3D-DRILLPRO のプロトコルだけを 1 台で）。推測が要らないようにします。
* **規約：** すべてのリポジトリが持つマニフェスト、リポジトリ チェック、8 言語の README。
* **2 つのチェック：** リポジトリ チェックとドキュメント間のリンク チェック。どちらも CI で実行されます。

## 🧩 EH3D での役割

EH3D-DOCS は、スイート全体を説明する場所です。各リポジトリは自分の README で自分を説明し、これはそれらがどう組み合わさるか、どれが存在するか、実際に何が動いたかを示します。

## 🏛️ アーキテクチャ

<p align="center">
  <img src="images/architecture.svg" alt="EH3D-DOCS のアーキテクチャ：誰が使い、何を持ち、何に依存するか" width="100%">
</p>

このリポジトリの各部分の関係：誰が使い、何を持ち、何に依存するか。図は `docs/architecture.json` から描かれ、コードと照合されます。

## 🔒 セキュリティと安全

このリポジトリには外部から入力を受け取るプログラムはありません。守っているのは、公開する内容の正確さと清潔さです。

| 脅威 | 防御 |
|---|---|
| スイートが実際以上のことをするという主張 | 機能マトリクスは「コンピューターでテスト済み」と「機械で動かした」を分け、誰でも実行できるコードができるまでリポジトリは計画として載せます |
| 公開してはならない非公開の参照、人物、ツール | `tools/ci_validate.py` が、公開ファイルに決して現れてはならない語を、すべてのテキスト ファイルで検査して失敗させます |
| ドキュメント間の壊れたリンク | Markdown ファイルの相対リンクが存在しないファイルを指すと、`tools/check_links.py` が失敗します |
| README の言語が他とずれる | チェックが 8 つのファイルで見出し構造、プロジェクトの状況の信号、バージョンを比較します |
| バージョン管理してはならないファイル（ビルド、鍵、ログ、大きなファイル） | リポジトリ チェックは、追跡されたビルド フォルダー、非公開フォルダー、鍵・ログ ファイル、1.5 MB を超えるファイルを拒否します |

## 🔌 インターフェース

| インターフェース | 内容 | 場所 |
|---|---|---|
| ドキュメント | Markdown：地図、アーキテクチャ、機能マトリクス、規約 | [docs/](docs/SUITE_MAP.md) |
| リポジトリ チェック | `python -I tools/ci_validate.py` が `CI_VALIDATION=PASS` を表示、または失敗項目を一覧 | `tools/ci_validate.py` |
| リンク チェック | `python -I tools/check_links.py` が `LINKS=PASS` を表示、または壊れたリンクを一覧 | `tools/check_links.py` |
| チェックのテスト | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |

## ⚙️ 設定

設定するものはありません。2 つのチェックは Python 3.10 以降が必要でインストールは不要、置かれているリポジトリのファイルを読みます。適用する規則は `tools/ci_validate.py` のコードにあります。

| 規則 | 上限 | 場所 |
|---|---|---|
| バージョン管理されるファイルのサイズ | 最大 1,500,000 バイト | `MAX_TRACKED_BYTES` |
| README の言語 | 見出し構造と信号が同じ 8 ファイル | `LANGUAGES` |
| マニフェストの項目 | `REQUIRED` の 14 項目。マニフェストのバージョンは `VERSION`（`native_version`）と最新の変更履歴の項目に一致 | `REQUIRED` |

## 🚀 クイックスタート

Python 3.10 以降が必要で、インストールするものはありません。

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I -m unittest discover -s tools -p "test_*.py"
```

ドキュメントを読むには、[スイートの地図](docs/SUITE_MAP.md)から始めてください。

## 🧪 テスト

リポジトリ チェックには 5 件のテストがあり（`python -I -m unittest discover -s tools -p "test_*.py"`）、通っています。CI はリポジトリ チェック（`tools/ci_validate.py`）、ドキュメント間のリンク チェック（`tools/check_links.py`）、そしてそれらのテストを実行します。ドキュメント自体にそれ以外のテストはなく、主張の正直さは、説明対象のリポジトリを読むことで保たれます。

## 🏗️ ビルドとリリース

バージョンは `VERSION` ファイルと `eh3d.project.json` にあり、各バージョンには [CHANGELOG.md](CHANGELOG.md) の項目があります。ビルドするものはなく、リリースは GitHub で公開されます。

## 📂 リポジトリの構成

<p align="center">
  <img src="images/repository-structure.svg" alt="EH3D-DOCS のリポジトリ構成" width="100%">
</p>

<details>
<summary>ツリーのテキスト版</summary>

```text
EH3D-DOCS/
├── docs/
│   ├── SUITE_MAP.md                             すべてのリポジトリと存在の有無
│   ├── ARCHITECTURE.md                          レイヤーと規則
│   ├── CAPABILITY_MATRIX.md                     テスト済みのものと機械で動かしたもの
│   ├── CONVENTIONS.md                           マニフェスト、チェック、README
│   └── architecture.json structure.json         2 つの図のデータ
├── tools/                                       リポジトリ チェック、リンク チェック、そのテストと図のツール
├── images/                                      バナーとアーキテクチャ・リポジトリ構成の図
├── .github/                                     CI とリリースのワークフロー、Issue と PR のテンプレート
├── eh3d.project.json                            マニフェスト：バージョン、役割、成熟度、ビルドコマンド
├── VERSION                                      ドキュメントのバージョン
├── CHANGELOG.md                                 各バージョンの変更点
├── SECURITY.md SUPPORT.md                       脆弱性の報告方法と問い合わせ先
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   貢献方法、行動規範、ライセンス
```

</details>

## 🗺️ ロードマップと既知の制限

**現時点で分かっている制限**

* 地図、アーキテクチャ ノート、機能マトリクスは手書きで、リポジトリのマニフェストと照合するものはないため、遅れることがあります。
* 詳しく説明しているのは公開済みのリポジトリだけで、他のプログラムは計画として印を付けた地図の 1 行です。
* ドキュメントには、リポジトリ チェックとリンク チェック以外に独自のテストはありません。

**次のステップ**

* 各リポジトリが公開・変更されるたびに、地図と機能マトリクスを歩調を合わせて更新する。
* 地図をリポジトリのマニフェストと照合し、新しいリポジトリが載り漏れないようにする。

## 🌍 言語

README とテキストは、英語、スペイン語、フランス語、イタリア語、ドイツ語、中国語、日本語、ヨーロッパポルトガル語で提供されています。

## 🔗 関連プロジェクト

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)：プロジェクト コンテナ、機械の型、ノードのファームウェア基盤
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)：Gerber、Excellon、G コードのリーダー
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) と [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)：ドリルとルーティングのプログラム
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) と [EH3D-MOTIONCNC](https://github.com/JuanenRac/EH3D-MOTIONCNC)：Bungard マシンのモダンなインターフェースとマシン制御プログラム
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) と [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)：プログラムの中心と、機械に届くノード
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) と [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)：リポジトリのインストールと更新

## 📚 ドキュメント

* [スイートの地図](docs/SUITE_MAP.md)、[アーキテクチャ](docs/ARCHITECTURE.md)、[機能マトリクス](docs/CAPABILITY_MATRIX.md)、[規約](docs/CONVENTIONS.md)。
* [変更履歴](CHANGELOG.md)

## 🤝 コントリビュートとコミュニティ

* プルリクエストの前に `python -I tools/ci_validate.py`、`python -I tools/check_links.py`、チェックのテストを実行し、すべて通してください。[CONTRIBUTING.md](CONTRIBUTING.md) と[行動規範](CODE_OF_CONDUCT.md)を参照してください。
* README は 8 言語あります。文章を変更するときは 8 つのファイルすべてを変更し、2 つの図は `docs/architecture.json` と `docs/structure.json` から `tools/make_architecture.py` と `tools/make_structure.py` で描画します。
* コンピューターでしか試していないことを、機械で動くものとして書かないでください。どちらかは機能マトリクスに書かれています。
* 脆弱性は非公開で報告してください：[SECURITY.md](SECURITY.md)。質問、アイデア、報告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later。[LICENSE](LICENSE) を参照。スイートのハードウェア設計には CERN OHL-S を使います。
