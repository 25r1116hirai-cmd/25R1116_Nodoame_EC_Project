from datetime import datetime
import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from routes.form import ItemForm
import uuid
#DBのテーブルとDB操作のファイルをインポート
from app.model.itemM import ItemM
from app.extensions import db


admin = Blueprint("admin",__name__)

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
# 商品の仮データ
# データベースができたら削除します
products = [
    {
        "id": 2001,
        "category": "食品",
        "name": "りんごジュース",
        "description": "青森県産りんごを使用した100%ジュース",
        "tax_rate": 8,
        "stock": 50,
        "is_recommended": False,
        "image_url": "/static/img/apple_juice.jpg",
        "is_deleted": False,
        "updated_at": "2026-03-20",
        "created_at": "2026-03-01"
    },
    {
        "id": 2002,
        "category": "食品",
        "name": "みかんゼリー",
        "description": "国産みかんをたっぷり使用したゼリー",
        "tax_rate": 8,
        "stock": 30,
        "is_recommended": False,
        "image_url": "/static/img/mikan_jelly.jpg",
        "is_deleted": False,
        "updated_at": "2026-03-18",
        "created_at": "2026-03-05"
    },
    {
        "id": 2003,
        "category": "飲料",
        "name": "緑茶ペットボトル",
        "description": "無添加・無糖のすっきりした味わい",
        "tax_rate": 10,
        "stock": 100,
        "is_recommended": False,
        "image_url": "/static/img/green_tea.jpg",
        "is_deleted": False,
        "updated_at": "2026-03-15",
        "created_at": "2026-02-25"
    },
    {
        "id": 2004,
        "category": "菓子",
        "name": "チョコレートクッキー",
        "description": "サクサク食感の手作りクッキー",
        "tax_rate": 10,
        "stock": 0,
        "is_recommended": False,
        "image_url": "/static/img/cookie.jpg",
        "is_deleted": False,
        "updated_at": "2026-03-10",
        "created_at": "2026-02-20"
    },
    {
        "id": 2005,
        "category": "食品",
        "name": "レトルトカレー",
        "description": "スパイス香る本格カレー",
        "tax_rate": 10,
        "stock": 20,
        "is_recommended": False,
        "image_url": "/static/img/curry.jpg",
        "is_deleted": True,
        "updated_at": "2026-03-12",
        "created_at": "2026-02-28"
    }
]

# ホーム画面(dashboard.htmlへ遷移)
@admin.route("/")
def dashboard():
    return render_template("admin/dashboard.html")

# 注文管理画面(orders.htmlへ遷移)
@admin.route("/orders")
def order():
    return render_template("admin/orders.html",orders=orders)

# 注文管理画面内にて発送状況を切り替えるロジック
@admin.route("/toggle/<int:order_id>", methods=["POST"])
def toggle_status(order_id):
    for order in orders:
        if order["id"] == order_id:
            order["shipped"] = not order["shipped"]
            break
    return redirect(url_for("admin.order"))



# 商品管理画面(product.htmlへ遷移)
# 商品create
@admin.route("/create", methods=["GET", "POST"])
def product():
    form = ItemForm()

    if request.method == "POST":
        itemName = form.itemName.data
        categoryName = form.categoryName.data
        itemDetail = form.itemDetail.data
        price = form.price.data
        taxRate = form.taxRate.data
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
        return redirect("/admin/product")

    return render_template("admin/product.html", form=form)

# 商品read
@admin.route("/items/list")
def list_items():
    # 削除されていない商品だけ取得
    active_items = ItemM.query.filter_by(delFlg=False).order_by(ItemM.insDate.desc()).all()
    
    # 削除済みも含む全商品
    all_items = ItemM.query.order_by(ItemM.insDate.desc()).all()

    return render_template("admin/items.html",
                           active_items=active_items,
                           all_items=all_items)



@admin.route("/items/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = ItemM.query.get_or_404(item_id)


    if request.method == "POST":
        # フォームの値を更新
        item.itemName = request.form["itemName"]
        item.itemDetail = request.form["itemDetail"]
        item.categoryName = request.form["categoryName"]
        item.price = int(request.form["price"])
        item.stock = int(request.form["stock"])
        item.recmdFlg = "recmdFlg" in request.form
        item.updDate = datetime.now()  # 更新日時

        # 画像ファイルの処理
        file = request.files.get("imageFile")
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1]  # 拡張子
            filename = f"{uuid.uuid4().hex}{ext}"     # 例: 3f1a2b4c8d9e.png
            save_path = os.path.join(current_app.static_folder, 'img', filename)
            file.save(save_path)
            item.imageName = filename
        try:
            db.session.commit()
            flash("商品を更新しました。", "success")
            return redirect(url_for("admin.list_items"))
        except Exception as e:
            db.session.rollback()
            flash(f"更新に失敗しました: {e}", "danger")

    return render_template("admin/edit_item.html", item=item)


@admin.route("/items/delete/<item_id>", methods=["POST"])
def delete_item(item_id):
    # 削除処理を書く
    return redirect(url_for("admin.list_items"))