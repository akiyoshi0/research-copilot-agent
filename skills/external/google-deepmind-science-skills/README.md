# Google DeepMind science-skills 連携

このディレクトリは、Google DeepMind science-skills を外部参考資料として扱う場合の案内だけを置く場所です。
MVPの必須要件としてはskill本体を同梱しません。

公式bundleを導入した場合は、このディレクトリ内の `upstream/` に配置します。
`upstream/` は外部公式bundleとして扱い、このプロジェクトの 5 core skills + 2 utility skills には数えません。

参照する場合は、必ず `02-research-executor` 経由で扱います。
`upstream/` 内のskillやPythonファイルは直接実行しません。
必要な処理は `upstream/` の実装を参考にして `src/` に実装し、`scripts/` と `experiments/*/run.sh` から再実行できる形にします。
外部APIへローカルデータを送る可能性がある場合は、review-gateでHUMAN判定にして人間へ確認します。
