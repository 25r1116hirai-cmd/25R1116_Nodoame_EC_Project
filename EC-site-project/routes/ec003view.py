import math

from flask import Flask, Blueprint, render_template, session, redirect, url_for
from app.model.schemas.cartItem import CartItem
from app.model.schemas.cartD import CartD   #3/24 add kurata


ec003view = Blueprint("ec003view",__name__)
ec003view.secret_key = 'your_secret_key' # セッション利用

@ec003view.route("/")
def index():
# 空の状態で画面を表示させるための初期値
    return render_template(
        "ec003view/index.html", 
        cart_obj=[], 
        subtotal=0, 
        shipping=0,
        total=0
    )

# 明細削除
@ec003view.route('/delete_item/<int:lineNo>')
def delete_item(lineNo):
    # セッションから現在のカートデータを取得
    cart_maisai = session.get('cartd', [])
    
    # 該当する行番号(lineNo)を除外した新しいリストを作成
    # lineNo は 1, 2, 3... と振られているので、一致しないものだけを残します
    updated_meisai = [d for d in cart_maisai if d.get('lineNo') != lineNo]
            
    # 更新したデータをセッションに保存し直す
    session['cartd'] = updated_meisai
    session.modified = True 
    
    # show_cartを呼び出すことで、合計金額が自動で再計算・再表示
    return redirect(url_for('ec003view.show_cart'))


# 数量変更（エラー解消のために追加）
#@ec003view.route('/update_amount/<int:lineNo>/<int:delta>')
@ec003view.route('/update_amount/<int:lineNo>/<int:delta>')
def update_amount(lineNo, delta):
    cart_meisai_list = session.get('cartd', [])
    for d in cart_meisai_list:
        print(f"lineno: {lineNo}, delta: {delta}, current_amount: {d.get('amount', 0)}")
        new_amount = 0
        if d.get('lineNo') == lineNo:
            if delta == 0:
                print("減算処理")
                new_amount = d.get('amount', 0) - 1
            elif delta == 1:
                print("増算処理")
                new_amount = d.get('amount', 0) + 1
            print(f"new_amount: {new_amount}")

            if new_amount > 0:
                d['amount'] = new_amount
            

    session['cartd'] = cart_meisai_list
    session.modified = True
    return redirect(url_for('ec003view.show_cart'))


@ec003view.route('/cart')
def show_cart():
    # 1. セッションから注文データを取得
    cart_dict = session.get('cart')
    cart_meisai = session.get('cartd',[])

    if not cart_dict:
        return redirect(url_for('ec003view.index'))
    
    # 2. 辞書から CartItem オブジェクトを復元
    cart_obj = CartItem.from_dict(cart_dict)
    # cart_meisai = [CartD.from_dict(d) for d in cart_meisai]
    
    # 3. 明細(details)の復元と行番号の振り直し
    details_objs = []
    # 削除等で欠番があっても、ここで1から連番を振り直す
    for i, d in enumerate(cart_meisai, start=1):
        try:
            item_detail = CartD(
                lineNo= i,
                itemId=d.get('itemId'),
                amount=d.get('amount', 0),
                price=d.get('price', 0),
                tax=d.get('tax', 0)
            )
            details_objs.append(item_detail)
        except Exception as e:
            print(f"明細の復元エラー: {e} - データ: {d}")
            continue
    # 4. 金額の計算（小数点以下切り捨て）
    # 小計（税抜合計）
    raw_subtotal = sum(d.price * d.amount for d in details_objs)
    subtotal = math.floor(raw_subtotal)  # 切り捨て
    
    # 消費税合計
    raw_total_tax = sum(d.tax * d.amount for d in details_objs)
    total_tax = math.floor(raw_total_tax)  # 切り捨て
    
    # 総合計（小計 + 消費税 + 送料）
    if (cart_obj, 'shipping') is  None:
            shipping = 0
    else:
        # ★ 小計が0の場合は送料を0にする
        if subtotal == 0:
            shipping = 0
        else:
            shipping = cart_obj.shipping

    total = math.floor(subtotal + total_tax + shipping) # 切り捨て

    # 各データを更新してセッションに保存
    # 明細を「辞書のリスト」に変換して保存
    session['cartd'] = [d.to_dict() for d in details_objs]

    # 振り直した行番号と計算結果を反映させてセッションを更新
    # これにより、以降の画面でも正しい連番と金額が保持されます
    cart_obj.details = [d.to_dict() for d in details_objs]
    cart_obj.price = subtotal
    cart_obj.tax = total_tax
    cart_obj.total = total
    
    # 各データを更新してセッションに保存
    # 明細を「辞書のリスト」に変換して保存
    session['cartd'] = [d.to_dict() for d in details_objs]
    session.modified = True  # セッションの変更を明示的に通知

    return render_template(
        'ec003view/index.html', 
        order=cart_obj,
        cart_items=details_objs,    #3/24 add kurata
        subtotal=subtotal,
        total_tax=total_tax,
        shipping=shipping,        # 3/24 add kurata
        total=total
    )

# サンプルデータ投入用（動作確認用）
@ec003view.route('/add_sample')
def add_sample():
    # サンプルデータの作成
    order_details = [
        CartD(lineNo=99, itemId="I001", amount=2, price=1500.8, tax=150.2),
        CartD(lineNo=100, itemId="I005", amount=1, price=800.5, tax=80.1)
    ]
    
    # CartItemの初期化（詳細はあとでセット）
    sample = CartItem(
        orderDate="2026-03-24",
        userName="倉田 珠誉",
        orderAddress="大阪府...",
        cardNum="****-1234",
        price=0,
        tax=0,
        shipping=500,
        total=0
    )
    
    # 明細を辞書化してセット
    # sample.details = [d.to_dict() for d in order_details]
    session['cart'] = sample.to_dict()
    print(session['cart'])
    session['cartd'] = [d.to_dict() for d in order_details]
    print(session['cartd'])
    # show_cartを呼び出して計算と表示を行う
    return redirect(url_for('ec003view.show_cart'))
    