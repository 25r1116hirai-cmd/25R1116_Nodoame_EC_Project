from . import db, func

class Employee(db.Model):
    __tablename__ = "employee"
    # リレーションの設定(親を指定)
    id = db.Column(db.Integer,db.ForeignKey("person.id"),primary_key=True)
    salary = db.Column(db.Integer)
    dept = db.Column(db.Integer,db.ForeignKey("department.id"))

    create_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    update_dt = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    del_flag = db.Column(db.Integer)

    # 辞書型で取得
    def getData(self):
        return{
            "id": int(self.id),
            "salary": int(self.salary),
            "name": str(self.person.name),
            "person": str(self.person)
        }
