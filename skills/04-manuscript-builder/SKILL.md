---
name: 04-manuscript-builder
summary: research_stateとresultsをもとに論文計画と原稿を作る。
description: review-gateで原稿作成へ進んでよいと判断された後に使う。根拠のない主張や存在しない結果を書かない。
---

# 目的

研究結果、先行研究、根拠表をもとに、論文原稿と `manuscript_plan.md` を更新する。

# 入力

- `research_state/manuscript_plan.md`
- `research_state/logbook.md`
- `results/`
- `results/result_index.md`
- `prior_research/*/paper.md`
- `experiments/*/manifest.md`
- `experiments/*/notes.md`

# 出力

- `manuscript/introduction.md`
- `manuscript/methods.md`
- `manuscript/results.md`
- `manuscript/discussion.md`
- `manuscript/references.md`
- 更新済みの `research_state/manuscript_plan.md`

# 手順

1. 研究目的と成功条件を確認する。
2. 先行研究の根拠を確認する。
3. 自分たちの結果を `results/` と `results/result_index.md` から確認する。
4. 主張と根拠を `manuscript_plan.md` に整理する。
5. `results/result_index.md` を使い、各成果物の生成元、対応する `reproduction/` step、出所となる experiment capsule または中間出力、原稿内での使い道を確認する。
6. `manuscript_plan.md` に `Results章構成案` を作る。
7. `Results章構成案` では、各小見出しについて対応method、対応experiment capsule、対応する `reproduction/` step、使う `results/` 成果物、metrics、figure/table、主張、制限を書く。
8. `manuscript/results.md` は `Results章構成案` の順番と対応関係に従って書く。
9. `results/result_index.md`、experiment capsule、`research_state/`、`reproduction/` は根拠確認のために読むが、論文本文には内部管理情報として書かない。
10. 原稿向けの解釈、主張、本文は `manuscript/` と `research_state/manuscript_plan.md` に書き、`src/` や `scripts/` の標準出力、実行ログ、生成レポートへ逆流させない。
11. 引用に必要な論文が `prior_research/` にない場合は、候補論文、必要理由、既知のDOIまたはURLを `manuscript_plan.md` に書く。
12. 合法的に取得できる DOI、paper_url、pdf_url が分かっている場合だけ、`utilities/prior-research-downloader` を使う。
13. 取得後は `utilities/prior-research-ingester` で `paper.md` を作る。
14. `paper.md` が作成されるまでは、その論文を引用根拠として本文に断定を書かない。
15. 論文各セクションの下書きを作る。
16. `manuscript/references.md` に番号付き参考文献リストを作る。
17. `introduction.md`, `methods.md`, `results.md`, `discussion.md` の引用箇所に対応する引用番号を書く。
18. 本文中の引用番号と `references.md` の番号が一対一に対応しているか確認する。
19. 数式はVS Code Markdownプレビュー互換の記法で書く。
20. 根拠がない主張には「根拠不足」と書く。
21. 必要な表、図、集約結果が `results/` にない場合は、原稿で作ったことにせず、`02-research-executor` または `03-review-gate` に戻す不足事項として記録する。
22. 投稿準備へ進む前に `03-review-gate` を呼ぶ。

# 論文本文ルール

論文本文には、研究内容を理解するために必要な情報だけを書く。

```text
- Introduction: 背景、先行研究、研究ギャップ、目的、限定した主張
- Methods: データ、前処理、モデル、評価指標、分割方法、比較条件、統計・集計方法
- Results: 得られた数値、表、図、観察結果
- Discussion: 結果の意味、先行研究との関係、限界、今後の課題
```

`Methods` には、ワークスペース運用、ファイル管理、スキル運用、review-gate、実行ログの扱いを書かない。
再現性に関する実装上の詳細は、論文本文ではなく `README.md`、`results/result_index.md`、`research_state/logbook.md`、補足資料、または Code and data availability 相当の短い節に分ける。

# 内部管理情報の扱い

次は原稿を書くための確認材料であり、論文本文にそのまま書かない。

```text
- Research Co-Pilot Workspace
- research_state/
- review-gate
- skill
- PROJECT_BRIEF.md
- AGENTS.md
- scripts/ と src/ の責務分離
- reproduction/run_all.sh
- results/result_index.md
- experiment capsule
- outputs/reports/summary.md
- 実行ログの扱い
```

これらを本文に書く必要がある場合は、論文本文ではなく、README、補足資料、Code and data availability に相当する短い節として扱う。

# Results章構成ルール

`manuscript/results.md` を書く前に、必ず `research_state/manuscript_plan.md` に `Results章構成案` を作る。

各小見出しには、少なくとも次を記録する。

```text
- 小見出し
- 対応するmethod
- 対応するexperiment capsule
- 対応するreproduction step
- 使うresults成果物
- 主要指標
- 補助指標
- figure/table
- 本文で述べる主張
- 制限または注意点
```

`results.md` では、`Results章構成案` にない結果を新しく主張しない。
methodで説明していない解析結果をresultsに出さない。
数値は `results/`, `results/result_index.md`, `manifest.md`, `notes.md`, 出所となる中間出力の記録と一致させる。
原稿に添付または引用する表、図、集約結果は `results/` に存在する成果物だけを使う。
`manuscript/` から `experiments/*/outputs/` を直接参照しない。

# 引用番号ルール

- `manuscript/references.md` は `[1]`, `[2]`, `[3]` のような番号付きリストにする。
- 本文中の引用は `[1]` または `[1,2]` のように書く。
- 本文中のすべての引用番号は `references.md` に存在しなければならない。
- `references.md` の各番号は、本文中の少なくとも1箇所で引用されていなければならない。
- 同じ論文には原稿全体で同じ番号を使う。
- 番号は原則として本文で初出する順に付ける。
- `references.md` にだけ存在し、本文中で使われない参考文献を残さない。

# Markdown数式ルール

- インライン数式は `$...$` を使う。
- 表示数式は `$$ ... $$` を使う。
- `\(...\)` と `\[...\]` は使わない。
- 文字としてのドル記号は、必要に応じて `\$` のようにエスケープする。
- 例: `$F_\beta$`

```text
$$
F_1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}
$$
```

# 呼び出してよいskill

- `03-review-gate`
- `utilities/prior-research-downloader`
- `utilities/prior-research-ingester`

# 呼び出してはいけないskill

- `02-research-executor` を直接呼び出さない。
- 未取得または未ingestの論文を引用根拠として扱わない。
- 本文中に対応番号のない参考文献を `references.md` に置かない。
- `references.md` に存在しない番号を本文中で引用しない。
- `results/` に存在しない表、図、集約結果を原稿に添付したことにしない。
- `experiments/*/outputs/` を原稿から直接参照しない。
- 原稿本文、Results/Discussionの解釈、引用説明を `src/` や `scripts/` の標準出力、実行ログ、生成レポートに書かない。
- `research_state/`、review-gate、skill、`scripts/` と `src/` の責務分離、`reproduction/run_all.sh`、`results/result_index.md`、実行ログなどの内部管理情報を、論文本文の `Introduction`、`Methods`、`Results`、`Discussion` に書かない。
- `Methods` を作業手順書、成果物管理メモ、ワークスペース説明にしない。
- paywall回避、private repository、token利用、ログインが必要な取得を人間確認なしに行わない。

# 事前にreview-gateが必要な場面

- 原稿作成を開始する前。
- 有料PDF、private repository、token利用、ログインが必要な引用文献取得へ進む前。
- 投稿準備へ進む前。
- 論文の主要主張を強める前。

# 戻り先

- 追加実験が必要な場合は `01-task-planner` に戻る。
- 引用に必要な論文の取得またはingestが必要な場合は `utilities/prior-research-downloader` または `utilities/prior-research-ingester` に戻る。
- 原稿だけの修正ならこのskillに戻る。

# 更新するresearch_state

- `manuscript_plan.md`
- `logbook.md`
- `state.md`

# 失敗時の動作

必要な結果や根拠がない場合は、原稿に断定を書かず、`manuscript_plan.md` に不足している実験または引用候補を書く。
