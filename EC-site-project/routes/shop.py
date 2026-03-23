from flask import Blueprint, render_template


shop = Blueprint("shop",__name__)

@shop.route("/")
def index():
    # データを関数の中で定義（確実にHTMLへ送るため）
    products_list = [
        {
            "id": 1, 
            "name": "プレミアムコーヒー豆", 
            "price": 1500, 
            "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?auto=format&fit=crop&w=400&q=80"
        },
        {
            "id": 2, 
            "name": "オーガニックティーセット", 
            "price": 2200, 
            "image": "https://images.unsplash.com/photo-1594631252845-29fc45865157?auto=format&fit=crop&w=400&q=80"
        }
    ]
    # ここが重要！ HTML側の「products」という変数名に「products_list」を割り当てる
    return render_template("shop/index.html", products=products_list)
    


