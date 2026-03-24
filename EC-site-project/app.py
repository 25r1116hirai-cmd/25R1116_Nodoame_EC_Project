from flask import Flask, render_template
from routes.shop import shop
from routes.checkout import checkout
from routes.admin import admin
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


  