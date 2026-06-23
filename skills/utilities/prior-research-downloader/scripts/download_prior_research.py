#!/usr/bin/env python3
"""metadata.yaml を見て、取得可能な先行研究PDFと公開コードを配置する。

このファイルの目的:
`prior_research/<paper_id>/metadata.yaml` に書かれた `pdf_url` と
`code_url` を読み、取得可能なものを `paper.pdf` と `source/` に保存します。

入力:
prior_research/<paper_id> のディレクトリを指定します。

出力:
- paper.pdf
- source/
- notes.md の取得ログ
- research_state/logbook.md の取得ログ

注意:
paywall、ログイン、token、private repository が必要そうな場合は停止します。
"""

from __future__ import annotations

import argparse
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    """UTC時刻を文字列で返す。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def read_simple_metadata(metadata_path: Path) -> dict[str, str]:
    """metadata.yaml から単純な key: value 形式だけを読む。

    PyYAMLを依存に増やさないため、MVPでは必要なキーだけを簡単に読みます。
    authors のような配列は、このスクリプトでは使いません。
    """
    metadata: dict[str, str] = {}

    if not metadata_path.exists():
        raise SystemExit(f"metadata.yaml が見つかりません: {metadata_path}")

    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue

        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata


def append_text(path: Path, text: str) -> None:
    """ファイルにテキストを追記する。なければ作る。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        with path.open("a", encoding="utf-8") as file:
            file.write(text)
    else:
        path.write_text(text, encoding="utf-8")


def looks_private_or_token_url(url: str) -> bool:
    """認証情報が含まれていそうなURLかどうかを簡単に判定する。"""
    lowered = url.lower()
    return "@" in url or "token=" in lowered or "access_token=" in lowered or "private" in lowered


def download_pdf(pdf_url: str, destination: Path) -> str:
    """PDFをpaper.pdfとして保存する。"""
    if not pdf_url:
        return "pdf_url が空なのでPDF取得をスキップした。"

    if looks_private_or_token_url(pdf_url):
        return "pdf_url に認証情報またはprivateを示す文字列があるため停止した。"

    if destination.exists():
        return f"`{destination}` が既に存在するためPDF取得をスキップした。"

    try:
        with urllib.request.urlopen(pdf_url, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()
    except Exception as exc:
        return f"PDF取得に失敗した: {exc}"

    if b"<html" in data[:500].lower() and "pdf" not in content_type.lower():
        return "PDFではなくHTMLが返った可能性があるため保存しなかった。ログインやpaywallの可能性がある。"

    destination.write_bytes(data)
    return f"PDFを取得した: `{destination}`"


def clone_public_code(code_url: str, destination: Path) -> str:
    """公開Gitリポジトリをsource/へcloneする。"""
    if not code_url:
        return "code_url が空なのでコード取得をスキップした。"

    if looks_private_or_token_url(code_url):
        return "code_url に認証情報またはprivateを示す文字列があるため停止した。"

    if destination.exists() and any(destination.iterdir()):
        return f"`{destination}` に既にファイルがあるためコード取得をスキップした。"

    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", code_url, str(destination)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "git コマンドが見つからないためコード取得に失敗した。"
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip()
        return f"コード取得に失敗した: {message}"

    return f"コードを取得した: `{destination}`"


def append_logs(item_dir: Path, project_dir: Path, messages: list[str]) -> None:
    """notes.md と research_state/logbook.md に取得結果を記録する。"""
    paper_id = item_dir.name
    text = "\n## 取得ログ\n\n" + f"- 日時: {utc_now()}\n" + "".join(f"- {message}\n" for message in messages)

    append_text(item_dir / "notes.md", text)

    logbook_text = f"\n## 先行研究取得: {paper_id}\n\n" + f"- 日時: {utc_now()}\n" + "".join(f"- {message}\n" for message in messages)
    append_text(project_dir / "research_state" / "logbook.md", logbook_text)


def download_prior_research(item_dir: Path) -> list[str]:
    """先行研究PDFとコードを取得する中心処理。"""
    metadata = read_simple_metadata(item_dir / "metadata.yaml")
    project_dir = item_dir.parents[1]

    pdf_url = metadata.get("pdf_url", "")
    code_url = metadata.get("code_url", "")

    messages = [
        download_pdf(pdf_url, item_dir / "paper.pdf"),
        clone_public_code(code_url, item_dir / "source"),
    ]

    append_logs(item_dir, project_dir, messages)
    return messages


def main() -> None:
    """コマンドラインから実行されたときの入り口。"""
    parser = argparse.ArgumentParser(description="metadata.yaml を見て先行研究PDFとコードを取得します。")
    parser.add_argument("item_dir", help="prior_research/<paper_id> のディレクトリ")
    args = parser.parse_args()

    item_dir = Path(args.item_dir).expanduser().resolve()
    messages = download_prior_research(item_dir)

    print("先行研究取得処理を完了しました。")
    for message in messages:
        print(message)


if __name__ == "__main__":
    main()
