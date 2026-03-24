from flask import Flask, Blueprint, render_template, session, redirect, url_for
from app.model.schemas.cartItem import CartItem

ec003view = Blueprint("ec003view",__name__)
ec003view.secret_key = 'your_secret_key' # セッション利用

@ec003view.route("/")
def index():
# 空の状態で画面を表示させるための初期値
    return render_template(
        "ec003view/index.html", 
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
    sample = CartItem("I001", "プレミアムコーヒー豆", 1500, "coffee.jpg", 1)
    cart = session.get('cart', [])
    cart.append(sample.to_dict())
    session['cart'] = cart
    return redirect(url_for('show_cart'))