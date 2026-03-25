from flask import Blueprint, redirect, render_template, session, url_for

checkout = Blueprint("checkout", __name__)

@checkout.route("/")
def index():
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['amount'] for item in cart)
    total = subtotal

    return render_template(
        "checkout/confirm.html",
        cart_items=cart,
        subtotal=subtotal,
        total=total
    )


@checkout.route("/add/<int:item_id>")
def add_to_cart(item_id):
    cart = session.get('cart', [])

    # 仮データ
    item = {
        "itemId": item_id,
        "itemName": "テスト商品",
        "price": 1000,
        "amount": 1,
        "imageName": "sample.jpg"
    }

    # すでにカートにあるかチェック
    for c in cart:
        if c["itemId"] == item_id:
            c["amount"] += 1
            break
    else:
        cart.append(item)

    session['cart'] = cart

    return redirect(url_for('checkout.index'))
