# add_test_orders.py
from run import app
from app.extensions import db
from app.model.orderH import OrderH
from datetime import datetime

with app.app_context():
    # 例: 3件のテスト注文を作成
    test_orders = [
        {
            "orderId": "202603260001",
            "orderDate": datetime.now().strftime("%Y-%m-%d"),
            "userName": "テストユーザーA",
            "orderAddress": "東京都渋谷区",
            "cardNum": "****",
            "shipFlg": False,
            "price": 2000,
            "tax": 200,
            "shipping": 500,
            "total": 2700
        },
        {
            "orderId": "202603260002",
            "orderDate": datetime.now().strftime("%Y-%m-%d"),
            "userName": "テストユーザーB",
            "orderAddress": "大阪府大阪市",
            "cardNum": "****",
            "shipFlg": False,
            "price": 3500,
            "tax": 350,
            "shipping": 800,
            "total": 4650
        },
        {
            "orderId": "202603260003",
            "orderDate": datetime.now().strftime("%Y-%m-%d"),
            "userName": "テストユーザーC",
            "orderAddress": "北海道札幌市",
            "cardNum": "****",
            "shipFlg": False,
            "price": 5000,
            "tax": 500,
            "shipping": 800,
            "total": 6300
        }
    ]

    for o in test_orders:
        if not OrderH.query.get(o["orderId"]):  # 既存チェック
            order = OrderH(**o)
            db.session.add(order)

    db.session.commit()
    print("テスト注文3件追加完了")