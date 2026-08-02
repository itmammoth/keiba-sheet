# Repository Guidelines

## プロジェクト構成

このリポジトリは、netkeiba の出馬表を取得して CSV または Google Sheets に出力する Python ツールです。

- `compose.yaml`: Playwright コンテナの起動定義。
- `playwright/Dockerfile`: Python 3.13 / Playwright 実行環境。
- `playwright/requirements.txt`: コンテナに入れる Python 依存関係。
- `playwright/app/netkeiba.py`: CLI、スクレイピング、CSV 出力の主処理。
- `playwright/app/sheets_uploader.py`: Google Sheets API へのシート作成・書込み。
- `playwright/app/hello.py`: Playwright の動作確認用スクリプト。

スクリーンショットなどの実行時ファイルは `playwright/app/tmp/` に置き、追跡しません。

## 開発・実行コマンド

まずコンテナを起動します。

```bash
docker compose up
```

別ターミナルから、コンテナ内でスクリプトを実行します。

```bash
docker compose exec playwright python hello.py
docker compose exec playwright python netkeiba.py 202506030811
docker compose exec playwright python netkeiba.py 202506030811 --upload
```

依存関係を追加・変更したら `playwright/requirements.txt` を更新し、`docker compose build` でイメージを再作成してください。

## コーディング規約

Python は 4 スペースでインデントし、PEP 8 を基本に読みやすい小さな関数を維持します。関数・変数は `snake_case`、クラスは `PascalCase`、定数は `UPPER_SNAKE_CASE` を使用します。型ヒントは既存コードにならい public 関数の引数・戻り値に付けます。Ruff の設定ファイルはまだないため、導入時は設定と実行手順を同時に追加してください。

## テスト

`pytest-playwright` は依存関係にありますが、現時点で自動テストはありません。ロジックを追加・変更する際は、ネットワークに依存しない `pytest` テストを `playwright/app/tests/test_<対象>.py` に追加し、コンテナ内で `pytest` を実行してください。スクレイパー変更時は、代表的なレース ID で CSV の列順・件数を手動確認します。

## 設定と機密情報

Sheets 連携には `playwright/app/.env.sample` を参考に `.env` を作成し、`GOOGLE_SHEETS_SPREADSHEET_ID` を設定します。サービスアカウント鍵 `keiba-sheet-py-key.json`、`.env`、取得データやスクリーンショットをコミットしないでください。エラー出力や PR に認証情報を貼り付けることも禁止です。

## コミットとプルリクエスト

既存履歴は短い日本語の命令形・要約（例: `印カラムを追加`、`バージョン固定`）が中心です。この形式で、1 コミットを 1 つの目的に絞ります。PR には変更の目的、動作確認コマンドと結果、外部出力や画面に影響する変更では CSV 例またはスクリーンショットを添えてください。
