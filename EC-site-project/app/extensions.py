# SQLAlchemyのインスタンス（DB操作用）を作成
# このdbはアプリ全体で共有される共通のDBオブジェクト
# 各モデルファイルで import して同じDBを使うために定義しています。


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()