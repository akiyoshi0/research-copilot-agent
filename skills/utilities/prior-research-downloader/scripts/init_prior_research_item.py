#!/usr/bin/env python3
"""先行研究1件分のディレクトリを作る。

このファイルの目的:
`prior_research/<paper_id>/` に、論文PDF、Markdown化した論文、
ソースコード、メタデータ、メモを置くための最小構成を作ります。

入力:
paper_id を1つ指定します。

出力:
prior_research/<paper_id>/ の下に `metadata.yaml`, `notes.md`, `source/` を作ります。
既存ファイルは上書きしません。

実行例:
python .agents/skills/utilities/prior-research-downloader/scripts/init_prior_research_item.py paper_a
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    """UTC時刻を文字列で返す。ログに同じ形式で時刻を残すために使う。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def write_if_missing(path: Path, text: str) -> str:
    """ファイルが存在しない場合だけ書き込む。"""
    if path.exists():
        return f"skip  {path}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return f"create {path}"


def build_metadata_text() -> str:
    """metadata.yaml の初期内容を作る。"""
    return """title: ""
authors: []
year: ""
doi: ""
paper_url: ""
pdf_url: ""
code_url: ""
local_pdf: "paper.pdf"
local_paper_markdown: "paper.md"
local_source_dir: "source/"
local_source_markdown: "source.md"
license_note: ""
access_note: ""
ingested_at: ""
"""


def build_notes_text(paper_id: str) -> str:
    """notes.md の初期内容を作る。"""
    return f"""# 先行研究メモ: {paper_id}

## 要点

未記入

## 本研究との関係

未記入

## 再利用できそうな手法

未記入

## 再利用できそうなコード

未記入

## 注意すべき実装

未記入

## ライセンス・利用条件

未記入

## 取得・変換ログ

- {utc_now()}: 先行研究ディレクトリを初期化した。
"""


def append_logbook(project_dir: Path, paper_id: str) -> None:
    """research_state/logbook.md に先行研究初期化ログを追記する。"""
    logbook_path = project_dir / "research_state" / "logbook.md"
    logbook_path.parent.mkdir(parents=True, exist_ok=True)

    line = f"\n## 先行研究初期化: {paper_id}\n\n- 日時: {utc_now()}\n- 内容: `prior_research/{paper_id}/` を作成した。\n"

    if logbook_path.exists():
        with logbook_path.open("a", encoding="utf-8") as file:
            file.write(line)
    else:
        logbook_path.write_text("# Logbook\n" + line, encoding="utf-8")


def init_prior_research_item(project_dir: Path, paper_id: str) -> list[str]:
    """先行研究1件分の最小構成を作る中心処理。"""
    item_dir = project_dir / "prior_research" / paper_id
    source_dir = item_dir / "source"
    messages: list[str] = []

    if item_dir.exists():
        messages.append(f"skip  {item_dir}")
    else:
        item_dir.mkdir(parents=True, exist_ok=True)
        messages.append(f"create {item_dir}")

    if source_dir.exists():
        messages.append(f"skip  {source_dir}")
    else:
        source_dir.mkdir(parents=True, exist_ok=True)
        messages.append(f"create {source_dir}")

    messages.append(write_if_missing(item_dir / "metadata.yaml", build_metadata_text()))
    messages.append(write_if_missing(item_dir / "notes.md", build_notes_text(paper_id)))
    append_logbook(project_dir, paper_id)

    return messages


def main() -> None:
    """コマンドラインから実行されたときの入り口。"""
    parser = argparse.ArgumentParser(description="先行研究1件分の置き場を作ります。")
    parser.add_argument("paper_id", help="先行研究ID。例: paper_a")
    args = parser.parse_args()

    project_dir = Path.cwd()
    messages = init_prior_research_item(project_dir, args.paper_id)

    print("先行研究ディレクトリを初期化しました。")
    for message in messages:
        print(message)


if __name__ == "__main__":
    main()
