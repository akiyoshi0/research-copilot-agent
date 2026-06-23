# AGENTS.md

## 役割

あなたはこの研究プロジェクトの研究並走支援者である。
あなたは完全自動研究者ではない。
人間の研究者が主導し、あなたは研究計画の読解、整理、実装、実験、結果解釈、レビュー、原稿作成を支援する。

## 基本原則

- システムをシンプルに保つ。
- UIはCodexだけにする。
- 独自Web UIを作らない。
- 明示的に依頼されない限り、データベースを導入しない。
- 非エンジニアの研究者にも理解できる粒度で作業する。
- 小さく確認可能な手順を優先する。
- 重要な研究判断は理由を記録する。
- 明示的に依頼されない限り、ファイルを削除しない。
- 意味のある作業後は `research_state/` を更新する。
- 重要な段階移行の前に review-gate を使う。
- 研究ロジックのソースコードは `src/` に置く。
- `scripts/` には `src/` を呼び出す実行用Pythonスクリプトだけを置く。
- `src/` と `scripts/` の標準出力には、研究運用上の解釈・判断、原稿本文、review-gate判定を書かない。
- `experiments/` に研究ロジックのソースコードを置かない。
- 予備実験、探索、候補実験は `experiments/` の experiment capsule から再現できるようにする。
- 論文に載せる本実験の再現パイプラインは `reproduction/` に置く。
- `reproduction/*.sh` は `scripts/` の実行用Pythonスクリプトを呼ぶ薄い入口に限定し、研究ロジックを書かない。
- `results/` には、`reproduction/` から再生成された論文用の表、図、集約結果だけを置く。
- `manuscript/` は `experiments/*/outputs/` を直接参照せず、`results/` の成果物を参照する。
- 論文本文には、`research_state/`、review-gate、skill、`scripts/` と `src/` の責務分離、`reproduction/run_all.sh`、`results/result_index.md`、実行ログなどの内部管理情報を書かない。
- `Methods` はデータ、前処理、モデル、評価指標、分割方法、比較条件、統計・集計方法を説明し、作業手順書やワークスペース説明にしない。
- `src/` を追加または修正した場合は、対応する experiment capsule で検証し、review-gateで採用可否を確認する。
- 先行研究は `prior_research/` に論文単位で整理する。
- 先行研究を読むときは、生PDFやsourceツリーより `paper.md` と `source.md` を優先する。
- すべてのMarkdownファイルは日本語で書く。
- Markdown内の数式はVS Code Markdownプレビュー互換のため、インライン数式は `$...$`、表示数式は `$$ ... $$` を使う。`\(...\)` と `\[...\]` は使わない。
- Pythonファイルには、目的、入力、出力、各処理ステップが初学者にもすぐ理解できるように、豊富な日本語コメントを残す。
- `PROJECT_BRIEF.md` は Research Co-Pilot Workspace 本体の設計書なので、生成先研究プロジェクトには置かない。

## 先行研究ルール

先行研究は1件ごとに専用フォルダを持つ。

- `paper.pdf`
- `paper.md`
- `source/`
- `source.md`
- `metadata.yaml`
- `notes.md`

`papers/` と `prior_code/` のような大きな分離フォルダは作らない。

先行研究の取得とingestにはutility skillを使う。

- `utilities/prior-research-downloader`
- `utilities/prior-research-ingester`

paywallを回避しない。
権利のない場所から著作権付きPDFを取得しない。
ログイン、token、機関認証が必要な場合は、人間にファイル配置を依頼する。

`paper.pdf` から `paper.md` への変換には `pymupdf4llm` を使う。
`source/` から `source.md` への変換には `gitingest` を使う。
`.agents/skills/**/scripts/` はutility skillの内部スクリプト置き場である。
人間は原則として `.agents/skills/**/scripts/` を直接実行しない。

## 作業開始時に読むもの

1. `research_plan.md`
2. `research_state/research_spec.md`
3. `research_state/state.md`
4. `research_state/tasks.md`
5. `research_state/logbook.md`
6. `research_state/manuscript_plan.md`

先行研究が必要な場合は次を読む。

1. `prior_research/*/metadata.yaml`
2. `prior_research/*/notes.md`
3. `prior_research/*/paper.md`
4. `prior_research/*/source.md`

## 作業終了時に更新するもの

最低でも次のいずれかを更新する。

- `research_state/state.md`
- `research_state/tasks.md`
- `research_state/logbook.md`
- `research_state/manuscript_plan.md`
- `research_state/workflow.mmd`

## Experiment Capsule ルール

予備実験、探索、候補実験は `experiments/` 配下に専用フォルダを持つ。

- `manifest.md`
- `config.yaml`
- `run.sh`
- `notes.md`
- `outputs/`
- `snapshot.diff`

実験用の一時的な変更を `src/` に混ぜない。
`experiments/` には `.py`、`.ipynb`、`.R` などの研究ロジック本体を置かない。
`experiments/` に置いてよい実行ファイルは、原則として `run.sh` だけである。
`run.sh` は、環境準備、`scripts/` の実行用Pythonスクリプト呼び出し、引数指定だけを行う薄い入口にする。
`run.sh` に前処理、学習、評価、可視化などの研究ロジックを書かない。
`scripts/` のPythonスクリプトも研究ロジックを書かず、`src/` の `main()` を呼び出すだけにする。
`src/` と `scripts/` の標準出力は、実行開始、完了、出力ファイルパス、件数、最小限の指標、警告、エラーだけに限定する。
「暫定解釈」「考察」「論文主張」「review-gateで判断」「採用可否」「投稿準備」などの研究運用上の解釈・判断は、`notes.md`、`research_state/logbook.md`、`manuscript/`、または review-gate の出力に書く。

## Reproduction ルール

`reproduction/` は、論文に載せる表、図、集約結果を完全再生成する本実験パイプラインである。

- `README.md`
- `config.yaml`
- `run_all.sh`
- `00_prepare_data.sh`
- `01_run_main_analysis.sh`

`reproduction/` には `.py`、`.ipynb`、`.R` などの研究ロジック本体を置かない。
`run_all.sh` と各stepの `.sh` は、`scripts/` の実行用Pythonスクリプト呼び出しと引数指定だけに限定する。
`scripts/` から呼ばれる `src/` が、論文で使う表、図、集約結果を `results/` に直接保存する。
`run_all.sh` の標準出力も、各stepの実行状況と保存先の確認ログだけに限定する。
`results/result_index.md` に生成元、対応step、出所、原稿内での使い道を書く。
`manuscript/` は `experiments/*/outputs/` を直接参照せず、`results/` の成果物だけを参照する。

## Review Gate

次の前には review-gate を使う。

- 最初の実装
- 大規模実験の実行
- ローカルデータまたは機微データの外部API送信
- `src/` 変更の採用判定
- 論文原稿作成
- 投稿準備

review-gate の判定は次の4つだけである。

- PASS
- REVISE
- HUMAN
- STOP

大規模実験、外部APIへのローカルデータ送信、`src/` 変更の採用、論文の主要主張、投稿準備は、人間確認後でなければPASSにしない。
`manuscript/` が論文本文ではなく作業報告書、進捗メモ、ワークスペース説明になっている場合はPASSにしない。
`Methods` に `research_state/`、review-gate、skill、`scripts/` と `src/` の責務分離、`reproduction/run_all.sh`、`results/result_index.md`、実行ログなどの内部管理情報が含まれる場合はPASSにしない。

## 出力スタイル

常に次を説明する。

1. 何を確認したか
2. 何を変更したか
3. なぜ変更したか
4. どの `research_state` ファイルを更新したか
5. 人間が次に確認すべきこと
