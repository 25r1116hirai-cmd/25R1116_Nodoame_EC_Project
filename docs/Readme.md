# 25R1116_Nodoame_EC_Project (Naniwa Select Shop)

FlaskとSQLAlchemyを使用した、シンプルでモダンなECサイトシステムです。

## 🚀 起動手順

システムをローカル環境で起動する方法は以下の通りです。

1. **ターミナルを起動**し、プロジェクトのルートディレクトリに移動します。
   ```powershell
   cd C:\Users\25R1116\Documents\25R1116_Nodoame_EC_Project\EC-site-project
2. `python app.py` を実行
3. ブラウザで `http://127.0.0.1:5000/` にアクセス


## 🔑 テスト用アカウント情報
- user_name == "testuser"
- password = "test1234"
- new_id = "USR9999"
- 
## 管理者メニューや注文データの確認には、以下の共通アカウントをご利用ください。
## 管理者（動作確認ガイド）
- 管理者アカウント
- ID: admin

- PW: admin123
1. ログインをし注文管理画面で注文内容や発送が押せる。
2. 
3. 商品管理画面にとぶと商品画像の変更や在庫の数詳細など変更可能。

## 🛒 ショッピングの流れ（動作確認ガイド）
1. 商品を選ぶ

2. トップ画面の「おすすめ商品」や一覧から、気になるアイテムをクリックします。

3. カートへ追加

4. 商品詳細画面で「数量」を選び、[カートに追加する] ボタンを押します。

5. 注文情報の入力

6. カート画面へ進み、配送先の 「名前」「住所」 および 「クレジットカード番号」 を入力します。

7. 注文確定と確認



## 🛠 使用技術
- Language: Python 3.14

- Framework: Flask

- ORM/Database: Flask-SQLAlchemy / SQLite

- Design: HTML, CSS



QA課題表のリンク
https://docs.google.com/spreadsheets/d/1pl8aFd5A04VsWQjRm03YsGW4YoKyYEwS2or4Z3iEC40/edit?usp=sharing

テスト仕様書 テスト結果へのリンク
https://docs.google.com/spreadsheets/d/1CfAcZ2rC3W4w2lZo-Z8VwrI_Stryo0uMcseVlyBZQv4/edit?usp=sharing

