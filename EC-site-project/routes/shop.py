from flask import Blueprint, render_template, request

shop = Blueprint("shop", __name__)

# 商品データを共通で使えるように関数化しました
def get_products():
    return [
        {"id": 1, "name": "プレミアムコーヒー豆", "price": 1500, "category": "coffee", "image": "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?auto=format&fit=crop&w=600&q=80", "desc": "厳選されたアラビカ種100%を使用。深いコクと香りが特徴です。"},
        {"id": 2, "name": "オーガニックティーセット", "price": 2200, "category": "tea", "image": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80", "desc": "自然豊かな農園で育った茶葉のセット。心安らぐひとときを。"},
        {"id": 3, "name": "ハンドメイドマグカップ", "price": 1800, "category": "tableware", "image": "https://images.unsplash.com/photo-1517256011261-5144813f819f?auto=format&fit=crop&w=600&q=80", "desc": "職人が一つ一つ丁寧に焼き上げた一点物。手に馴染む質感が魅力です。"},
        {"id": 4, "name": "深煎りエスプレッソ", "price": 1600, "category": "coffee", "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=600&q=80", "desc": "濃厚でパンチのある味わい。ミルクとの相性も抜群です。"}
    ]

@shop.route('/')
def base():
    
    return render_template("base.html")


@shop.route('/test')
def index():
    products_list = get_products()
    
    # URLから「category」と「price」の条件を取得
    cat = request.args.get('category')
    price_range = request.args.get('price')

    filtered_products = products_list

    # カテゴリーで絞り込み
    if cat and cat != 'all':
        filtered_products = [p for p in filtered_products if p.get('category') == cat]

    # 価格帯で絞り込み
    if price_range:
        if price_range == '1000':
            filtered_products = [p for p in filtered_products if p['price'] <= 1000]
        elif price_range == '3000':
            filtered_products = [p for p in filtered_products if 1001 <= p['price'] <= 3000]
        elif price_range == '3001':
            filtered_products = [p for p in filtered_products if p['price'] >= 3001]

    return render_template("shop/index.html", products=filtered_products)

@shop.route('/product/<int:id>')
def detail(id):
    products_list = get_products()
    # IDが一致する商品を探す
    product = next((p for p in products_list if p['id'] == id), None)
    
    if product is None:
        return "商品が見つかりません", 404
        
    return render_template("shop/detail.html", product=product)
    
 