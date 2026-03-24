from flask import Flask, render_template
from flask_login import LoginManager
from routes.shop import shop
from routes.checkout import checkout
from routes.admin import admin
from app.model.userM import UserM
from routes.ec003view import ec003view  # 3/24 add kurata

# app __init__を設置することで、extension.py(SQL alchemyをインスタンス化)
from app.model import *


app = Flask(__name__, template_folder="app/templates")

# CSRF保護のためにシークレットキーを作成
app.config['SECRET_KEY'] = 'abc'
# 使用するDBを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
# dbにFlaskアプリを紐付
db.init_app(app)

# ログイン管理システム
login_manager = LoginManager()
login_manager.init_app(app)


# ユーザを識別するための関数
@login_manager.user_loader
def load_user(user_id):
   return db.session.get(UserM, int(user_id))



app.register_blueprint(shop, url_prefix="/shop")
app.register_blueprint(checkout, url_prefix="/checkout")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(ec003view, url_prefix="/ec003view")  # 3/24 add kurata


@app.route("/")
def index():
    return render_template("base.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


  