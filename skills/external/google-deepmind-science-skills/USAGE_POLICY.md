# 使用ポリシー

## 基本方針

- `upstream/` 内のskillやPythonファイルは直接実行しない。
- `upstream/` は外部参考資料として読み、必要な処理だけを `src/` に実装する。
- 実装した処理は `scripts/` の薄いCLIと `experiments/*/run.sh` から再実行できる形にする。
- 外部実装を参考にした場合は、参照元、ライセンス、変更理由を `manifest.md` と `research_state/logbook.md` に記録する。

## Level 1: 自動参照OK

- 公開文献検索
- 公開DB参照
- 遺伝子・タンパク質情報確認

## Level 2: 参照後にlogbook.mdへ記録

- ClinVar
- gnomAD
- GTEx
- AlphaFold DB
- ChEMBL
- PubChem

## Level 3: review-gateでHUMAN必須

- API keyが必要な処理
- 外部APIへローカルデータを送る処理
- 臨床データや個人情報に関わる処理
- 大量実行
- 論文主張を左右する解析
