from flask import Blueprint, render_template, request


shop = Blueprint("shop",__name__)

@shop.route('/')
def index():
    products_list = [
        {
            "id": 1, 
            "name": "プレミアムコーヒー豆", 
            "price": 1500, 
            "image": "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2, 
            "name": "オーガニックティーセット", 
            "price": 2200, 
            "image": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3, 
            "name": "ハンドメイドマグカップ", 
            "price": 1800, 
            "image": "https://images.unsplash.com/photo-1517256011261-5144813f819f?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4, 
            "name": "深煎りエスプレッソ", 
            "price": 1600, 
            "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=600&q=80"
        }
    ]
    return render_template("shop/index.html", products=products_list)



@shop.route('/product/<int:id>')
def detail(id):
    # 本来はDBから取得しますが、今はリストから該当IDを探します
    # products_listはindex関数内にあるものと同じ内容を定義するか、共通変数にします
    products_list = [
        {"id": 1, "name": "プレミアムコーヒー豆", "price": 1500, "image": "https://images.unsplash.com/photo-1611854779393-1b2da9d400fe?auto=format&fit=crop&w=600&q=80", "desc": "厳選されたアラビカ種100%を使用。深いコクと香りが特徴です。"},
        {"id": 2, "name": "オーガニックティーセット", "price": 2200, "image": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80", "desc": "自然豊かな農園で育った茶葉のセット。心安らぐひとときを。"},
        {"id": 3, "name": "ハンドメイドマグカップ", "price": 1800, "image": "https://images.unsplash.com/photo-1517256011261-5144813f819f?auto=format&fit=crop&w=600&q=80", "desc": "職人が一つ一つ丁寧に焼き上げた一点物。手に馴染む質感が魅力です。"},
        {"id": 4, "name": "深煎りエスプレッソ", "price": 1600, "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=600&q=80", "desc": "濃厚でパンチのある味わい。ミルクとの相性も抜群です。"}
    ]
    
    # IDが一致する商品を探す
    product = next((p for p in products_list if p['id'] == id), None)

    # URLから「category」と「price」の条件を取得
    # 例: /shop/?category=coffee
    cat = request.args.get('category')
    price_range = request.args.get('price')

    filtered_products = products_list

    # カテゴリーで絞り込み
    if cat and cat != 'all':
        filtered_products = [p for p in filtered_products if p['category'] == cat]

    # 価格帯で絞り込み
    if price_range:
        if price_range == '1000':
            filtered_products = [p for p in filtered_products if p['price'] <= 1000]
        elif price_range == '3000':
            filtered_products = [p for p in filtered_products if 1001 <= p['price'] <= 3000]
        elif price_range == '3001':
            filtered_products = [p for p in filtered_products if p['price'] >= 3001]

    return render_template("shop/index.html", products=filtered_products)
    
    if product is None:
        return "商品が見つかりません", 404
        
    return render_template("shop/detail.html", product=product)