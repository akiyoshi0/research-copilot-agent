# AGENTS.md

## 役割

このリポジトリは、Research Co-Pilot Workspace MVP の本体です。
Codexは `PROJECT_BRIEF.md` を正として、実装、テンプレート、skills、example_project を更新します。

## 作業前に読むもの

1. `/Users/akiyoshi/Documents/研究並走エージェント/PROJECT_BRIEF.md`
2. `README.md`
3. `tools/init_research_workspace.py`
4. `templates/`
5. `skills/`
6. `example_project/`

## 作業の原則

- UIはCodexだけにする。
- 独自Web UIやDBを追加しない。
- 本体リポジトリの `skills/` は、生成先 `.agents/skills/` の正本として扱う。
- 本体リポジトリの `templates/` は、生成先Markdown、Mermaid、設定ファイル、`.gitkeep` の正本として扱う。
- 生成先プロジェクトの `scripts/` には研究固有スクリプトだけを置く。
- 本体の初期化処理は `tools/` に置く。
- utility skill の内部処理は各skill配下の `scripts/` に置く。
- すべてのMarkdownファイルは日本語で書く。
- Pythonファイルには、初学者でも目的、入力、出力、処理手順がすぐ理解できる豊富な日本語コメントを残す。
- 依存ライブラリは `uv` で管理する。
- `pip install` ではなく `uv sync` を使う。

## 守る構成

- 5 core skills
- 2 utility skills
- 6 research_state files
- `prior_research/` による論文単位管理
- `experiments/` による experiment capsule
- review-gate による重要局面の確認

## 動作確認

`example_project/` は仕様の一部です。
初期化、先行研究ingest、research_state更新、experiment capsule、review-gate、manuscript計画更新の流れを確認できる状態を保ちます。
