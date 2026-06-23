---
name: 02-research-executor
summary: 承認済みタスクに従って実装、解析、実験を実行する。
description: review-gateでPASSになったタスクを実行するときに使う。研究ロジックはsrcに置き、scriptsにはsrcを呼ぶ薄いCLIだけを置く。予備実験はexperimentsに記録し、論文用の本実験パイプラインはreproductionからresultsを再生成できる形にする。
---

# 目的

承認済みタスクに従い、再現可能な experiment capsule または論文用の本実験パイプラインを作って実行する。

# 入力

- review-gateでPASSになったタスク
- `research_state/tasks.md`
- `research_state/research_spec.md`
- `research_state/logbook.md`

# 出力

- `experiments/exp_YYYYMMDD_001_short_name/`
- `manifest.md`
- `config.yaml`
- `run.sh`
- `notes.md`
- `outputs/`
- `snapshot.diff`
- 必要に応じた `reproduction/run_all.sh`
- 必要に応じた `reproduction/config.yaml`
- 必要に応じた `results/tables/`
- 必要に応じた `results/figures/`
- 必要に応じた `results/result_index.md`
- 必要に応じた `notebooks/` の探索用ノート
- 更新済みの `research_state/logbook.md`

# 手順

1. PASS済みタスクのIDと成功条件を確認する。
2. 予備実験、探索、候補実験の場合は `experiments/` に experiment capsule を作る。
3. 実験条件を `config.yaml` に書く。
4. 必要な研究ロジックは `src/` に追加または修正する。
5. 探索用ノートが必要な場合だけ `notebooks/` に作り、再現に必要な処理は `src/` と `scripts/` に移す。
6. `src/` の `main()` を呼び出す実行用Pythonスクリプトを `scripts/` に書く。
   `scripts/` のPythonスクリプトに研究ロジックを書かない。
7. `scripts/` の実行用Pythonスクリプトを呼び出す再実行コマンドを `run.sh` に書く。
   `run.sh` は環境準備、`scripts/` 呼び出し、引数指定だけに限定し、研究ロジックを書かない。
8. `src/` と `scripts/` の標準出力は、実行開始、完了、出力ファイルパス、件数、最小限の指標、警告、エラーだけに限定する。
   「暫定解釈」「考察」「論文主張」「review-gateで判断」「採用可否」「投稿準備」などの研究運用上の解釈・判断を標準出力に書かない。
9. 実験の目的、仮説、データ、seed、環境、利用した `src/` ファイルと `scripts/` ファイルを `manifest.md` に書く。
10. Google DeepMind science-skills を参照する必要がある場合は、`external/google-deepmind-science-skills/upstream/` を参考資料として読む。
   `upstream/` 内のPythonファイルを直接実行せず、必要な処理だけを `src/` に実装する。
11. 外部実装を参考にした場合は、参照元、ライセンス、変更理由を `manifest.md` と `research_state/logbook.md` に書く。
12. 実験を実行する。
13. 出力を experiment capsule の `outputs/` に保存する。
14. 論文に採用する解析の場合は、`reproduction/` に本実験パイプラインを整理する。
15. `reproduction/run_all.sh` と各stepの `.sh` は、`scripts/` の実行用Pythonスクリプト呼び出しと引数指定だけに限定する。
16. `reproduction/` に `.py`、`.ipynb`、`.R` などの研究ロジック本体を置かない。
17. 論文で使う表、図、集約結果は `results/` に保存する。
18. `results/result_index.md` に、各成果物の生成元、対応する `reproduction/` step、出所となる experiment capsule または中間出力、原稿内での使い道を書く。
19. `manuscript/` から直接 `experiments/*/outputs/` を参照させない。
20. 実験結果と解釈を `manifest.md` と `notes.md` に書く。
21. 研究運用上の判断は、`notes.md`、`research_state/logbook.md`、`research_state/manuscript_plan.md`、`manuscript/`、または `03-review-gate` の出力に分けて書く。
22. 差分を `snapshot.diff` に保存する。
23. `research_state/logbook.md` に実験ログ、`src/` 変更理由、`reproduction/` または `results/` を更新した理由を書く。

# 呼び出してよいskill

- `03-review-gate`

# 参照してよい外部資料

- `external/google-deepmind-science-skills/upstream/`

# 呼び出してはいけないskill

- `04-manuscript-builder` を直接呼び出さない。
- `external/google-deepmind-science-skills/upstream/` 内のskillやPythonファイルを直接実行しない。
- `external/google-deepmind-science-skills/upstream/` 内のPythonファイルを実験の実行入口にしない。
- `reproduction/` に研究ロジックを書かない。
- 出所が `results/result_index.md` に記録されていない成果物を `results/` に置かない。
- `manuscript/` に `experiments/*/outputs/` への直接参照を作らない。
- `src/` や `scripts/` の標準出力に、研究運用上の解釈・判断、原稿本文、review-gate判定を書かない。
- `src/` が生成する要約やレポートに、「暫定解釈」「論文主要主張」「review-gateで判断」などの運用判断を混ぜない。

# 事前にreview-gateが必要な場面

- 大規模実験。
- 外部APIへのローカルデータ送信。
- `src/` 変更の採用判定。
- 論文主張を左右する解析。

# 戻り先

- 実験後は `03-review-gate` に進む。
- 実験修正が必要な場合は `01-task-planner` に戻る。

# 更新するresearch_state

- `logbook.md`
- `state.md`
- `tasks.md`

# 失敗時の動作

失敗した実験も消さずに記録する。
原因、実行コマンド、出力、次に確認することを `manifest.md` と `logbook.md` に書く。
