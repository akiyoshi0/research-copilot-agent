---
name: prior-research-downloader
summary: 先行研究1件分の置き場を作り、合法的に取得できる公開PDFと公開コードdigestを整える。
description: prior_research/<paper_id>/ を作る、metadata.yamlを整える、公開PDFを取得する、PDFをpaper.mdへ変換する、公開コードをcloneせずgitingestでsource.mdへ変換するときに使う。paywall回避、private repo、token利用、ログイン、機関認証の迂回は行わない。
---

# 目的

`prior_research/<paper_id>/` を論文単位の先行研究カプセルとして作成し、合法的に取得できる公開PDFと公開コードdigestを配置する。

# 入力

- `paper_id`
- `metadata.yaml` の `title`
- `metadata.yaml` の `doi`
- `metadata.yaml` の `pmid`
- `metadata.yaml` の `pmcid`
- `metadata.yaml` の `paper_url`
- `metadata.yaml` の `pdf_url`
- `metadata.yaml` の `code_url`

# 出力

```text
prior_research/<paper_id>/
├── paper.pdf
├── paper.md
├── figures/
├── metadata.yaml
├── idea_notes.md
├── source.md
└── source/        # 人間が手動配置した公開コードがある場合だけ使う
```

# 基本コマンド

先行研究カプセルを初期化する。

```bash
uv run python .agents/skills/utilities/prior-research-downloader/scripts/init_prior_research_item.py <paper_id>
```

PDF取得とMarkdown化を実行する。

```bash
uv run python .agents/skills/utilities/prior-research-downloader/scripts/download_prior_research.py prior_research/<paper_id>
```

既存ファイルを上書きする場合だけ `--force` を付ける。

```bash
uv run python .agents/skills/utilities/prior-research-downloader/scripts/download_prior_research.py prior_research/<paper_id> --force
```

PDFだけ扱う場合は `--pdf-only`、コードだけ扱う場合は `--code-only` を使う。
取得だけ行い `paper.md` や `source.md` への変換をしない場合は `--no-ingest` を使う。

# 取得ルール

1. `pdf_url` がある場合は、まずそのURLから `paper.pdf` を取得する。
2. `pdf_url` で取得できない場合は、PMCID、PMID、DOIからPMC Free Full Textを確認する。
3. PMC OA APIでPDFまたはtgz packageが公開されている場合は、本文PDFだけを取得する。
4. PMC経由でも取得できない場合は、Semantic Scholar `openAccessPdf` を確認する。
5. `paper.md` は必ず `paper.pdf` からだけ作る。HTML、XML、abstractだけから `paper.md` を作ってはいけない。
6. 取得できない場合は、手動取得候補URLと保存先を `idea_notes.md` に記録する。

# 公開コードルール

1. `code_url` は `source/` へcloneしない。
2. `code_url` は `gitingest` Python APIへ直接渡し、`source.md` を作る。
3. `gitingest` では1ファイルあたり100KB以下だけをingest対象にする。
4. `100KB` を超えるファイルは `source.md` に入れず、gitingest側のdigest対象外として扱う。
5. `source/` は、人間が手動で公開コードを置いた場合だけ使う。
6. private repository、token、ログイン、機関認証が必要なコードは扱わない。

# 記録ルール

- 取得元、取得結果、失敗理由、変換結果は `metadata.yaml` と `idea_notes.md` に記録する。
- `research_state/logbook.md` は更新しない。
- `title`、DOI、URL、ライセンス表記などの固有情報は原文表記を保つ。
- 説明、メモ、判断、未解決点は日本語で書く。

# 依存関係

- `pymupdf4llm`
- `gitingest`

依存関係がない場合は `uv sync` を促し、勝手に別ツールへフォールバックしない。
helper scriptは `uv run python ...` で実行する。

# 呼び出してよいskill

- `prior-research-ingester`

# 呼び出してはいけないskill

- `02-research-executor`
- `04-manuscript-builder`
- `external/google-deepmind-science-skills`

# 事前にreview-gateが必要な場面

なし。
ただし、有料PDF、private repository、token利用、ログイン、機関認証が必要な取得は `HUMAN` として止める。

# 戻り先

- 通常は取得とingestが終わったら呼び出し元へ戻る。
- `04-manuscript-builder` から引用文献取得のために呼ばれた場合は、`paper.md` 作成後に `04-manuscript-builder` に戻る。

# 更新するファイル

- `prior_research/<paper_id>/metadata.yaml`
- `prior_research/<paper_id>/idea_notes.md`
- `prior_research/<paper_id>/paper.pdf`
- `prior_research/<paper_id>/paper.md`
- `prior_research/<paper_id>/figures/`
- `prior_research/<paper_id>/source.md`

# 失敗時の動作

取得できない場合は理由を `idea_notes.md` に書く。
paywall、ログイン、token、private repository、自動アクセス防御は回避しない。
