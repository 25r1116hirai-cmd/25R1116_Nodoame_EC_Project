from datetime import datetime
import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user,current_user
from routes.form import ItemForm
import uuid
#DBのテーブルとDB操作のファイルをインポート
from app.model.itemM import ItemM
from app.model.userM import UserM
from app.model.orderH import OrderH
from app.extensions import db


admin = Blueprint("admin",__name__)


@admin.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userID = request.form["login_id"]
        password = request.form["password"]

        user = UserM.query.filter_by(userID=userID).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.order"))  # 管理画面へ

        flash("ログイン失敗", "danger")

    return render_template("admin/login.html")


# 注文情報の仮データ
# データベースができたら削除します
orders = [
    {
        "id": 1001,
        "name": "佐藤 太郎",
        "address": "東京都新宿区...",
        "items": "商品A×2, 商品B×1",
        "total": 5500,
        "shipped": False
    },
    {
        "id": 1002,
        "name": "鈴木 花子",
        "address": "大阪府大阪市...",
        "items": "商品C×1",
        "total": 3000,
        "shipped": False
    },
    {
        "id": 1003,
        "name": "田中 一郎",
        "address": "北海道札幌市...",
        "items": "商品B×3, 商品D×1",
        "total": 7800,
        "shipped": False
    }
]

# ----------------------------------------------------
# 注文管理画面
# ----------------------------------------------------
# 注文管理画面(orders.htmlへ遷移)
## 更新ボタンを押すと発送済みは下に、未発送は上に並び替えるロジック追加
@admin.route("/orders")
@login_required
def order():
    # 管理者権限チェック
    if current_user.role != 1:
        flash("管理者専用ページです", "danger")
        return redirect(url_for("shop.index"))

    sort = request.args.get("sort")

    # DBから注文取得
    display_orders = OrderH.query.all()

    # 並び替え
    if sort == "true":
        display_orders = sorted(display_orders, key=lambda x: (x.shipFlg, x.orderId))

    return render_template("admin/orders.html", orders=display_orders)


# 注文管理画面内にて発送状況を切り替えるロジック
@admin.route("/toggle/<int:order_id>", methods=["POST"])
def toggle_status(order_id):
    for order in orders:
        if order["id"] == order_id:
            order["shipped"] = not order["shipped"]
            break
    return redirect(url_for("admin.order"))


# ----------------------------------------------------
# 商品管理画面
# ----------------------------------------------------

# 商品管理画面(admin/items.htmlへ移動)
# 未削除のデータを上に、削除済のデータを下に並び替えするロジック込み
@admin.route("/items")
@login_required
def list_items():
    items = ItemM.query.order_by(ItemM.delFlg.asc(), ItemM.insDate.desc()).all()
    return render_template("admin/items.html", items=items)

# ----------------------------------------------------
# 商品新規登録画面
# ----------------------------------------------------

# 商品新規登録画面(product.htmlへ遷移)
# 商品create
@admin.route("/items/create", methods=["GET", "POST"])
@login_required
def product():
    form = ItemForm()

    if request.method == "POST":
        itemName = form.itemName.data
        categoryName = form.categoryName.data
        itemDetail = form.itemDetail.data
        price = form.price.data
        taxRate = float(form.taxRate.data) #文字列でくるため、変換
        stock = form.stock.data
        recmdFlg = form.recmdFlg.data

        #1. 画像の取得
        file = form.imageFile.data
        # 画像がある場合
        if file:
            #2. 画像ファイル名の取得
            filename = file.filename
            #3. static/img/配下にアップロードされたファイル名を追加。
            # DBにパスのみ img直下に画像が入ります。
            save_path = os.path.join(current_app.static_folder, 'img', filename)
            #4. 画像のパス保存する
            file.save(save_path)
        else:
            filename = None

        # itemId はここで生成（例: 自動採番や規則に合わせて）
        item = ItemM(
            itemName=itemName,
            categoryName=categoryName,
            itemDetail=itemDetail,
            price=price,
            taxRate=taxRate,
            stock=stock,
            recmdFlg=recmdFlg,
            imageName=filename
        )

        db.session.add(item)
        db.session.commit()
        return redirect(url_for("admin.list_items"))

    return render_template("admin/product.html", form=form)



@admin.route("/items/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    item = ItemM.query.get_or_404(item_id)
    # 論理削除フラグON
    item.delFlg = True
    item.updDate = datetime.now()
    
    db.session.commit()
    return redirect(url_for("admin.list_items"))


# ----------------------------------------------------
# 商品編集画面
# ----------------------------------------------------
# 編集画面
# 更新成功時は一覧画面へ遷移
# 更新失敗時は遷移せずエラーメッセージを表示
@admin.route("/items/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = ItemM.query.get_or_404(item_id)

    if request.method == "POST":
        # フォームの値を更新
        item.itemName = request.form["itemName"]
        item.itemDetail = request.form["itemDetail"]
        item.categoryName = request.form["categoryName"]
        item.price = int(request.form["price"])
        item.taxRate = float(request.form["taxRate"])
        item.stock = int(request.form["stock"])
        item.recmdFlg = "recmdFlg" in request.form
        item.updDate = datetime.now()  # 更新日時

        # -------- 画像更新 --------
        file = request.files.get("imageFile")
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"

            save_path = os.path.join(current_app.static_folder, 'img', filename)
            file.save(save_path)

            item.imageName = filename

        # -------- 保存 --------
        try:
            db.session.commit()
            flash("商品を更新しました", "success")
            return redirect(url_for("admin.list_items"))

        except Exception as e:
            db.session.rollback()
            flash(f"更新失敗: {e}", "danger")

    return render_template("admin/edit_item.html", item=item)












