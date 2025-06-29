# CLAUDE.md

このファイルは、このリポジトリでClaude Code (claude.ai/code)が作業する際のガイダンスを提供します。

## 概要

netkeibaから競馬の出馬表データをスクレイピングしてCSV形式で出力する予想シート作成ツールです。DockerコンテナでPlaywrightを使用してブラウザを自動化し、BeautifulSoupでHTMLをパースしています。

## よく使うコマンド

### Dockerコンテナの起動
```bash
docker compose up
```

### コンテナ内でスクリプトを実行
```bash
# hello.pyテストスクリプトの実行
docker compose exec playwright python hello.py

# netkeibaスクレイパーの実行
docker compose exec playwright python netkeiba.py <race_id>
# 例：2025年皐月賞
docker compose exec playwright python netkeiba.py 202506030811
```

### 新しいPythonパッケージのインストール
1. `playwright/requirements.txt`にパッケージを追加
2. コンテナを再ビルド: `docker compose build`

## プロジェクトアーキテクチャ

シンプルなコンテナ化されたアーキテクチャを採用：

- **Docker Compose**: Python 3.13を搭載したPlaywrightコンテナを管理
- **メインスクリプト**: `netkeiba.py` - レースIDを引数に取り、CSVデータを出力
- **主要ロジック**: `stable_disp`関数で遠征でない厩舎に「+」マークを付与（栗東厩舎が阪神・京都で走る場合、美浦厩舎が東京・中山で走る場合）
- **出力形式**: 枠番、馬番、馬名、性齢、斤量、騎手、厩舎、調教師、馬体重、オッズ、人気を含むCSV

## ディレクトリ構造

- `/playwright/` - Dockerコンテナ設定とアプリケーションコード
  - `/app/` - メインのPythonスクリプト
  - `/app/tmp/` - 一時ファイル（スクリーンショット）
  - `requirements.txt` - Python依存関係
- `/venv/` - ローカルPython仮想環境（Docker使用時は不要）

## 依存関係

- playwright - ブラウザ自動化
- beautifulsoup4 - HTMLパース
- python-dotenv - 環境変数管理
- pytest-playwright - テストフレームワーク（テストは未実装）

## 備考

- DockerコンテナでPlaywrightのChromiumブラウザを使用
- スクレイピング時にスクリーンショットが`playwright/app/tmp/`に保存される
- `.gitignore`に`.ruff_cache/`が含まれているため、将来的にRuffでのリンティングが想定される
