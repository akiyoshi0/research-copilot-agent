#!/usr/bin/env python3
"""先行研究PDFとソースコードをMarkdown化する。

このファイルの目的:
`prior_research/<paper_id>/paper.pdf` を `paper.md` に変換し、
`prior_research/<paper_id>/source/` を `source.md` に変換します。

入力:
prior_research/<paper_id> のディレクトリを指定します。

出力:
- paper.md
- source.md
- metadata.yaml の ingested_at 更新
- notes.md の変換ログ
- research_state/logbook.md の変換ログ

実行例:
python .agents/skills/utilities/prior-research-ingester/scripts/ingest_prior_research.py prior_research/paper_a
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MAX_SOURCE_FILE_BYTES = 100 * 1024


def utc_now() -> str:
    """UTC時刻を文字列で返す。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def append_text(path: Path, text: str) -> None:
    """ファイルにテキストを追記する。なければ作る。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        with path.open("a", encoding="utf-8") as file:
            file.write(text)
    else:
        path.write_text(text, encoding="utf-8")


def load_pymupdf4llm():
    """pymupdf4llm を読み込む。見つからない場合は理由を出して止める。"""
    try:
        import pymupdf4llm  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "pymupdf4llm が見つかりません。\n"
            "このプロジェクトでは pip install ではなく uv sync を使います。"
        ) from exc
    return pymupdf4llm


def load_gitingest():
    """gitingest を読み込む。見つからない場合は理由を出して止める。"""
    try:
        from gitingest import ingest  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "gitingest が見つかりません。\n"
            "このプロジェクトでは pip install ではなく uv sync を使います。"
        ) from exc
    return ingest


def format_bytes(size: int) -> str:
    """バイト数を、人間が読みやすいKB表記に変換する。"""
    return f"{size / 1024:.1f}KB"


def prepare_small_source_tree(source_dir: Path, filtered_dir: Path) -> tuple[int, list[str]]:
    """100KB以下のファイルだけを、一時ディレクトリへ同じ階層構造でコピーする。

    gitingest に元の source/ をそのまま渡すと、大きなnotebook、データ、
    モデルファイルなどが source.md に入り、Codexが読むには重くなりすぎる。
    そのため、ここで1ファイル100KB以下のものだけを明示的に選別する。
    """
    copied_count = 0
    skipped_messages: list[str] = []

    for path in sorted(source_dir.rglob("*")):
        if not path.is_file():
            continue

        relative_path = path.relative_to(source_dir)
        file_size = path.stat().st_size

        if file_size > MAX_SOURCE_FILE_BYTES:
            skipped_messages.append(
                f"`source/{relative_path}` は {format_bytes(file_size)} で100KBを超えるため source.md から除外した。"
            )
            continue

        destination = filtered_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        copied_count += 1

    return copied_count, skipped_messages


def convert_paper(item_dir: Path) -> str:
    """paper.pdf があれば paper.md に変換する。"""
    pdf_path = item_dir / "paper.pdf"
    output_path = item_dir / "paper.md"

    if not pdf_path.exists():
        return "paper.pdf がないため論文Markdown化をスキップした。"

    try:
        pymupdf4llm = load_pymupdf4llm()
        body = pymupdf4llm.to_markdown(str(pdf_path))
    except Exception as exc:
        return f"paper.pdf のMarkdown化に失敗した: {exc}"

    header = f"""# 論文Markdown

## メタ情報

- PDFファイル: `{pdf_path}`
- Markdown変換日: {utc_now()}
- 変換ライブラリ: pymupdf4llm

## 本文

"""
    output_path.write_text(header + body, encoding="utf-8")
    return f"paper.md を作成した: `{output_path}`"


def convert_source(item_dir: Path) -> list[str]:
    """source/ があれば source.md に変換する。"""
    source_dir = item_dir / "source"
    output_path = item_dir / "source.md"

    if not source_dir.exists() or not any(source_dir.iterdir()):
        return ["source/ が空または存在しないためコードMarkdown化をスキップした。"]

    with tempfile.TemporaryDirectory(prefix="research_source_ingest_") as temp_dir_name:
        filtered_dir = Path(temp_dir_name) / "source"
        copied_count, skipped_messages = prepare_small_source_tree(source_dir, filtered_dir)

        if copied_count == 0:
            messages = ["source/ に100KB以下のファイルがないため source.md 作成をスキップした。"]
            messages.extend(skipped_messages)
            return messages

        try:
            ingest = load_gitingest()
            summary, tree, content = ingest(str(filtered_dir))
        except Exception as exc:
            messages = [f"source/ のMarkdown化に失敗した: {exc}"]
            messages.extend(skipped_messages)
            return messages

    text = f"""# ソースコードMarkdown

## メタ情報

- 入力ディレクトリ: `{source_dir}`
- Markdown変換日: {utc_now()}
- 変換ライブラリ: gitingest
- ingest対象: 1ファイルあたり100KB以下のファイルのみ
- ingest対象ファイル数: {copied_count}

## Summary

{summary}

## Directory Tree

{tree}

## Files

{content}
"""
    output_path.write_text(text, encoding="utf-8")
    messages = [f"source.md を作成した: `{output_path}`"]
    messages.extend(skipped_messages)
    return messages


def update_ingested_at(metadata_path: Path) -> str:
    """metadata.yaml の ingested_at を更新する。"""
    now = utc_now()

    if not metadata_path.exists():
        metadata_path.write_text(f'ingested_at: "{now}"\n', encoding="utf-8")
        return "metadata.yaml を作成し、ingested_at を記録した。"

    lines = metadata_path.read_text(encoding="utf-8").splitlines()
    updated_lines: list[str] = []
    replaced = False

    for line in lines:
        if line.startswith("ingested_at:"):
            updated_lines.append(f'ingested_at: "{now}"')
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        updated_lines.append(f'ingested_at: "{now}"')

    metadata_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    return "metadata.yaml の ingested_at を更新した。"


def append_logs(item_dir: Path, project_dir: Path, messages: list[str]) -> None:
    """notes.md と logbook.md に変換結果を記録する。"""
    paper_id = item_dir.name
    text = "\n## 変換ログ\n\n" + f"- 日時: {utc_now()}\n" + "".join(f"- {message}\n" for message in messages)

    append_text(item_dir / "notes.md", text)

    logbook_text = f"\n## 先行研究ingest: {paper_id}\n\n" + f"- 日時: {utc_now()}\n" + "".join(f"- {message}\n" for message in messages)
    append_text(project_dir / "research_state" / "logbook.md", logbook_text)


def ingest_prior_research(item_dir: Path) -> list[str]:
    """先行研究1件をMarkdown化する中心処理。"""
    if not item_dir.exists():
        raise SystemExit(f"先行研究ディレクトリが見つかりません: {item_dir}")

    project_dir = item_dir.parents[1]
    messages = [convert_paper(item_dir)]
    messages.extend(convert_source(item_dir))
    messages.append(update_ingested_at(item_dir / "metadata.yaml"))
    append_logs(item_dir, project_dir, messages)
    return messages


def main() -> None:
    """コマンドラインから実行されたときの入り口。"""
    parser = argparse.ArgumentParser(description="先行研究PDFとソースコードをMarkdown化します。")
    parser.add_argument("item_dir", help="prior_research/<paper_id> のディレクトリ")
    args = parser.parse_args()

    item_dir = Path(args.item_dir).expanduser().resolve()
    messages = ingest_prior_research(item_dir)

    print("先行研究ingest処理を完了しました。")
    for message in messages:
        print(message)


if __name__ == "__main__":
    main()
