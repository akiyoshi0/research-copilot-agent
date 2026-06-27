# Research Co-Pilot Agent

Research Co-Pilot Agent は、研究者が主導し、Codex が横で研究を整理、実装、検証、論文化まで支援するためのローカル研究並走ワークスペースです。

目的は「完全自動研究者」を作ることではありません。
目的は、研究者の判断を中心に残したまま、先行研究整理、実験記録、再現性確認、論文作成の負担を下げることです。

このリポジトリは、生命科学、バイオインフォマティクス、機械学習研究における「真の研究者並走型 AI for Science」を実現するための最小構成を提供します。

```text
Codex
+ Markdown
+ skills
+ review-gate
+ experiment capsules
+ reproducible results
+ manuscript workflow
```

## なぜ必要か

研究で AI を使うときの問題は、単にコードを書けるかどうかではありません。
実際の研究では、次のような地味で重要な作業が継続的に発生します。

- 研究計画を崩さずにタスクへ分解する
- 先行研究のPDFと公開コードを整理する
- 実験条件、seed、環境、出力、失敗を記録する
- 一時的な実験と採用済みコードを分ける
- 結果の飛躍、データリーク、外部送信リスクを確認する
- 論文本文と内部作業ログを混同しない
- 論文で使う表や図を完全再生成できる状態にする

Research Co-Pilot Agent は、これらを Codex と Markdown だけで扱えるようにします。
複雑なWeb UI、DB、ベクトルDB、多数の自律エージェントは使いません。
研究者が理解でき、監査でき、必要なところで止められることを優先します。

## 設計思想

### 人間主導

研究方針、評価指標、主要主張、投稿準備、大規模実験、外部API送信は、Codexだけで勝手に進めません。
重要な局面では `03-review-gate` によって止め、人間の判断を要求します。

### ローカル優先

研究状態はローカルのMarkdownファイルとして管理します。
明示的に必要とされない限り、データベース、クラウド同期、独自Web UIは導入しません。

### 再現性優先

探索実験は `experiments/` に experiment capsule として残します。
論文に使う本実験は `reproduction/` から `results/` を再生成できる形に整理します。
原稿は `results/` の成果物を参照し、予備実験の生出力を直接参照しません。

### 論文本文と内部管理の分離

`research_state/`、review-gate、実行ログ、`scripts/` と `src/` の責務分離、`results/result_index.md` などは内部管理情報です。
論文本文には、研究内容を理解するために必要なデータ、方法、結果、考察だけを書きます。

## 目指さないこと

- 完全自動研究者
- 自動投稿
- 独自Web UI
- データベース
- ベクトルDB
- 複雑なマルチエージェント基盤
- 研究者の判断を置き換えること
- 外部APIへローカルデータを無断送信すること

## リポジトリ構成

```text
research-copilot-mvp/
├── README.md
├── LICENSE
├── ROADMAP.md
├── AGENTS.md
├── tools/
│   └── init_research_workspace.py
├── templates/
├── skills/
└── .github/
    └── ISSUE_TEMPLATE/
```

`skills/` は、生成先研究プロジェクトの `.agents/skills/` にコピーされる正本です。
`templates/` は、生成先研究プロジェクトにコピーされるMarkdown、Mermaid、設定ファイル、`.gitkeep` の正本です。
`example_project/` はローカル検証用のサンプルであり、公開リポジトリの中核成果物としては扱いません。

## インストール

依存関係は `uv` で管理します。

```bash
uv sync
```

このプロジェクトでは、通常のセットアップでは `pip install` ではなく `uv sync` を使います。

## 新しい研究ワークスペースを作る

```bash
python tools/init_research_workspace.py --project-name my_project
```

生成される研究ワークスペースは次の構成です。

```text
my_project/
├── AGENTS.md
├── README.md
├── research_plan.md
├── prior_research/
├── data/
├── src/
├── scripts/
├── notebooks/
├── experiments/
├── reproduction/
├── results/
├── manuscript/
├── research_state/
│   ├── research_spec.md
│   ├── state.md
│   ├── tasks.md
│   ├── logbook.md
│   ├── manuscript_plan.md
│   └── workflow.mmd
└── .agents/
    └── skills/
```

生成後、Codex にはまず次のように依頼します。

```text
00-project-initializer を実行して。
```

ここでの「実行」はOSコマンドではなく、生成先の `.agents/skills/00-project-initializer/` のskillとして作業するという意味です。

## 5つの core skills

### `00-project-initializer`

研究計画と先行研究を読み、`research_state/` の6ファイルを初期化します。

### `01-task-planner`

次に行うべき実装タスク、実験タスク、確認タスクを設計します。
大きな作業を、review-gateで確認できる単位へ分解します。

### `02-research-executor`

承認済みタスクに従って、実装、解析、実験、結果出力を行います。
研究ロジックは `src/` に置き、`scripts/` は `src/` を呼び出す薄いCLIに限定します。

### `03-review-gate`

研究計画とのズレ、データリーク、再現性、外部送信リスク、`src/` 変更採用、論文主張、原稿品質を確認します。
判定は `PASS`、`REVISE`、`HUMAN`、`STOP` の4つだけです。

### `04-manuscript-builder`

`results/`、`prior_research/`、`research_state/manuscript_plan.md` をもとに論文原稿を作成します。
内部管理情報を論文本文に混ぜないことを明示的なルールにしています。

## 2つの utility skills

呼び出すときの正式なskill名は `prior-research-downloader` と `prior-research-ingester` です。
`skills/utilities/...` は実体のフォルダパスを説明するときだけ使います。

### `prior-research-downloader`

先行研究1件分のフォルダを作り、合法的に取得できる公開PDFと公開コードdigestを整えます。
paywall回避、ログイン回避、token利用、機関認証の迂回は行いません。
実体は `skills/utilities/prior-research-downloader/` にあります。

### `prior-research-ingester`

PDFと公開コードをCodexが読みやすいMarkdownへ変換します。
実体は `skills/utilities/prior-research-ingester/` にあります。

```text
paper.pdf -> paper.md
code_url or source/ -> source.md
```

PDF変換には `pymupdf4llm` を使います。
ソースコードdigest化には `gitingest` を使います。
公開コードは原則としてcloneせず、`metadata.yaml` の `code_url` から `source.md` へ直接digest化します。
`gitingest` では、1ファイルあたり100KB以下のファイルだけを `source.md` に入れます。
取得元、変換結果、失敗理由、未解決点は `metadata.yaml` と `idea_notes.md` に記録します。

## research_state

研究状態は6つのMarkdownファイルで管理します。

```text
research_state/
├── research_spec.md
├── state.md
├── tasks.md
├── logbook.md
├── manuscript_plan.md
└── workflow.mmd
```

この構成により、Codexの作業をブラックボックスにせず、研究者が常に確認、差し戻し、再開できる状態を保ちます。

## experiment capsule

予備実験、探索、候補実験は `experiments/` に capsule として残します。

```text
experiments/
└── exp_YYYYMMDD_001_short_name/
    ├── manifest.md
    ├── config.yaml
    ├── run.sh
    ├── idea_notes.md
    ├── outputs/
    └── snapshot.diff
```

`experiments/` に研究ロジックのソースコードは置きません。
`run.sh` は、環境準備、`scripts/` の実行用Pythonスクリプト呼び出し、引数指定だけに限定します。

## reproduction と results

論文に使う本実験は `reproduction/` に整理します。

```text
reproduction/
├── README.md
├── config.yaml
├── run_all.sh
├── 00_prepare_data.sh
└── 01_run_main_analysis.sh
```

`reproduction/run_all.sh` を実行すると、`results/` の表、図、集約結果が再生成される状態を目指します。

```text
results/
├── tables/
├── figures/
└── result_index.md
```

`result_index.md` には、各成果物の生成元、対応する `reproduction/` step、出所となる中間出力、原稿内での使い道を記録します。

## 安全性とレビュー方針

次の場合、CodexだけでPASSにしません。

- 大規模実験
- 外部APIへのローカルデータ送信
- API keyやtokenの利用
- `src/` 変更の採用
- 論文の主要主張
- 投稿準備
- 医療、臨床、法務、財務など高リスクな断定

review-gateでは、必要に応じて `HUMAN` または `STOP` を返します。

## OSSメンテナンス方針

このプロジェクトでは、IssueとPull Requestを次の観点で扱います。

- 研究者が理解できる単純さを保つ
- Codexが扱いやすいMarkdown中心の状態管理を保つ
- 生成先ワークスペースの再現性を壊さない
- 内部管理情報と論文本文を混ぜない
- 外部データ送信やライセンス上のリスクを明示する

Issueを作る場合は、`.github/ISSUE_TEMPLATE/` のテンプレートを使ってください。

## ロードマップ

今後の計画は [ROADMAP.md](ROADMAP.md) にまとめています。
当面は、研究ワークスペース生成、先行研究ingest、review-gate、reproduction、manuscript workflow の品質を優先します。

## ライセンス

このプロジェクトは [MIT License](LICENSE) で公開します。

## 貢献

現在はMVP段階です。
Pull Requestでは、機能追加よりも次を重視します。

- 既存ワークフローを単純に保つ改善
- review-gateの精度向上
- 研究再現性の改善
- ドキュメントの明確化
- テストしやすい小さな変更

複雑なWeb UI、DB、クラウド同期、多数の自律エージェントを追加する提案は、原則としてこのMVPの範囲外です。
