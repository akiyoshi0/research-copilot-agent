---
name: 00-project-initializer
summary: 研究計画と先行研究を読み、research_stateの初期状態を作る。
description: 研究プロジェクト開始時、または research_state を作り直す必要があるときに使う。実装、実験、論文の原稿作成は行わない。
---

# 目的

`research_plan.md` と `prior_research/` を読み、研究の仕様と最初のタスク候補を日本語で整理する。

# 入力

- `research_plan.md`
- `prior_research/*/metadata.yaml`
- `prior_research/*/paper.md`
- `prior_research/*/source.md`
- `prior_research/*/notes.md`

# 出力

- `research_state/research_spec.md`
- `research_state/state.md`
- `research_state/tasks.md`
- `research_state/logbook.md`
- `research_state/manuscript_plan.md`
- `research_state/workflow.mmd`

# 手順

1. `research_plan.md` を読む。
2. 研究目的、仮説、データ、手法、評価指標、成功条件を抽出する。
3. `prior_research/` のメタデータとMarkdown化済みファイルを読む。
4. `paper.md` や `source.md` がない場合は、utility skill の `prior-research-ingester` 利用を提案する。
5. 不明点は推測で埋めず、「不明」と書く。
6. `research_state/` の6ファイルを初期化する。
7. 最初のタスク候補を `tasks.md` に書く。
8. 初期化内容を `logbook.md` に記録する。

# 呼び出してよいskill

- `01-task-planner`
- `utilities/prior-research-ingester`

# 呼び出してはいけないskill

- `02-research-executor`
- `04-manuscript-builder`
- `external/google-deepmind-science-skills`

# 事前にreview-gateが必要な場面

なし。

# 戻り先

- 初期化後は `01-task-planner` に進む。
- 先行研究のMarkdown化が必要な場合は `utilities/prior-research-ingester` に戻る。

# 更新するresearch_state

- `research_spec.md`
- `state.md`
- `tasks.md`
- `logbook.md`
- `manuscript_plan.md`
- `workflow.mmd`

# 失敗時の動作

必要な入力がない場合は停止し、`research_state/logbook.md` に理由を明確に書く。
静かに推測して進めない。
