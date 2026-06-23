---
name: prior-research-downloader
summary: 先行研究1件分の置き場を作り、取得可能なPDFや公開コードを配置する。
description: prior_research/<paper_id>/ を作る、metadata.yamlを整える、合法的に取得可能なPDFや公開コードを配置するときに使う。paywall回避、private repo、token利用は人間確認なしに行わない。
---

# 目的

論文PDFと先行研究ソースコードを `prior_research/<paper_id>/` に配置する。

# 入力

- paper_id
- pdf_url
- code_url
- doi
- paper_url

# 出力

```text
prior_research/<paper_id>/
├── paper.pdf
├── source/
├── metadata.yaml
└── notes.md
```

# 手順

1. `prior_research/<paper_id>/` を作る。
2. `metadata.yaml` を作る、または更新する。
3. `pdf_url` があり、合法的に取得可能なら `paper.pdf` として保存する。
4. `code_url` が公開GitHub等なら `source/` に取得する。
5. 取得元、取得日時、ライセンス注意を `notes.md` に書く。
6. `research_state/logbook.md` に記録する。

# 呼び出してよいskill

- `prior-research-ingester`

# 呼び出してはいけないskill

- `02-research-executor`
- `04-manuscript-builder`

# 事前にreview-gateが必要な場面

なし。
ただし、有料PDF、private repository、token利用、ログインが必要な取得はHUMANとして止める。

# 戻り先

- 取得後に `prior-research-ingester` を提案する。
- `04-manuscript-builder` から引用文献取得のために呼ばれた場合は、ingest完了後に `04-manuscript-builder` に戻る。

# 更新するresearch_state

- `logbook.md`

# 失敗時の動作

取得できない場合は、理由を `notes.md` と `research_state/logbook.md` に書く。
paywallや認証を回避しない。
