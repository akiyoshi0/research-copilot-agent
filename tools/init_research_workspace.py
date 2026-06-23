#!/usr/bin/env python3
"""Research Co-Pilot Workspace 用の研究プロジェクトを初期化する。

このファイルの目的:
研究者が使う新しい研究プロジェクトのディレクトリを作り、
README、AGENTS、research_state、skills などの最小構成を配置します。

入力:
--project-name で作成する研究プロジェクト名を指定します。

出力:
指定した研究プロジェクトディレクトリの中に、研究並走用のファイルと
フォルダを作ります。既存ファイルは上書きしません。

実行例:
python tools/init_research_workspace.py --project-name my_project
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


# このスクリプトは research-copilot-mvp/tools/ にあります。
# parents[1] は research-copilot-mvp/ を指します。
ROOT_DIR = Path(__file__).resolve().parents[1]

# 生成先にコピーするMarkdownや空ディレクトリの正本です。
TEMPLATE_DIR = ROOT_DIR / "templates"

# 生成先の .agents/skills/ にコピーするskillの正本です。
SKILLS_DIR = ROOT_DIR / "skills"


# 研究プロジェクトに必ず作るディレクトリです。
# scripts/ は研究固有スクリプト用なので、初期状態では .gitkeep だけを置きます。
PROJECT_DIRS = [
    "prior_research",
    "data",
    "src",
    "scripts",
    "notebooks",
    "experiments",
    "reproduction",
    "results",
    "manuscript",
    "research_state",
    ".agents/skills",
]


# 生成先にコピーするトップレベルMarkdownです。
TOP_LEVEL_TEMPLATE_FILES = [
    "README.md",
    "AGENTS.md",
    "research_plan.md",
]


# research_state は6ファイルだけに絞ります。
RESEARCH_STATE_FILES = [
    "research_spec.md",
    "state.md",
    "tasks.md",
    "logbook.md",
    "manuscript_plan.md",
    "workflow.mmd",
]


# 生成先にコピーするskillです。
# external は参照ドキュメントだけを置き、MVPの必須実行要件にはしません。
SKILL_PATHS = [
    "00-project-initializer",
    "01-task-planner",
    "02-research-executor",
    "03-review-gate",
    "04-manuscript-builder",
    "utilities/prior-research-downloader",
    "utilities/prior-research-ingester",
    "external/google-deepmind-science-skills",
]


def should_skip_path(path: Path) -> bool:
    """コピーしないファイルやディレクトリかどうかを判定する。

    研究者に不要なキャッシュやOS固有ファイルを生成先に混ぜないための関数です。
    """
    skip_names = {".DS_Store", "__pycache__"}
    return any(part in skip_names for part in path.parts) or path.suffix == ".pyc"


def copy_file_if_missing(source: Path, destination: Path) -> str:
    """ファイルが存在しない場合だけコピーする。

    既存ファイルを上書きしないことで、研究者が書いた内容を守ります。
    """
    if destination.exists():
        return f"skip  {destination}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return f"create {destination}"


def copy_tree_if_missing(source_dir: Path, destination_dir: Path) -> list[str]:
    """ディレクトリ内のファイルを、存在しないものだけコピーする。

    shutil.copytree ではなく1ファイルずつコピーすることで、
    既に編集済みのファイルを壊さないようにします。
    """
    messages: list[str] = []

    for source in sorted(source_dir.rglob("*")):
        if source.is_dir() or should_skip_path(source):
            continue

        relative_path = source.relative_to(source_dir)
        destination = destination_dir / relative_path
        messages.append(copy_file_if_missing(source, destination))

    return messages


def create_project_directories(target: Path) -> list[str]:
    """研究プロジェクトに必要なディレクトリを作る。"""
    messages: list[str] = []

    if target.exists():
        messages.append(f"skip  {target}")
    else:
        target.mkdir(parents=True, exist_ok=True)
        messages.append(f"create {target}")

    for directory_name in PROJECT_DIRS:
        directory = target / directory_name
        if directory.exists():
            messages.append(f"skip  {directory}")
        else:
            directory.mkdir(parents=True, exist_ok=True)
            messages.append(f"create {directory}")

    return messages


def copy_templates(target: Path) -> list[str]:
    """README、research_state、.gitkeep などのテンプレートをコピーする。"""
    messages: list[str] = []

    for file_name in TOP_LEVEL_TEMPLATE_FILES:
        source = TEMPLATE_DIR / file_name
        destination = target / file_name
        messages.append(copy_file_if_missing(source, destination))

    for file_name in RESEARCH_STATE_FILES:
        source = TEMPLATE_DIR / "research_state" / file_name
        destination = target / "research_state" / file_name
        messages.append(copy_file_if_missing(source, destination))

    # 空ディレクトリをGitで保持できるように .gitkeep を置きます。
    for directory_name in ["prior_research", "data", "src", "scripts", "notebooks", "experiments", "results", "manuscript"]:
        source = TEMPLATE_DIR / directory_name / ".gitkeep"
        destination = target / directory_name / ".gitkeep"
        messages.append(copy_file_if_missing(source, destination))

    # reproduction/ はREADMEを持つため、ディレクトリ全体をコピーします。
    # ここには研究ロジックを置かず、本実験パイプラインの説明だけを初期配置します。
    messages.extend(copy_tree_if_missing(TEMPLATE_DIR / "reproduction", target / "reproduction"))

    return messages


def copy_skills(target: Path) -> list[str]:
    """本体リポジトリのskillsを、生成先の .agents/skills/ にコピーする。"""
    messages: list[str] = []
    destination_root = target / ".agents" / "skills"

    for skill_path in SKILL_PATHS:
        source_dir = SKILLS_DIR / skill_path
        destination_dir = destination_root / skill_path

        if not source_dir.exists():
            messages.append(f"missing {source_dir}")
            continue

        messages.extend(copy_tree_if_missing(source_dir, destination_dir))

    return messages


def init_workspace(target: Path) -> list[str]:
    """研究ワークスペースを初期化する中心処理。"""
    messages: list[str] = []
    messages.extend(create_project_directories(target))
    messages.extend(copy_templates(target))
    messages.extend(copy_skills(target))
    return messages


def main() -> None:
    """コマンドラインから実行されたときの入り口。"""
    parser = argparse.ArgumentParser(description="研究並走ワークスペースを初期化します。")
    parser.add_argument("--project-name", required=True, help="作成する研究プロジェクトのディレクトリ名")
    args = parser.parse_args()

    # expanduser は ~ をホームディレクトリに変換します。
    # resolve は絶対パスに変換します。
    target = Path(args.project_name).expanduser().resolve()

    messages = init_workspace(target)

    print("研究ワークスペースを初期化しました。")
    for message in messages:
        print(message)


if __name__ == "__main__":
    main()
