# Research Co-Pilot Workspace MVP

これは、研究者とCodexがMarkdownを共有記憶として使い、研究計画、先行研究整理、実装、実験、結果解釈、論文作成を進めるための最小構成です。
目的は完全自動研究者を作ることではありません。
研究者が主導し、Codexが横で整理と実行を支援します。

## 目指さないこと

- 独自Web UI
- データベース
- ベクトルDB
- 複雑なマルチエージェント基盤
- 完全自動研究者
- 自動投稿

## 本体リポジトリの構成

```text
research-copilot-mvp/
├── README.md
├── AGENTS.md
├── tools/
│   └── init_research_workspace.py
├── templates/
├── skills/
└── example_project/
```

`skills/` は、生成先プロジェクトの `.agents/skills/` にコピーする正本です。
`templates/` は、生成先プロジェクトにコピーするMarkdown、Mermaid、設定ファイル、`.gitkeep` の正本です。
`PROJECT_BRIEF.md` は本体設計書です。
生成先研究プロジェクトにはコピーせず、研究者向けの説明は `README.md`、Codex向けの規則は `AGENTS.md` に置きます。

## 初期化方法

依存ライブラリは `uv` で管理します。
このプロジェクトでは `pip install` ではなく `uv sync` を使います。

```bash
uv sync
```

新しい研究プロジェクトを作る場合は次を実行します。

```bash
python tools/init_research_workspace.py --project-name my_project
```

## 生成される研究プロジェクト

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

`README.md` は、生成先研究プロジェクトで研究者がどう作業するかを説明する利用ガイドです。
`AGENTS.md` は、Codexが守る作業規則、review-gate、experiment capsule、`src/` 変更ルール、MarkdownとPythonの書き方をまとめます。

## Codexへの最初の指示

生成した研究プロジェクトで、Codexには最初に次のように依頼します。

```text
00-project-initializer を実行して。
```

ここでの「実行」は、OSコマンドではなく `.agents/skills/00-project-initializer/` のskillとして作業する、という意味です。

## 5 core skills

- `00-project-initializer`: 研究計画と先行研究を読み、`research_state/` を初期化する
- `01-task-planner`: 次の実装タスクと実験タスクを設計する
- `02-research-executor`: 承認済みタスクに従って実装、解析、実験を行う
- `03-review-gate`: 方針、実験、結果、外部送信、src変更、論文主張を確認する
- `04-manuscript-builder`: 研究結果と先行研究をもとに論文計画と原稿を作る

## 2 utility skills

- `utilities/prior-research-downloader`: 先行研究1件分の置き場を作り、取得可能なPDFや公開コードを配置する
- `utilities/prior-research-ingester`: PDFとソースコードをCodexが読みやすいMarkdownに変換する

## prior_research の考え方

先行研究は論文単位で管理します。
論文とコードを大きな `papers/` と `prior_code/` に分けません。

```text
prior_research/
└── paper_id/
    ├── paper.pdf
    ├── paper.md
    ├── source/
    ├── source.md
    ├── metadata.yaml
    └── notes.md
```

paywall、ログイン、token、機関認証が必要な場合、Codexは勝手に取得しません。
人間が合法的にファイルを配置します。

## PDFとコードのMarkdown化

Codexは、生PDFやソースツリー全体ではなく、まずMarkdown化済みファイルを読みます。

```text
paper.pdf → paper.md
source/   → source.md
```

PDF変換には `pymupdf4llm` を使います。
ソースコードdigest化には `gitingest` を使います。
`source/` のdigest化では、1ファイルあたり100KB以下のファイルだけを `source.md` に入れます。
100KBを超えるファイルは除外し、スキップ理由を `notes.md` と `research_state/logbook.md` に記録します。
実処理は生成先プロジェクトの `.agents/skills/utilities/` 配下に置かれたutility skill内部スクリプトが担当します。
人間は原則として `.agents/skills/**/scripts/` を直接実行せず、Codexに依頼します。

## review-gate

判定は4つだけです。

```text
PASS
REVISE
HUMAN
STOP
```

大規模実験、外部APIへのローカルデータ送信、`src/` 変更の採用、論文の主要主張、投稿準備は、人間確認後でなければPASSにしません。

## experiment capsule

予備実験、探索、候補実験は `experiments/` に experiment capsule として残します。
研究ロジックのソースコードは `src/` に置き、`experiments/` には置きません。
`scripts/` には、`src/` を呼び出す実行用Pythonスクリプトだけを置きます。
`experiments/` は、どの `scripts/` 経由でどの `src/` コードをどの設定で実行したか、結果がどうだったかを残す場所です。

```text
experiments/
└── exp_YYYYMMDD_001_short_name/
    ├── manifest.md
    ├── config.yaml
    ├── run.sh
    ├── notes.md
    ├── outputs/
    └── snapshot.diff
```

`experiments/` に置いてよい実行ファイルは、原則として `run.sh` だけです。
`run.sh` は研究ロジックを書かず、環境準備、`scripts/` の実行用Pythonスクリプト呼び出し、引数指定だけを行う薄い入口にします。
`scripts/` のPythonスクリプトも研究ロジックを書かず、`src/` の `main()` を呼び出すだけにします。
`src/` を追加または修正した場合は、対応する experiment capsule で検証し、review-gateで採用可否を確認します。

## reproduction

`reproduction/` は、論文に載せる表、図、集約結果を完全再生成する本実験パイプラインです。
`reproduction/run_all.sh` を実行すると、`results/` の成果物が再生成される状態を目指します。

```text
reproduction/
├── README.md
├── config.yaml
├── run_all.sh
├── 00_prepare_data.sh
└── 01_run_main_analysis.sh
```

`reproduction/` には研究ロジックを書きません。
`.sh` ファイルは `scripts/` の実行用Pythonスクリプトを呼び出す薄い入口に限定します。
`scripts/` から呼ばれる `src/` が、論文用の表、図、集約結果を `results/` に直接出力します。
研究ロジックは `src/`、Pythonの実行入口は `scripts/`、論文用成果物は `results/` に分けます。

## results

`results/` は、論文に添付または引用する最終成果物を置く場所です。
予備実験の生出力ではなく、`reproduction/` から再生成された表、図、集約結果だけを置きます。

```text
results/
├── tables/
├── figures/
└── result_index.md
```

`result_index.md` には、各成果物の生成元、対応する `reproduction/` step、出所となる experiment capsule または中間出力、原稿内での使い道を記録します。
`manuscript/` は `experiments/*/outputs/` を直接参照せず、`results/` の成果物を参照します。

## example_project

`example_project/` は、このMVPの動作確認用プロジェクトです。
初期化、先行研究取り込み、`research_state` 更新、experiment capsule、review-gate、manuscript作成の流れを確認するために維持します。
初期状態の `example_project/README.md` は、Codexの判断材料を増やしすぎないよう最小限にします。
研究概要は `example_project/research_plan.md` を正とします。

確認手順：

1. Codexアプリで `example_project/` をワークスペースとして開く。
2. Codexに次を依頼する。

```text
00-project-initializer を実行して。
```

確認するファイル：

```text
example_project/research_state/research_spec.md
example_project/research_state/tasks.md
example_project/research_state/logbook.md
```

## external science-skills

Google DeepMind science-skills は、生命科学・バイオインフォマティクス用の外部参考資料として扱います。
MVPではskill本体を同梱せず、導入案内と使用ポリシーだけを置きます。
参照する場合は `02-research-executor` 経由にします。
`science-skills` 内のPythonファイルは直接実行せず、必要な処理だけを `src/` に実装し、`scripts/` と `experiments/*/run.sh` から再実行できる形にします。
外部APIへローカルデータを送る可能性がある場合は review-gate でHUMAN判定にします。

## 書き方

- すべてのMarkdownファイルは日本語で書きます。
- Markdown内の数式は、VS Code Markdownプレビューで表示しやすい `$...$` と `$$ ... $$` で書きます。`\(...\)` と `\[...\]` は使いません。
- Pythonファイルには、初学者でも目的、入力、出力、処理手順がすぐ理解できる豊富な日本語コメントを残します。
