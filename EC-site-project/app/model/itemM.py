from app.extensions import db
from sqlalchemy import func

class ItemM(db.Model):
    __tablename__ = "itemM"
    itemId = db.Column(db.Integer, primary_key=True)    # 商品ID
    categoryName = db.Column(db.String(30))             # カテゴリ名
    itemName = db.Column(db.String(100))                # 商品名
    itemDetail = db.Column(db.String(100))              # 商品詳細
    price = db.Column(db.Integer, default=0)            # 単価
    taxRate = db.Column(db.Float, default=0)            # 消費税率
    stock = db.Column(db.Integer, default=0)            # 在庫数
    recmdFlg = db.Column(db.Boolean)                    # おすすめフラグ
    imageName = db.Column(db.String(100))               # イメージ図名称
    delFlg = db.Column(db.Boolean, default=False, nullable=False)       # 削除フラグ
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 更新日付
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())  # 登録日付

    # 辞書型で取得
    def getData(self):
        return {
            "itemId": int(self.itemId),
            "categoryName": str(self.categoryName),
            "itemName": str(self.itemName),
            "itemDetail": str(self.itemDetail),
            "price": int(self.price),             
            "taxRate": float(self.taxRate),
            "stock": int(self.stock),
            "recmdFlg": bool(self.recmdFlg),
            "imageName": str(self.imageName),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }
