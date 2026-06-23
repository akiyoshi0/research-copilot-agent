# Reproduction

このディレクトリは、論文に載せる表、図、集約結果を完全再生成する本実験パイプラインを置く場所です。

- `run_all.sh`: 論文用成果物を `results/` に再生成する入口
- `config.yaml`: 本実験パイプラインの設定
- `00_*.sh`, `01_*.sh`: `scripts/` の実行用Pythonスクリプトを呼ぶ薄いstep

ここに研究ロジックを書きません。
研究ロジックは `src/`、Pythonの実行入口は `scripts/`、論文用成果物は `results/` に置きます。
論文用の表、図、集約結果は、`scripts/` から呼ばれる `src/` が `results/` に直接出力します。
