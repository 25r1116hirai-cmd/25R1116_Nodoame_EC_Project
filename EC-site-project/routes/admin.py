from flask import Blueprint, redirect, render_template, url_for


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
@admin.route("/product")
def product():
    return render_template("admin/product.html",products=products)
