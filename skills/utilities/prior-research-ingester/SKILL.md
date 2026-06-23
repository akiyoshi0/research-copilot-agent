---
name: prior-research-ingester
summary: prior_research内のPDFとソースコードをCodexが読みやすいMarkdownに変換する。
description: paper.pdfをpaper.mdへ、source/をsource.mdへ変換するときに使う。変換に失敗した場合は理由をnotes.mdとlogbook.mdへ記録する。
---

# 目的

`prior_research/<paper_id>/` のPDFとソースコードを、Codexが読みやすいMarkdownに変換する。

# 入力

```text
prior_research/<paper_id>/
├── paper.pdf
└── source/
```

# 出力

```text
prior_research/<paper_id>/
├── paper.md
├── source.md
├── metadata.yaml
└── notes.md
```

# 手順

1. `paper.pdf` があれば pymupdf4llm で `paper.md` に変換する。
2. `source/` があれば、1ファイルあたり100KB以下のファイルだけを gitingest で `source.md` に変換する。
3. 100KBを超えるファイルは `source.md` に入れず、スキップ理由を `notes.md` と `research_state/logbook.md` に書く。
4. `metadata.yaml` に `ingested_at` を書く。
5. `notes.md` に変換ログを書く。
6. `research_state/logbook.md` に外部ツール利用履歴を書く。

# 呼び出してよいskill

なし。

# 呼び出してはいけないskill

- `02-research-executor`
- `04-manuscript-builder`

# 事前にreview-gateが必要な場面

なし。

# 戻り先

- `00-project-initializer`
- `01-task-planner`
- `04-manuscript-builder` から引用文献取得のために呼ばれた場合は、`paper.md` 作成後に `04-manuscript-builder` に戻る。

# 更新するresearch_state

- `logbook.md`

# 失敗時の動作

PDF変換やsource変換に失敗した場合は、理由を `notes.md` と `research_state/logbook.md` に書く。
勝手に別ツールへ切り替えない。
