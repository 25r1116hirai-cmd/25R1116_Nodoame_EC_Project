from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.model.itemM import ItemM
from app.model.orderH import OrderH
from app.model.orderD import OrderD

checkout = Blueprint("checkout", __name__)


# カート確認ページ
@checkout.route("/")
def index():
    cart = session.get("cart", [])
# 単価(price)を税込として扱う、またはここで計算する
    # 今回は「単価×数量」の合計を「税抜小計」として、別途税を加算する方式で調整します
    subtotal_ex_tax = sum(item["price"] * item["amount"] for item in cart)
    tax = int(subtotal_ex_tax * 0.1)
    subtotal_inc_tax = subtotal_ex_tax + tax # これが画面上の「税込小計」
    
    shipping = 800 if subtotal_inc_tax > 0 else 0
    total = subtotal_inc_tax + shipping
    return render_template(
        "checkout/confirm.html",
        cart_items=cart,
        subtotal=subtotal_inc_tax,
        total=total,
        shipping=shipping
    )


# カートに追加
@checkout.route("/add/<int:item_id>")
@login_required  # 未ログインなら login_view にリダイレクト
def add_to_cart(item_id):
    # DBから商品取得
    item = ItemM.query.get(item_id)
    if not item or item.delFlg:
        flash("商品が存在しません")
        return redirect(url_for("shop.index"))

    cart = session.get("cart", [])

    # すでにカートにある場合は数量増加
    for c in cart:
        if c["itemId"] == item_id:
            c["amount"] += 1
            break
    else:
        # 新規追加
        cart.append({
            "itemId": item.itemId,
            "itemName": item.itemName,
            "price": item.price,
            "amount": 1,
            "imageName": item.imageName
        })

    session["cart"] = cart
    session.modified = True
    flash(f"{item.itemName} をカートに追加しました")
    return redirect(url_for("checkout.index"))


# カートから削除
@checkout.route("/remove/<int:item_id>")
def remove_from_cart(item_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["itemId"] != item_id]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout.index"))


# 数量増加
@checkout.route("/increase/<int:item_id>", methods=["POST"])
def increase(item_id):
    cart = session.get("cart", [])
    for item in cart:
        if item["itemId"] == item_id:
            item["amount"] += 1
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout.index"))


# 数量減少
@checkout.route("/decrease/<int:item_id>", methods=["POST"])
def decrease(item_id):
    cart = session.get("cart", [])
    for item in cart:
        if item["itemId"] == item_id:
            if item["amount"] > 1:
                item["amount"] -= 1
            else:
                cart = [i for i in cart if i["itemId"] != item_id]
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout.index"))


# 注文確定
@checkout.route("/complete", methods=["POST"])
@login_required
def complete():
    cart = session.get("cart", [])
    if not cart:
        flash("カートが空です")
        return redirect(url_for("checkout.index"))

    userName = request.form.get("userName")
    orderAddress = request.form.get("orderAddress")
    phone = request.form.get("phone")

    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    subtotal = sum(item['price'] * item['amount'] for item in cart)
    shipping = 800 if subtotal > 0 else 0
    tax = int(subtotal * 0.1)
    total = subtotal + shipping + tax

    # ヘッダ保存
    order_h = OrderH(
        orderId=order_id,
        orderDate=datetime.now().strftime("%Y-%m-%d"),
        userName=userName,
        orderAddress=orderAddress,
        phone=phone,
        shipFlg=False,
        price=subtotal,
        tax=tax,
        shipping=shipping,
        total=total
    )
    db.session.add(order_h)

    # 明細保存
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

    db.session.commit()
    session.pop("cart", None)
    flash("注文が完了しました！")
    return render_template("checkout/complete.html", order_id=order_id, total=total)


@checkout.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    cart = session.get("cart", [])
    if not cart:
        flash("カートに商品がありません")
        return redirect(url_for("checkout.index"))

    if request.method == "POST":
        # フォームからPOSTされたらcompleteにリダイレクト
        return redirect(url_for("checkout.complete"))

    return render_template("checkout/payment.html", cart_items=cart)