# keiba-sheet
競馬予想シート作成ツール

# 開発

コンテナを起動する

```bash
docker compose up
```

任意のファイルを実行する

```bash
docker compose exec playwright python hello.py
```

# 使用方法

## netkeibaから出馬表を作る

こんな感じで。CSV形式で標準出力に吐かれるのでリダイレクトするなりなんなりと。

```bash
docker compose exec playwright python netkeiba.py <race_id>
# 例：2025年皐月賞
# docker compose exec playwright python netkeiba.py 202506030811
```