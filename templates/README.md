# 研究プロジェクト

このディレクトリは、Research Co-Pilot Workspace で進める研究プロジェクトです。
研究者が方針を決め、Codex が整理、実装、実験、記録、レビュー、原稿作成を支援します。

## 最初に読むもの

1. `AGENTS.md`
2. `README.md`
3. `research_plan.md`
4. `research_state/state.md`
5. `research_state/tasks.md`

## 最初に行うこと

1. `research_plan.md` に研究計画を書く
2. 必要な先行研究を `prior_research/` に論文単位で置く
3. Codex に「00-project-initializer を実行して。」と依頼する
4. Codex が作った `research_state/` を人間が確認する
5. review-gate を通して最初の実装・実験へ進む

Codexへの最初の指示例：

```text
00-project-initializer を実行して。
```

ここでの「実行」は、OSコマンドではなく `.agents/skills/00-project-initializer/` のskillとして作業する、という意味です。

## prior_research の置き方

先行研究は1件ごとに専用フォルダを作ります。

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

PDFやコードの取得にログイン、token、機関認証が必要な場合は、Codexが勝手に取得せず、人間が合法的に配置します。

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
実処理は `.agents/skills/utilities/` 配下のutility skill内部スクリプトが担当します。

## 実験の置き方

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

## 本実験と論文用成果物

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

## external science-skills

Google DeepMind science-skills はMVPの必須実行要件ではありません。
初期状態では参照ドキュメントだけを置きます。
外部APIへローカルデータを送る可能性がある場合は、review-gateでHUMAN判定にします。

## 書き方

- Markdown は日本語で書きます。
- Markdown内の数式は、VS Code Markdownプレビューで表示しやすい `$...$` と `$$ ... $$` で書きます。`\(...\)` と `\[...\]` は使いません。
- Python には、初学者でも目的、入力、出力、処理の流れがすぐ理解できる日本語コメントを十分に書きます。
