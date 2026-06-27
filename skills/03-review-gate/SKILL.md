---
name: 03-review-gate
summary: 方針、実験、結果、外部送信、src変更、論文主張を確認する。
description: 重要な段階移行の前後に使う。判定はPASS、REVISE、HUMAN、STOPの4つだけにする。
---

# 目的

研究計画とのズレ、再現性、データ安全性、結果解釈、`src/` 変更の採用可否、論文主張の根拠を確認する。

# 入力

- `research_state/research_spec.md`
- `research_state/state.md`
- `research_state/tasks.md`
- `research_state/logbook.md`
- experiment capsule
- 必要に応じて `reproduction/`
- 必要に応じて `results/` と `results/result_index.md`
- 必要に応じて `manuscript/`
- 必要に応じて `prior_research/*/metadata.yaml`
- 必要に応じて `prior_research/*/idea_notes.md`
- 必要に応じて `prior_research/*/paper.md`

# 出力

- 判定
- 理由
- 戻る先
- 修正タスク
- 人間が確認すべき点
- 更新すべき `research_state` ファイル

# 手順

1. 研究計画とズレていないか確認する。
2. 評価指標、baseline、データリークを確認する。
3. seed、環境、commit、実行コマンドが記録されているか確認する。
4. experiment capsule が十分か確認する。
5. 研究ロジックが `src/` にあり、`experiments/` にソースコード本体が置かれていないか確認する。
6. Google DeepMind science-skills を参考にした場合、`upstream/` 内のskillやPythonファイルを直接実行していないか確認する。
7. science-skillsを参考にした処理が、必要最小限だけ `src/` に実装され、`scripts/` と `experiments/*/run.sh` または `reproduction/run_all.sh` から再実行できる形になっているか確認する。
8. science-skillsを参考にした場合、参照元、ライセンス、変更理由が `manifest.md` と `research_state/logbook.md` に記録されているか確認する。
9. `src/` と `scripts/` の標準出力、`run.sh`、`reproduction/run_all.sh`、`outputs/reports/` に、研究運用上の解釈・判断が混ざっていないか確認する。
10. 標準出力が、実行開始、完了、出力ファイルパス、件数、最小限の指標、警告、エラーに限定されているか確認する。
11. 結果解釈に飛躍がないか確認する。
12. `research_state/manuscript_plan.md` に `Results章構成案` があるか確認する。
13. `manuscript/results.md` が `Results章構成案` の順番と対応関係に従っているか確認する。
14. results章の各小見出しが、対応method、experiment capsule、`reproduction/` step、`results/` 成果物、figure/table、主張、制限と対応しているか確認する。
15. methodで説明していない解析結果がresultsに出ていないか確認する。
16. 論文に使う表、図、集約結果が `results/` に存在するか確認する。
17. `reproduction/run_all.sh` から `results/` の成果物を再生成できるか確認する。
18. `reproduction/*.sh` が `scripts/` の実行用Pythonスクリプト呼び出しだけに限定され、研究ロジックを含まないか確認する。
19. `results/result_index.md` に、各成果物の生成元、対応する `reproduction/` step、出所となる experiment capsule または中間出力、原稿内での使い道が記録されているか確認する。
20. `manuscript/` が `experiments/*/outputs/` を直接参照していないか確認する。
21. resultsの数値が `results/`, `results/result_index.md`, `manifest.md`, `notes.md`, 出所となる中間出力と一致しているか確認する。
22. `manuscript/` が作業報告書ではなく、論文として成立する構成と文体になっているか確認する。
23. `Introduction` が背景、先行研究、研究ギャップ、目的、限定した主張を説明しているか確認する。
24. `Methods` がデータ、前処理、モデル、評価指標、分割方法、比較条件、統計・集計方法を説明しているか確認する。
25. `Methods` に `research_state/`、review-gate、skill、`scripts/` と `src/` の責務分離、`reproduction/run_all.sh`、`results/result_index.md`、実行ログなどの内部管理情報が混入していないか確認する。
26. `Results` が結果の提示を主とし、Discussionで扱うべき解釈、限界、今後の課題を過度に混ぜていないか確認する。
27. `Discussion` が結果の意味、先行研究との関係、限界、今後の課題を扱っているか確認する。
28. `Abstract`、`Introduction`、`Methods`、`Results`、`Discussion` の主張が一貫しているか確認する。
29. 論文本文に「ワークスペース」「作業ログ」「review-gate」「skill」「research_state」「PROJECT_BRIEF」「AGENTS.md」など、読者に不要な内部運用語が混入していないか確認する。
30. 外部送信リスクを確認する。
31. 論文主張と根拠が対応しているか確認する。
32. 引用された論文が `prior_research/*/paper.md` としてingest済みか確認する。
33. 引用された論文の `metadata.yaml` と `idea_notes.md` を読み、取得元、アクセス条件、ライセンス注意、取得・変換ログが根拠として妥当か確認する。
34. 未取得または未ingestの論文を根拠にした断定がないか確認する。
35. 本文中の引用番号が `manuscript/references.md` の番号付き参考文献リストと対応しているか確認する。
36. `references.md` の各番号が本文中で少なくとも1回引用されているか確認する。
37. ライセンス上の問題がないか確認する。
38. 4つの判定から1つだけ選ぶ。

# 論文としての批評観点

`manuscript/` を確認する場合は、研究運用の整合性だけでなく、論文として読めるかを批評する。

```text
- 論文本文が作業報告、進捗メモ、ワークスペース説明になっていないか
- Abstractが目的、方法、主要結果、限定した結論を簡潔に含むか
- Introductionが背景、先行研究、研究ギャップ、研究目的を自然につなげているか
- Methodsが研究の再現に必要な科学的方法を説明しており、内部ファイル管理の説明になっていないか
- Resultsが表や図に対応する結果を提示し、考察を過剰に先取りしていないか
- Discussionが結果の意味、先行研究との関係、限界、今後の課題を述べているか
- section間で主張、用語、指標、表番号、引用番号が一貫しているか
- すべての主張が `results/` または `prior_research/` の根拠に対応しているか
- 論文読者に不要な内部運用語が本文に残っていないか
```

# 判定

```text
PASS
REVISE
HUMAN
STOP
```

大規模実験、外部APIへのローカルデータ送信、`src/` 変更の採用、論文の主要主張、投稿準備は、人間確認後でなければPASSにしない。
Google DeepMind science-skills の `upstream/` 内にあるskillやPythonファイルを直接実行していた場合はPASSにしない。
その場合はREVISEとして、必要な処理を `src/` に実装し直し、`scripts/` と `experiments/*/run.sh` または `reproduction/run_all.sh` から再実行できる形へ戻す。
外部APIへのローカルデータ送信やAPI key利用が絡む場合はHUMANにする。
未取得または未ingestの論文を根拠にした断定がある場合はPASSにしない。
本文中の引用番号と `manuscript/references.md` の番号付き参考文献リストが対応していない場合はPASSにしない。
`Results章構成案` がない、または `results.md` が構成案、method、experiment capsule、`results/` の成果物と対応していない場合はPASSにしない。
論文に使う表、図、集約結果が `results/` に存在しない場合はPASSにしない。
`reproduction/run_all.sh` から `results/` の成果物を再生成できない場合はPASSにしない。
`reproduction/` に研究ロジック本体が置かれている場合はPASSにしない。
`results/result_index.md` に成果物の出所と原稿内での使い道が記録されていない場合はPASSにしない。
`manuscript/` が `experiments/*/outputs/` を直接参照している場合はPASSにしない。
`src/` や `scripts/` の標準出力、`run.sh`、`reproduction/run_all.sh`、`outputs/reports/` に、研究運用上の解釈・判断、原稿本文、review-gate判定が含まれる場合はPASSにしない。
その場合はREVISEとして、数値や成果物の生成処理と、解釈・判断を書く場所を分離する。
`manuscript/` が論文本文ではなく作業報告書、進捗メモ、ワークスペース説明になっている場合はPASSにしない。
`Methods` に `research_state/`、review-gate、skill、`scripts/` と `src/` の責務分離、`reproduction/run_all.sh`、`results/result_index.md`、実行ログなどの内部管理情報が含まれる場合はPASSにしない。
`Introduction`、`Methods`、`Results`、`Discussion` の役割分担が崩れている場合はPASSにしない。
その場合はREVISEとして、`04-manuscript-builder` に戻し、内部管理情報を本文から除去して論文構成へ書き直す。

# 呼び出してよいskill

- `01-task-planner`
- `02-research-executor`
- `04-manuscript-builder`

# 呼び出してはいけないskill

なし。

# 事前にreview-gateが必要な場面

このskill自体がreview-gateである。

# 戻り先

- 実験修正時は `01-task-planner`
- 原稿だけの修正時は `04-manuscript-builder`
- HUMANまたはSTOPの場合は停止して人間に確認する

# 更新するresearch_state

- `logbook.md`
- `state.md`
- `tasks.md`
- 必要に応じて `manuscript_plan.md`

# 失敗時の動作

必要な情報が足りない場合は、判定をHUMANまたはREVISEにし、不足情報を `logbook.md` に書く。
