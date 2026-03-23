from app.extensions import db
from sqlalchemy import func

class CartT(db.Model):
    __tablename__ = "orderH"
    orderId = db.Column(db.String(10),primary_key=True) # ユーザーID + 行番号　の複合キー
    orderDate = db.Column(db.String(10),primary_key=True) # ユーザーID + 行番号　の複合キー
    userName = db.Column(db.String(50))
    orderAddress = db.Column(db.String(50))
    cardNum = db.Column(db.String(50))
    shipFlg = db.Column(db.Boolean)
    price = db.Column(db.Float)
    tax = db.Column(db.Float)
    total = db.Column(db.Float)
    delFlg = db.Column(db.Boolean, default=False, nullable=False)
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    # リレーションの設定(子供を指定)
    # 無

    # 辞書型で取得
    def getData(self):
        return{
            "orderId": str(self.userID),
            "orderDate": str(self.lineNo),
            "userName": str(self.ItemId),
            "orderAddress": str(self.amount),
            "cardNum": str(self.price),
            "shipFlg": bool(self.tax),
            "price": float(self.tax),
            "tax": float(self.tax),
            "total": float(self.tax),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
