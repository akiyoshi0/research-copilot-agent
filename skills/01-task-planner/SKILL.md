---
name: 01-task-planner
summary: 次に行う実装タスクと実験タスクを設計する。
description: 初回タスク分解、実験失敗後の再設計、review-gateからの差し戻し時に使う。実験実行やコードの実装、修正は行わない。
---

# 目的

研究計画、現在地、先行研究、過去ログを読み、次に行うタスクを小さく確認可能な単位へ分解する。

# 入力

- `research_plan.md`
- `research_state/research_spec.md`
- `research_state/state.md`
- `research_state/tasks.md`
- `research_state/logbook.md`
- `prior_research/*/metadata.yaml`
- `prior_research/*/idea_notes.md`
- `prior_research/*/paper.md`
- `prior_research/*/source.md`

# 出力

- 更新済みの `research_state/tasks.md`
- 必要に応じた `research_state/state.md`
- 判断理由を追記した `research_state/logbook.md`

# 手順

1. 現在の短期目標とブロッカーを確認する。
2. 研究計画から外れていないか確認する。
3. `prior_research/*/metadata.yaml` と `idea_notes.md` から、取得状況、未解決点、弱点、再利用可能な手法、発展アイデアを確認する。
4. 実装タスクと実験タスクを分ける。
5. 先行研究由来の未解決点や発展案を、研究計画に合う範囲で確認可能なタスクに落とす。
6. 各タスクにID、目的、対象ファイル、成功条件、戻り先を書く。
7. 大規模実験や外部送信が必要な場合は、review-gateでHUMANが必要な点として明記する。
8. `tasks.md` を更新する。
9. 方針確認のため `03-review-gate` に進む。

# 呼び出してよいskill

- `03-review-gate`

# 呼び出してはいけないskill

- `02-research-executor` を直接呼び出さない。

# 事前にreview-gateが必要な場面

- `02-research-executor` へ進む前。
- 大規模実験へ進む前。
- 外部APIへローカルデータを送る前。

# 戻り先

- review-gateでREVISEになった場合は、このskillに戻る。

# 更新するresearch_state

- `tasks.md`
- `state.md`
- `logbook.md`

# 失敗時の動作

研究目的、評価指標、データ利用条件が不明な場合は停止し、`logbook.md` に確認事項を書く。
