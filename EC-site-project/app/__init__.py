print("--- 初期化処理実行 ---")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# サーバー設定
app = Flask("app")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['DEBUG'] = True
app.config['PORT'] = 7777
app.config['HOST'] = "localhost"
# Sessionのシークレットキー
app.secret_key = b"abc"
# Flaskインスタンスと連動設定
db = SQLAlchemy(app)

# DBへmodelの設定
from app.src.model import *

# DBの初期化
with app.app_context():
    db.create_all()

from app import main