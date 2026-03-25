from datetime import datetime
from flask import Blueprint, redirect, render_template, session, url_for
from app.model.orderH import OrderH
from app.model.orderD import OrderD
from app.extensions import db
checkout = Blueprint("checkout", __name__)


@checkout.route("/")
def index():
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['amount'] for item in cart)

    shipping = 800 if subtotal > 0 else 0
    total = subtotal + shipping

    return render_template(
        "checkout/confirm.html",
        cart_items=cart,
        subtotal=subtotal,
        total=total,
        shipping=shipping
    )


@checkout.route("/add/<int:item_id>")
def add_to_cart(item_id):
    cart = session.get('cart', [])

    item = {
        "itemId": item_id,
        "itemName": "テスト商品",
        "price": 1000,
        "amount": 1,
        "imageName": "sample.jpg"
    }

    for c in cart:
        if c["itemId"] == item_id:
            c["amount"] += 1
            break
    else:
        cart.append(item)

    session['cart'] = cart
    session.modified = True   # ← これ重要

    return redirect(url_for('checkout.index'))


@checkout.route("/remove/<int:item_id>")
def remove_from_cart(item_id):
    cart = session.get('cart', [])

    cart = [item for item in cart if item["itemId"] != item_id]

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('checkout.index'))


@checkout.route("/increase/<int:item_id>", methods=['POST'])
def increase(item_id):
    cart = session.get('cart', [])

    for item in cart:
        if item["itemId"] == item_id:
            item["amount"] += 1
            break

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('checkout.index'))


@checkout.route("/decrease/<int:item_id>", methods=['POST'])
def decrease(item_id):
    cart = session.get('cart', [])

    for item in cart:
        if item["itemId"] == item_id:
            if item["amount"] > 1:
                item["amount"] -= 1
            else:
                # ← ここ追加（0になったら削除）
                cart = [i for i in cart if i["itemId"] != item_id]
            break

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('checkout.index'))


@checkout.route("/complete", methods=["POST"])
def complete():
    cart = session.get('cart', [])

    if not cart:
        return redirect(url_for('checkout.index'))

    # 注文ID（超簡易版）
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")

    subtotal = sum(item['price'] * item['amount'] for item in cart)
    shipping = 800 if subtotal > 0 else 0
    tax = int(subtotal * 0.1)
    total = subtotal + shipping + tax

    # ===== ヘッダ保存 =====
    order_h = OrderH(
        orderId=order_id,
        orderDate=datetime.now().strftime("%Y-%m-%d"),
        userName="テストユーザー",
        orderAddress="東京都",
        cardNum="****",
        shipFlg=False,
        price=subtotal,
        tax=tax,
        shipping=shipping,
        total=total
    )

    db.session.add(order_h)

    # ===== 明細保存 =====
    for i, item in enumerate(cart, start=1):
        order_d = OrderD(
            orderId=order_id,
            lineNo=i,
            itemId=item["itemId"],
            amount=item["amount"],
            price=item["price"],
            tax=int(item["price"] * item["amount"] * 0.1)
        )
        db.session.add(order_d)

    # DB確定
    db.session.commit()

    # カート削除
    session.pop('cart', None)

    return render_template("checkout/complete.html")