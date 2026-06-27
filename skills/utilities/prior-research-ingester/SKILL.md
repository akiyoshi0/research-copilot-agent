---
name: prior-research-ingester
summary: prior_research内のPDFと公開コードをCodexが読みやすいMarkdownへ変換する。
description: paper.pdfをpaper.mdへ変換し、metadata.yamlのcode_urlまたは手動配置されたsource/をgitingestでsource.mdへ変換するときに使う。paper.mdは必ずpaper.pdfから作り、公開コードはcloneせずsource.mdとしてdigest化する。
---

# 目的

`prior_research/<paper_id>/` の論文PDFと公開コードを、Codexが読みやすいMarkdown成果物へ変換する。

# 入力

```text
prior_research/<paper_id>/
├── paper.pdf
├── metadata.yaml
└── source/        # 人間が手動配置した公開コードがある場合だけ
```

`metadata.yaml` に `code_url` がある場合は、`source/` がなくてもURLを `gitingest` に直接渡して `source.md` を作る。

# 出力

```text
prior_research/<paper_id>/
├── paper.md
├── figures/
├── source.md
├── metadata.yaml
└── idea_notes.md
```

# 基本コマンド

PDFと公開コードdigestを両方作る。

```bash
uv run python .agents/skills/utilities/prior-research-ingester/scripts/ingest_prior_research.py prior_research/<paper_id>
```

既存の `paper.md` または `source.md` を上書きする場合だけ `--force` を付ける。

```bash
uv run python .agents/skills/utilities/prior-research-ingester/scripts/ingest_prior_research.py prior_research/<paper_id> --force
```

PDFだけ変換する場合は `--pdf-only`、コードだけ変換する場合は `--source-only` を使う。

# PDF変換ルール

1. `paper.pdf` がある場合だけ `paper.md` を作る。
2. `paper.md` は `pymupdf4llm.to_markdown(...)` で作る。
3. PDF内画像は `figures/` にPNGとして保存する。
4. `pymupdf4llm` がない場合は、別ツールへ勝手に切り替えない。
5. HTML、XML、abstract、出版社ページ本文から `paper.md` を作ってはいけない。

# 公開コード変換ルール

1. `metadata.yaml` の `code_url` がある場合、`gitingest` Python APIへ直接渡して `source.md` を作る。
2. `source/` がある場合は、手動配置された公開コードとして `gitingest` Python APIへ渡す。
3. `gitingest` の `max_file_size` は `100KB` にする。
4. `source.md` には、1ファイルあたり100KB以下の内容だけを含める。
5. `gitingest` がない場合は、別方式の手製digestへフォールバックしない。
6. private repository、token、ログイン、機関認証が必要なコードは扱わない。

# 記録ルール

- 変換結果、失敗理由、スキップ理由は `idea_notes.md` に記録する。
- `metadata.yaml` の `ingested_at` を更新する。
- `research_state/logbook.md` は更新しない。
- 説明、メモ、判断、未解決点は日本語で書く。

# 依存関係

- `pymupdf4llm`
- `gitingest`

依存関係がない場合は `uv sync` を促し、勝手に別ツールへフォールバックしない。
helper scriptは `uv run python ...` で実行する。

# 呼び出してよいskill

なし。

# 呼び出してはいけないskill

- `02-research-executor`
- `04-manuscript-builder`
- `external/google-deepmind-science-skills`

# 事前にreview-gateが必要な場面

なし。

# 戻り先

- `00-project-initializer`
- `01-task-planner`
- `04-manuscript-builder` から引用文献取得のために呼ばれた場合は、`paper.md` 作成後に `04-manuscript-builder` に戻る。

# 更新するファイル

- `prior_research/<paper_id>/paper.md`
- `prior_research/<paper_id>/figures/`
- `prior_research/<paper_id>/source.md`
- `prior_research/<paper_id>/metadata.yaml`
- `prior_research/<paper_id>/idea_notes.md`

# 失敗時の動作

PDF変換やsource変換に失敗した場合は、理由を `idea_notes.md` に書く。
勝手に別ツールへ切り替えない。
