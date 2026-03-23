from . import db, func

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    tel = db.Column(db.String(20))
    email = db.Column(db.String(30))

    create_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_dt = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    del_flag = db.Column(db.Integer)

    # リレーションの設定(子供を指定)
    employee = db.relationship("Employee", backref="person", uselist=False)

    # 辞書型で取得
    def getData(self):
        return{
            "id": int(self.id),
            "name": str(self.name),
            "age": int(self.age),
            "gender": int(self.gender),
            "tel": str(self.tel),
            "email": str(self.email)
        }