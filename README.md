# スニーカーサイト データベースセットアップ手順

## 前提条件
- PostgreSQLがインストールされていること
- psqlコマンドラインツールが利用可能であること

## セットアップ手順

1. PostgreSQLにログイン
```bash
psql -U postgres
```

2. データベースの作成
```sql
CREATE DATABASE sneaker_db;
```

3. データベースに接続
```sql
\c sneaker_db
```

4. スキーマの適用
```bash
psql -U postgres -d sneaker_db -f schema.sql
```

## データベースの確認

1. テーブル一覧の確認
```sql
\dt
```

2. ブランドデータの確認
```sql
SELECT * FROM brands;
```

3. スニーカーデータの確認
```sql
SELECT * FROM sneakers;
```

## データベース接続情報

アプリケーションの設定（app.py）で使用する接続情報：
- データベース名: sneaker_db
- ユーザー名: postgres
- パスワード: （PostgreSQLのインストール時に設定したパスワード）
- ホスト: localhost
- ポート: 5432

## トラブルシューティング

1. データベース接続エラーが発生する場合
   - PostgreSQLサービスが起動していることを確認
   - 接続情報（ユーザー名、パスワード）が正しいことを確認
   - データベースが存在することを確認

2. テーブルが作成されない場合
   - schema.sqlの実行権限を確認
   - エラーメッセージを確認して、具体的な問題を特定

## データベースのバックアップとリストア

バックアップの作成：
```bash
pg_dump -U postgres sneaker_db > backup.sql
```

バックアップからのリストア：
```bash
psql -U postgres sneaker_db < backup.sql
``` 
