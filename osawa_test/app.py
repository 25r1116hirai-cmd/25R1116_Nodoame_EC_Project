from datetime import datetime
import os
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify



db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kintai.db'

# セッションキー
app.config["SECRET_KEY"] = "abc"

# ログイン管理システム
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
db.init_app(app)

# ユーザを識別するための関数
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin,db.Model):
   id = db.Column(db.Integer , primary_key=True )
   name = db.Column(db.String(50),nullable=False)
   mail = db.Column(db.String(50),nullable=False,unique=True)
   password_hash = db.Column(db.String(255), nullable=False)
   role = db.Column(db.String(20), default="user") 
   attendances = db.relationship("Attendance", backref="user", lazy=True)
    # パスワード設定
   def set_password(self, password):
        self.password_hash = generate_password_hash(password,method="pbkdf2:sha256")

    # パスワード確認
   def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 外部キー
    clock_in_datetime = db.Column(db.DateTime, nullable=False)
    clock_out_datetime = db.Column(db.DateTime, nullable=True)
    
    # 1日あたりの休憩情報とのリレーション
    breaks = db.relationship("BreakTime", backref="attendance", lazy=True)

class BreakTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer, db.ForeignKey("attendance.id"), nullable=False)
    break_start_time = db.Column(db.Time, nullable=True)
    break_end_time = db.Column(db.Time, nullable=True)
    
    @property
    def break_duration(self):
        if self.break_start_time and self.break_end_time:
            start = datetime.combine(datetime.today(), self.break_start_time)
            end = datetime.combine(datetime.today(), self.break_end_time)
            return end - start
        return None

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":
        mail = request.form.get("mail")
        password = request.form.get("password")

        user = User.query.filter_by(mail=mail).first()
        if user and user.check_password(password):
            login_user(user)

            if user.role == "admin":
                return redirect("/admin")
            else:
                return redirect("/user")

        return "ログイン失敗"

    return render_template("login.html")


@app.route("/admin", methods = ["GET","POST"])
@login_required
def admin():
    if current_user.role != "admin":
        return "権限がありません"
    # admin = User.query.filter_by(is_deleted=False).all()
    admin = User.query.all()
    attendances = db.relationship("Attendance", backref="user", lazy=True)
    return render_template("admin.html",admin=admin,attendances=attendances)

@app.route("/create", methods = ["GET","POST"])
@login_required
def signup():
    if current_user.role != "admin":
        return "権限がありません"

    if request.method == 'POST':
        name = request.form.get('name')
        mail = request.form.get('mail')
        password = request.form.get('password')

        if User.query.filter_by(mail=mail).first():
            return "このメールは既に登録されています"
        
        user = User(name=name,mail=mail)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    
    elif request.method == 'GET':
        return render_template("signup.html")



@app.route("/<int:post_id>/update", methods=['GET','POST'])
def update(post_id):
   
    user = User.query.get(post_id)

    if request.method == "POST":
        user.name = request.form.get('userName')
       # user.is_deleted = request.form.get('departmentflag') =="True"
        db.session.commit()

        return redirect('/admin')
    elif request.method == "GET":
        return render_template("update.html", user=user)


with app.app_context():
    db.create_all()

   # 管理者アカウント
    admin = User.query.filter_by(mail="admin@test.com").first()
    if not admin:
        admin = User(
            name="admin",
            mail="admin@test.com",
            role="admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    # テストユーザ
    test_user = User.query.filter_by(mail="testuser@test.com").first()
    if not test_user:
        test_user = User(
            name="テストユーザ",
            mail="testuser@test.com",
            role="user"
        )
        test_user.set_password("test123")
        db.session.add(test_user)
        db.session.commit()

        # 勤怠データ
        attendance = Attendance(
            user_id=test_user.id,
            clock_in_datetime=datetime(2026, 3, 12, 9, 0),
            clock_out_datetime=datetime(2026, 3, 12, 18, 0)
        )
        db.session.add(attendance)
        db.session.commit()

        # 休憩データ
        br = BreakTime(
            attendance_id=attendance.id,
            break_start_time=datetime.strptime("12:00", "%H:%M").time(),
            break_end_time=datetime.strptime("12:45", "%H:%M").time()
        )
        db.session.add(br)
        db.session.commit()



@app.route("/api/users")
def api_users():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "mail": user.mail,
            "role": user.role
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)



