from app.extensions import db
from sqlalchemy import func

class ItemM(db.Model):
    __tablename__ = "itemM"
    itemId = db.Column(db.String(10),primary_key=True)
    categoryName = db.Column(db.String(30)) 
    itemName = db.Column(db.String(100))
    itemDetail = db.Column(db.String(100))
    taxRate = db.Column(db.Float)
    stock = db.Column(db.Integer)
    recmdFlg = db.Column(db.Boolean)
    imageName = db.Column(db.String(100))
    delFlg = db.Column(db.Boolean, default=False, nullable=False)
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    # リレーションの設定(子供を指定)
    orderD = db.relationship("OrderD", backref="itemM", uselist=False)


    # 辞書型で取得
    def getData(self):
        return{
            "itemId": str(self.itemId),
            "categoryName": str(self.categoryName),
            "itemName": str(self.itemName),
            "itemDetail": int(self.itemDetail),
            "taxRate": float(self.taxRate),
            "stock": int(self.stock),
            "recmdFlg": bool(self.recmdFlg),
            "imageName": str(self.imageName),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
