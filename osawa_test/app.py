from datetime import datetime
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kitai.db'
app.config["SECRET_KEY"] = "abc"

db.init_app(app)

# -----------------------------
# Login
# -----------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# -----------------------------
# User Model
# -----------------------------

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    mail = db.Column(db.String(50), nullable=False, unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    kintais = db.relationship("Kintai", backref="user", lazy=True)

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)


# -----------------------------
# Kintai Model
# -----------------------------

class Kintai(db.Model):

    __tablename__ = "kintai"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    clock_in_datetime = db.Column(db.DateTime)

    clock_out_datetime = db.Column(db.DateTime)

    rests = db.relationship("Rest", backref="kintai", lazy=True)


# -----------------------------
# Rest Model
# -----------------------------

class Rest(db.Model):

    __tablename__ = "rest"

    id = db.Column(db.Integer, primary_key=True)

    kintai_id = db.Column(
        db.Integer,
        db.ForeignKey("kintai.id"),
        nullable=False
    )

    break_start_time = db.Column(db.DateTime)

    break_end_time = db.Column(db.DateTime)

    @property
    def break_duration(self):

        if self.break_start_time and self.break_end_time:

            return self.break_end_time - self.break_start_time

        return None


# -----------------------------
# Login Page
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        mail = request.form.get("mail")
        password = request.form.get("password")

        user = User.query.filter_by(mail=mail).first()

        if user and user.check_password(password):

            login_user(user)

            if user.role == "admin":
                return redirect("/admin")

            return redirect("/user")

        return render_template("base.html", msg="ユーザ名またはパスワードが違います")

    return render_template("base.html")


# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


# -----------------------------
# Create User
# -----------------------------

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        new_user = User(
            name=name,
            mail=email,
            role=role
        )

        new_user.set_password(password)

        db.session.add(new_user)

        db.session.commit()

        return redirect("/admin")

    return render_template("create.html")


# -----------------------------
# Clock In
# -----------------------------

@app.route("/clock_in", methods=["POST"])
@login_required
def clock_in():

    kintai = Kintai(

        user_id=current_user.id,

        clock_in_datetime=datetime.now()

    )

    db.session.add(kintai)

    db.session.commit()

    return redirect("/user")


# -----------------------------
# Clock Out
# -----------------------------

@app.route("/clock_out", methods=["POST"])
@login_required
def clock_out():

    kintai = Kintai.query.filter_by(

        user_id=current_user.id,

        clock_out_datetime=None

    ).first()

    if kintai:

        kintai.clock_out_datetime = datetime.now()

    db.session.commit()

    return redirect("/user")


# -----------------------------
# Break Start
# -----------------------------

@app.route("/break_start", methods=["POST"])
@login_required
def break_start():

    kintai = Kintai.query.filter_by(
        user_id=current_user.id,
        clock_out_datetime=None
    ).order_by(Kintai.id.desc()).first()

    if not kintai:
        return redirect("/user")

    # 休憩中チェック
    active_rest = Rest.query.filter_by(
        kintai_id=kintai.id,
        break_end_time=None
    ).first()

    if active_rest:
        return redirect("/user")

    rest = Rest(
        kintai_id=kintai.id,
        break_start_time=datetime.now()
    )

    db.session.add(rest)
    db.session.commit()

    return redirect("/user")

# -----------------------------
# Break End
# -----------------------------

@app.route("/break_end", methods=["POST"])
@login_required
def break_end():

    kintai = Kintai.query.filter_by(
        user_id=current_user.id,
        clock_out_datetime=None
    ).order_by(Kintai.id.desc()).first()

    if not kintai:
        return redirect("/user")

    rest = Rest.query.filter_by(
        kintai_id=kintai.id,
        break_end_time=None
    ).order_by(Rest.id.desc()).first()

    if rest:
        rest.break_end_time = datetime.now()

        db.session.commit()

    return redirect("/user")


# -----------------------------
# Admin Page
# -----------------------------

@app.route("/admin")
@login_required
def admin():

    if current_user.role != "admin":
        return redirect("/user")
    users = User.query.all()

    return render_template("admin.html", users=users)


# -----------------------------
# User Page
# -----------------------------

@app.route("/user")
@login_required
def user():

    latest = Kintai.query.filter_by(
        user_id=current_user.id
    ).order_by(Kintai.id.desc()).first()

    return render_template(
        "user.html",
        users=current_user,
        latest=latest
    )

# -----------------------------
# Update User
# -----------------------------

@app.route("/<int:user_id>/update", methods=["GET", "POST"])
def update(user_id):

    user = User.query.get(user_id)

    if request.method == "POST":

        user.name = request.form.get("name")

        user.mail = request.form.get("email")

        password = request.form.get("password")

        if password:

            user.set_password(password)

        user.role = request.form.get("role")

        db.session.commit()

        return redirect("/admin")

    return render_template("update.html", user=user)


# -----------------------------
# Delete User
# -----------------------------

@app.route("/<int:user_id>/delete")
def delete(user_id):

    user = User.query.get(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect("/admin")


# -----------------------------
# DB Create
# -----------------------------

with app.app_context():

    db.create_all()


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True, port=12345)