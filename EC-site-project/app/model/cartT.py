from . import db, func
from flask_sqlalchemy import SQLAlchemy
# セッションを使用してカートを管理する為、カートテーブルは不要

class cartT(db.Model):
    __tablename__ = "cartT"
    userID = db.Column(db.String(10),primary_key=True) # ユーザーID + 行番号　の複合キー
    lineNo = db.Column(db.String(30),primary_key=True) # ユーザーID + 行番号　の複合キー
    ItemId = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    price = db.Column(db.float)
    tax = db.Column(db.Integer)
    delFlg = db.Column(db.Boolean, default=False, nullable=False)
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    # リレーションの設定(子供を指定)
    # 無

    # 辞書型で取得
    def getData(self):
        return{
            "userID": str(self.userID),
            "lineNo": int(self.lineNo),
            "ItemId": str(self.ItemId),
            "amount": int(self.amount),
            "price": float(self.price),
            "tax": float(self.tax),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
