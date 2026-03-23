from . import db, func

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)

    create_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_dt = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    del_flag = db.Column(db.Integer)

    # リレーションの設定(子供を指定)
    employees = db.relationship("Employee", backref="department")

    # 辞書型で取得
    def getData(self):
        return{
            "id": int(self.id),
            "name": str(self.name)
        }
