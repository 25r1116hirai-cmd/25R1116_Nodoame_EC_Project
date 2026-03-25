from app.extensions import db
from sqlalchemy import func

class OrderH(db.Model):
    __tablename__ = "orderH"
    orderId = db.Column(db.String(10),primary_key=True)     # 発注ID 
    orderDate = db.Column(db.String(10))                    # 注文日付
    userName = db.Column(db.String(50))                     # お客様名
    orderAddress = db.Column(db.String(50))                 # お届け先住所
    cardNum = db.Column(db.String(50))                      # クレジットカード番号
    shipFlg = db.Column(db.Boolean, default=False)          # 発送フラグ
    price = db.Column(db.Float, default=0)                  # 小計（税別）
    tax = db.Column(db.Float, default=0)                    # 消費税
    shipping  = db.Column(db.Float, default=0)              # 送料
    total = db.Column(db.Float, default=0)                  # 合計
    delFlg = db.Column(db.Boolean, default=False, nullable=False)   # 削除フラグ
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 更新日付
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 登録日付

    # リレーションの設定(子供を指定)
    # 無

    # 辞書型で取得
    def getData(self):
        return{
            "orderId": str(self.orderId),
            "orderDate": str(self.orderDate),
            "userName": str(self.userName),
            "orderAddress": str(self.orderAddress),
            "cardNum": str(self.cardNum),
            "shipFlg": bool(self.shipFlg),
            "price": float(self.price),
            "tax": float(self.tax),
            "shipping": float(self.shipping),
            "total": float(self.total),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
