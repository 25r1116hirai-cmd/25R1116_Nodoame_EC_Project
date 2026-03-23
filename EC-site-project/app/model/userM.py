from app.extensions import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

class userM(db.Model):
    __tablename__ = "userM"
    userID = db.Column(db.String(10),primary_key=True)
    passWord = db.Column(db.String(255)) # ハッシュ化後は長くなるため、文字数を多めに（128〜255）
    userName = db.Column(db.String(50))
    auth = db.Column(db.Integer)
    delFlg = db.Column(db.Boolean, default=False, nullable=False)
    updDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    insDate = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    # リレーションの設定(子供を指定)
    cartT = db.relationship("CartT", backref="userM", uselist=False)


    # 辞書型で取得
    def getData(self):
        return{
            "userID": str(self.userID),
            "password": str(self.password),
            "userName": str(self.userName),
            "auth": int(self.auth),
            "delFlg": bool(self.delFlg),
            "updDate": self.updDate.strftime('%Y/%m/%d %H:%M:%S') if self.updDate else None,
            "insDate": self.insDate.strftime('%Y/%m/%d %H:%M:%S') if self.insDate else None
        }

    # パスワードをハッシュ化してセットする
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 入力されたパスワードとハッシュ値を照合する
    def check_password(self, password):
        return check_password_hash(self.password, password)