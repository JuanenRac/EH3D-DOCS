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
  <img src="https://img.shields.io/badge/Version-0.0.9-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**正直さの確認 - 今日実際に動くもの：** ドキュメントとスイートのツール。これらはコンピューター上でしか動きません（各リポジトリが持つリポジトリ チェックと図の描画ツール、リポジトリ間の契約、バージョンを上げてリリースを準備するスクリプト、作業領域を用意するスクリプト、新しいリポジトリを作るスクリプト）。スイートはまだ最初の段階です。公開されているリポジトリは 29 件（ライブラリ、Bungard のプログラム、サーバーと Studio、ノードとタッチ スクリーン、スマートフォン アプリ、CAM とユーティリティのプログラム、アップデーター、そしてこれ）、コードとテストはあるが未リリースの 1 件（電子設計プロジェクトのテスト ラボ）、計画のみの 10 件（小型タッチ スクリーン用のペンダントと、電子設計プロジェクトとそのブリッジの 9 件）です。公開済みのものはすべてコンピューター上でテスト済みで、インターフェースは 37 言語に対応しています。スイート全体で実機を動かしたのは EH3D-DRILLPRO のシリアル プロトコルだけで（Bungard CCD MTC 1 台での原点復帰と各軸の動き）、ジョブ全体を機械で実行したことはまだありません。14 件のテストがリポジトリ チェックを網羅します。

---

> **安全性とセキュリティの現状：** このリポジトリは機械上では何も実行せず、安全装置でもありません。ここにある文書が、機械とそのコントローラーの上限、インターロック、非常停止の代わりになることは決してありません。

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.0.9` |
| 成熟度 | 機能する |
| テスト | 196 |
| 技術スタック | Markdown と Python 3.10+ のツール |
| 実機での動作 | 該当なし：ドキュメント |

**移動先：** [概要](#-概要) · [アーキテクチャ](#-アーキテクチャ) · [クイックスタート](#-クイックスタート) · [テスト](#-テスト) · [構成](#-リポジトリの構成) · [関連](#-関連プロジェクト)

## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| リポジトリ チェック | 🟡 | リポジトリ チェック、ドキュメント間のリンク チェック、ツールのテストは CI で実行され、通っています。 |
| テスト | 🟠 | ツールの 196 件のテストがコンピューター上で通っており、その一部は小さな試験用リポジトリで行っています。ドキュメントとその主張は、手作業とスクリプトで読み、確認します。 |
| スイートの契約 | 🟡 | リポジトリ間の契約は、Updater のパーサーで各マニフェストを読み、ずれ（ポート、README の言語、共有ツール、課題フォーム）を警告します。CI で毎日警告として実行され、名前が挙がったリポジトリは 1 つずつ更新していきます。 |
| バージョンとリリースのツール | 🟠 | バージョンを上げ、ノートを書き、リリースを確認するスクリプトと、再利用できる検証ワークフローは、試験用リポジトリでテスト済みです。これらでリリースを公開したリポジトリはまだありません。 |
| 作業領域と新しいリポジトリ | 🟠 | リポジトリに必要なものを一覧して複製するスクリプトと、新しいリポジトリを作るスクリプトは、一時フォルダー内の試験用リポジトリでテスト済みです。どちらも、実際の作業領域の準備や実際のリポジトリの作成にはまだ使われていません。 |
| 地図と機能マトリクス | 🟡 | スイート マップ、アーキテクチャ ノート、機能マトリクスは 40 件のリポジトリを扱います。公開済みの 29 件は各バージョンとともに、開始済みの 1 件（コードとテストはあるが未リリース）と計画中の 10 件（文書化した範囲のみでコードなし）を載せています。手書きなので、リポジトリより遅れることがあります。 |
| 実機 | 🟡 | 該当なし：ドキュメントで、ここにあるものはハードウェア上では動きません。 |
| ドキュメント | 🟡 | 8 言語の README。変更のたびにマニフェストと変更履歴と照合します。 |

## 🎯 概要

* **スイートの地図：** すべてのリポジトリ、その役割、公開済み、着手済み（コードとテストはあるがリリースはまだ）、計画のみのいずれか。
* **アーキテクチャ：** 共有される 2 つのライブラリ、それらに依存する予定で互いには依存しないプログラム、機械に届くノードとサーバー、すべてのリポジトリが従う規則。
* **機能マトリクス：** コンピューターでテスト済みのものと、機械で動かしたもの（EH3D-DRILLPRO のプロトコルだけを 1 台で）。推測が要らないようにします。
* **規約：** すべてのリポジトリが持つマニフェスト、リポジトリ チェック、8 言語の README。
* **チェックとツール：** リポジトリ チェック、ドキュメント間のリンク チェック、2 つの README 図の描画ツールと状態ランプを、このリポジトリから各リポジトリへコピーします（`tools/sync_shared_tools.py` が遅れているリポジトリを示します）。終了コード規約の検査ツールもあります。`banner_check.py` は各バナーの文言がマニフェストの内容と一致するかを確認し、`docs/vendored.lock` は共有ツールごとの出所とバージョンを記録します。
* **スイートの契約：** `tools/suite_contract.py` は、単独のリポジトリでは確認できない関係を確認します。すべてのマニフェストが Updater のパーサーで読めてフォルダー名を持つこと、パスで隣のリポジトリに依存する場合に必要なバージョンを示すこと、地図のバージョンがマニフェストと一致すること、画面とサーバーがポートで一致すること、共有バリデーターがどこでも同じであること、`docs/suite.json` が値を繰り返している場所と一致すること、すべてのリポジトリに課題フォームがあること。警告のみです。
* **バージョン、リリース、新しい作業：** `bump_version.py`、`release_notes.py`、`prerelease_check.py`、`readme_staleness.py`、`vendored_tools_report.py`（[docs/RELEASING.md](docs/RELEASING.md)）、再利用できる検証ワークフロー（[docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md)）、リポジトリに必要なものを取得する `bootstrap_workspace.py`、新しいリポジトリを作る `new_repo.py`。`bump_version.py` は、最小バージョンを要求する内部依存関係、ワークスペースのパッケージの `Cargo.lock` の項目、ファミリー全体のアップデーターのマニフェストも更新します。
* **更新の方法：** 作業場の CM5 は**リリース経由**で更新されます（EH3D-SERVER の `deploy/eh3d-update.py` が GitHub のリリースを `/opt` にダウンロードします）。EH3D-UPDATER は**開発用 PC 向けで、git 経由**です（[docs/UPDATING.md](docs/UPDATING.md)）。

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
| ドキュメント | Markdown：地図、アーキテクチャ、機能マトリクス、規約、更新とリリースのガイド | [docs/](docs/SUITE_MAP.md) |
| リポジトリ チェック | `python -I tools/ci_validate.py` が `CI_VALIDATION=PASS` を表示、または失敗項目を一覧 | `tools/ci_validate.py` |
| リンク チェック | `python -I tools/check_links.py` が `LINKS=PASS` を表示、または壊れたリンクを一覧 | `tools/check_links.py` |
| チェックのテスト | `python -I -m unittest discover -s tools -p "test_*.py"` | `tools/test_ci_validate.py` |
| スイートの契約 | `python -I tools/suite_contract.py --workspace ..` が `SUITE_CONTRACT=PASS` を出力するか、指摘を一覧します。`--write-map` はマニフェストのバージョンを地図に書き込みます | `tools/suite_contract.py` |
| 共有ツール | `python -I tools/sync_shared_tools.py` が、コピーが異なるリポジトリを示します | `tools/sync_shared_tools.py` |
| バージョンとリリース | `bump_version.py`、`release_notes.py`、`prerelease_check.py`、`readme_staleness.py`、`vendored_tools_report.py` | [docs/RELEASING.md](docs/RELEASING.md) |
| 再利用できるワークフロー | `on: workflow_call` による検証。各リポジトリから呼び出します | [docs/REUSABLE_VALIDATION.md](docs/REUSABLE_VALIDATION.md) |
| 作業領域 | `bootstrap_workspace.py` はリポジトリに必要なものを一覧して複製し、`new_repo.py` は新しいリポジトリを作ります | `tools/bootstrap_workspace.py`、`tools/new_repo.py` |
| 終了コード | `0`、`1`、`2`、`10`、`64`。`exit_conventions.py` がツールをこれと照合します | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |

## ⚙️ 設定

ツールには Python 3.10 以降が必要で、インストールは不要です。ツールは自分が置かれているリポジトリのファイルを読みます。適用する規則は `tools/ci_validate.py` のコードにあり、複数のリポジトリが繰り返すスイートの値は `docs/suite.json` にあります。

| 規則 | 上限 | 場所 |
|---|---|---|
| バージョン管理されるファイルのサイズ | 最大 1,500,000 バイト | `MAX_TRACKED_BYTES` |
| README の言語 | 見出し構造と信号が同じ 8 ファイル | `LANGUAGES` |
| マニフェストの項目 | `REQUIRED` の 14 項目。マニフェストのバージョンは `VERSION`（`native_version`）と最新の変更履歴の項目に一致 | `REQUIRED` |
| スイートの定数 | サーバーのポート、マニフェストのスキーマ、8 つの README 言語、回転数の欄、バージョンの形式、課題フォーム | `docs/suite.json` |
| 契約の既知の例外 | 1 行に 1 つの `check リポジトリ`。原因が直ったら削除します | `docs/suite_contract_allow.txt` |
| リポジトリがチェックに加えるもの | たとえば禁止語の走査が飛ばすフォルダー | 各リポジトリの `tools/ci_config.json` |

## 🚀 クイックスタート

Python 3.10 以降が必要で、インストールするものはありません。

```bash
python -I tools/ci_validate.py
python -I tools/check_links.py
python -I tools/suite_contract.py --workspace ..
python -I tools/bootstrap_workspace.py --workspace .. EH3D-DRILLPRO
python -I -m unittest discover -s tools -p "test_*.py"
```

ドキュメントを読むには、[スイートの地図](docs/SUITE_MAP.md)から始めてください。

## 🧪 テスト

ツールには 196 件のテストがあり（`python -I -m unittest discover -s tools -p "test_*.py"`）、通っています。CI はリポジトリ チェック（`tools/ci_validate.py`）、ドキュメント間のリンク チェック（`tools/check_links.py`）、2 つの図のチェック、これらのテストを実行し、毎日のワークフローがスイートの契約を実行します。ドキュメント自体にはこれ以外のテストはなく、主張は機能マトリクスと読み返しによって正直に保たれます。

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
│   ├── UPDATING.md                              CM5 と PC の更新方法
│   ├── RELEASING.md                             スクリプトでバージョンを上げて公開する
│   ├── REUSABLE_VALIDATION.md                   各リポジトリが呼び出せる検証ワークフロー
│   ├── VENDORED_TOOLS_REPORT.md                 各リポジトリにコピーされた、使われていないツール
│   ├── suite.json                               スイートの定数
│   ├── suite_contract_allow.txt                 契約の既知の例外
│   ├── templates/                               新しいリポジトリのテンプレート
│   └── architecture.json structure.json         2 つの図のデータ
├── tools/                                       チェック、契約、バージョンとリリースのスクリプト、そのテスト
├── registry/                                    コンテナと識別子のコードの一覧とそのテスト
├── images/                                      バナーとアーキテクチャ・リポジトリ構成の図
├── .github/                                     CI とダッシュボードのワークフロー、Issue と PR のテンプレート
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
* 詳しく説明しているのは公開済みのリポジトリだけで、着手済みのプログラムと計画中のプログラムは、それぞれその旨の印を付けた地図の 1 行です。
* ドキュメントには、リポジトリ チェックとリンク チェック以外に独自のテストはありません。
* リリース、作業領域、新しいリポジトリのスクリプトは試験用リポジトリでしか試していません。実際のリリースや実際のリポジトリの作成には、まだ使われていません。
* スイートの契約は警告のみで、共有バリデーターの古いコピーを持つリポジトリがまだいくつかあります。

**次のステップ**

* 各リポジトリが公開・変更されるたびに、地図と機能マトリクスを歩調を合わせて更新する。
* 地図をリポジトリのマニフェストと照合し、新しいリポジトリが載り漏れないようにする。
* 次の実際のリリースでスクリプトを使い、各リポジトリで再利用できるワークフローを採用し、既知の指摘がなくなったらスイートの契約を必須にする。

## 🌍 言語

README とテキストは、英語、スペイン語、フランス語、イタリア語、ドイツ語、中国語、日本語、ヨーロッパポルトガル語で提供されています。

## 🔗 関連プロジェクト

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)：プロジェクト コンテナ、機械の型、ノードのファームウェア基盤
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)：Gerber、Excellon、G コードのリーダー
* [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) と [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO)：ドリルとルーティングのプログラム
* [EH3D-BUNGARD-GUI](https://github.com/JuanenRac/EH3D-BUNGARD-GUI) と [EH3D-PHOENIX-CNC](https://github.com/JuanenRac/EH3D-PHOENIX-CNC)：Bungard マシンのモダンなインターフェースとマシン制御プログラム
* [EH3D-SERVER](https://github.com/JuanenRac/EH3D-SERVER) と [EH3D-NODE-BUNGARD](https://github.com/JuanenRac/EH3D-NODE-BUNGARD)：プログラムの中心と、機械に届くノード
* [EH3D-STUDIO](https://github.com/JuanenRac/EH3D-STUDIO)、[EH3D-NODE-BUNGARD-HMI](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-HMI)、[EH3D-NODE-BUNGARD-AUX](https://github.com/JuanenRac/EH3D-NODE-BUNGARD-AUX)：サーバーの設定パネル（GitHub からの更新付き）、マシンのタッチスクリーン、ドリルヘッドのノード（RTSP と ONVIF のカメラ、テーブルを測るレーザー、スピンドルの回転数と温度）
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) と [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)：リポジトリのインストールと更新
* [EH3D-PHOENIX-PCB](https://github.com/JuanenRac/EH3D-PHOENIX-PCB) および [EH3D-PHOENIX-CAD](https://github.com/JuanenRac/EH3D-PHOENIX-CAD)（電子設計と機械設計、どちらも最初のリリースあり）と、電子設計プロジェクトとそのブリッジ（ラボ、検証ツール、熱ラボ、HYDRA-UMC へのアダプター）のほかの 9 件のリポジトリ：開始済みまたは計画中で、未リリース

## 📚 ドキュメント

* [スイートの地図](docs/SUITE_MAP.md)、[アーキテクチャ](docs/ARCHITECTURE.md)、[機能マトリクス](docs/CAPABILITY_MATRIX.md)、[規約](docs/CONVENTIONS.md)。
* [バージョンの公開](docs/RELEASING.md)、[機械を最新に保つ方法](docs/UPDATING.md)、[再利用できる検証](docs/REUSABLE_VALIDATION.md)。
* [別のリポジトリから共有クレートを使う](https://github.com/JuanenRac/EH3D-COMMON/blob/main/docs/CONSUMING.md)：隣接フォルダー、パスとバージョンの行、CI がビルドに使うタグ、`min_common`。
* [変更履歴](CHANGELOG.md)

## 🤝 コントリビュートとコミュニティ

* プル リクエストの前に `python -I tools/ci_validate.py`、`python -I tools/check_links.py`、ツールのテストを実行してください。すべて通る必要があります。[CONTRIBUTING.md](CONTRIBUTING.md) と[行動規範](CODE_OF_CONDUCT.md)を参照してください。
* README は 8 言語あります。文章を変更するときは 8 つのファイルすべてを変更し、2 つの図は `docs/architecture.json` と `docs/structure.json` から `tools/make_architecture.py` と `tools/make_structure.py` で描画します。
* コンピューターでしか試していないことを、機械で動くものとして書かないでください。どちらかは機能マトリクスに書かれています。
* 脆弱性は非公開で報告してください：[SECURITY.md](SECURITY.md)。質問、アイデア、報告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later。[LICENSE](LICENSE) を参照。スイートのハードウェア設計には CERN OHL-S を使います。
