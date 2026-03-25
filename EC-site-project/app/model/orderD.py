from app.extensions import db
from sqlalchemy import func

class OrderD(db.Model):
    __tablename__ = "orderD"
    orderId = db.Column(db.String(10),primary_key=True)     # 発注ID 複合キー
    lineNo = db.Column(db.Integer,primary_key=True)         # 行番号 複合キー
    itemId = db.Column(db.String(10))                      # 商品ID
    amount = db.Column(db.Integer, default=0)               # 数量
    price = db.Column(db.Float, default=0)                  # 単価（税抜き）
    tax = db.Column(db.Float, default=0)                    # 消費税
    delFlg = db.Column(db.Boolean, default=False, nullable=False)   # 削除フラグ
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 更新日付
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 登録日付

    # リレーションの設定(子供を指定)
    # 無

    # 辞書型で取得
    def getData(self):
        return{
            "userID": str(self.userID),
            "lineNo": int(self.lineNo),
            "itemId": str(self.ItemId),
            "amount": int(self.amount),
            "price": float(self.price),
            "tax": float(self.tax),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
