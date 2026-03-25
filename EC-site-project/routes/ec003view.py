from flask import Flask, Blueprint, render_template, session, redirect, url_for
from app.model.schemas.cartItem import CartItem

ec003view = Blueprint("ec003view",__name__)
ec003view.secret_key = 'your_secret_key' # セッション利用

@ec003view.route("/")
def index():
# 空の状態で画面を表示させるための初期値
    return render_template(
        "shop/cart.html", 
        cart_items=[], 
        subtotal=0, 
        total=0
    )

@ec003view.route('/cart')
def show_cart():
    # セッションからカート情報を取得（なければ空リスト）
    cart_data = session.get('cart', [])
    
    # 辞書データからオブジェクトのリストに復元
    cart_items = [CartItem.from_dict(item) for item in cart_data]
    
    # 合計金額の計算
    subtotal = sum(item.price * item.amount for item in cart_items)
    tax = 0  # サンプル画面に合わせて無料設定、必要なら計算式を追加
    total = subtotal + tax

    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, total=total)

# サンプルデータ投入用（動作確認用）
@ec003view.route('/add_sample')
def add_sample():
    # 明細行をリストとして作成
    order_details = [
        {"lineNo": 1, "itemId": "I001", "itemName": "プレミアムコーヒー豆", "amount": 2, "price": 1500, "tax": 150},
        {"lineNo": 2, "itemId": "I005", "itemName": "ドリッパー", "amount": 1, "price": 800, "tax": 80}
    ]
    
    sample = CartItem(
        orderId="ORD001",
        orderDate="2026-03-24",
        userName="倉田 珠誉",
        orderAddress="大阪府...",
        cardNum="****-1234",
        shipFlg=False,
        price=3800,
        tax=380,
        shipping=0,
        total=4180,
        details=order_details  # ここでリストを渡す
    )
    return redirect(url_for('show_cart'))
    