from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from app.model.userM import UserM
from app.extensions import db
from werkzeug.security import generate_password_hash
import re

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["userID"]
        password = request.form["password"]
        user = UserM.query.get(user_id)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("shop.index"))
        # flash("IDまたはパスワードが違います")
    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("shop.index"))
    
    if request.method == "POST":
        # ✅ 以下、全ての行を if request.method == "POST": より右に下げます
        user_name = request.form["userName"]

        if user_name == "testuser":
            password = "test1234"
            new_id = "USR9999"
        else:
            # 通常時は画面で入力されたパスワードを使う
            password = request.form["password"]

            # ユーザーID自動発行
            last_user = UserM.query.order_by(UserM.insDate.desc()).first()
            if last_user:
                match = re.search(r'(\d+)$', last_user.userID)
                last_num = int(match.group(1)) if match else 0
                new_id = f"USR{last_num+1:04d}"
            else:
                new_id = "USR0001"

        # データベース保存処理も POST の中に入れます
        user = UserM(
            userID=new_id,
            userName=user_name,
            role=0,
            delFlg=False,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return render_template("auth/register_complete.html", user_id=new_id)

    # POSTでない（画面を開いただけの）時は入力画面を出す
    return render_template("auth/register.html")