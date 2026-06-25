# ROADMAP

Research Co-Pilot Agent は、研究者が主導し、Codexが研究実務を横で支援するためのオープンソース基盤です。
ロードマップでは、完全自動研究者ではなく、監査可能で再現可能な研究並走AIを育てることを優先します。

## 基本方針

- 研究者の判断を中心に置く
- Markdownで読める状態管理を維持する
- 複雑なWeb UI、DB、多数の自律エージェントを追加しない
- 実験、結果、論文主張をreview-gateで確認する
- 論文本文と内部管理情報を分離する
- ローカルデータの外部送信リスクを明示する

## v0.1: 公開MVP

目的は、研究並走ワークスペースの最小構成を公開できる状態にすることです。

- [x] 5 core skills の整備
- [x] 2 utility skills の整備
- [x] 6つの `research_state` ファイルのテンプレート化
- [x] `prior_research/` の論文単位管理
- [x] PDFと公開コードのMarkdown化方針
- [x] experiment capsule の設計
- [x] `src/`、`scripts/`、`experiments/`、`reproduction/`、`results/` の責務分離
- [x] `03-review-gate` のPASS/REVISE/HUMAN/STOP判定
- [x] `04-manuscript-builder` の論文本文ルール
- [x] README、LICENSE、Issueテンプレート、ROADMAP

## v0.2: 初期化と検証の安定化

目的は、生成された研究ワークスペースが常に同じ品質で開始できるようにすることです。

- [ ] `tools/init_research_workspace.py` のテスト追加
- [ ] 生成先ワークスペースのsmoke test追加
- [ ] `.agents/skills/` コピーの整合性チェック
- [ ] テンプレートのMarkdown構文チェック
- [ ] example workflowの最小検証手順をREADMEに追加
- [ ] `uv sync` 後に実行できる検証コマンドの整備

## v0.3: review-gateの品質向上

目的は、Codexが研究上の危険な飛躍を検出しやすくすることです。

- [ ] データリーク確認チェックリストの強化
- [ ] 外部API送信リスクのチェックリスト化
- [ ] `src/` 変更採用時のレビュー観点追加
- [ ] 結果と主張の対応表テンプレート追加
- [ ] manuscriptが作業報告書化していないかの監査強化
- [ ] citation番号とreferencesの整合チェック手順強化

## v0.4: 先行研究ワークフローの強化

目的は、研究者が合法的かつ監査可能に先行研究を扱えるようにすることです。

- [ ] DOI、paper_url、pdf_url、code_urlの記録形式を安定化
- [ ] paywall、ログイン、token利用時のHUMAN判定ルール強化
- [ ] `source.md` 生成時の除外理由レポート改善
- [ ] 100KB制限の動作テスト追加
- [ ] 先行研究からタスク候補を抽出するテンプレート整備

## v0.5: reproductionとmanuscriptの実用化

目的は、論文用成果物を完全再生成し、原稿と対応させる流れを実用レベルに近づけることです。

- [ ] `results/result_index.md` の検証スクリプト追加
- [ ] `manuscript/` から `experiments/*/outputs/` を直接参照していないかのチェック
- [ ] `reproduction/run_all.sh` の標準出力ルール検証
- [ ] 表、図、本文中の参照整合性チェック
- [ ] Methods、Results、Discussionの役割分担レビュー強化

## v0.6: メンテナー体験の改善

目的は、OSSとしてIssue、Pull Request、リリースを継続的に扱える状態にすることです。

- [ ] Pull Requestテンプレートの整備
- [ ] 変更種別ラベルの整理
- [ ] リリースノート雛形の追加
- [ ] 小さな回帰テストセットの追加
- [ ] Codexを使ったIssueトリアージ手順の文書化

## 長期構想

Research Co-Pilot Agent は、研究者を置き換える自律研究システムではありません。
長期的には、次のような「人間主導のAI for Science基盤」を目指します。

- 研究計画から論文草稿までの監査可能な作業ログ
- 研究者が判断を差し戻せるreview-gate
- 先行研究、実験、成果物、原稿の一貫した対応
- ローカルデータを不用意に外へ送らない安全なワークフロー
- 小規模研究室や個人研究者でも使える軽量な研究支援基盤

## ロードマップ外

次は現時点のMVP範囲外です。

- 独自Web UI
- データベース
- ベクトルDB
- クラウド同期
- 自動投稿
- 完全自動研究者
- 多数の自律エージェントによる大規模パイプライン
