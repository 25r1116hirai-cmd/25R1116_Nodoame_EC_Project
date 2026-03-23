from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, StringField, SubmitField, TelField, SelectField
from wtforms.validators import DataRequired, Email, Length  

from . import app,db,Employee,Person,Department
from flask import render_template, redirect, request, url_for

@app.route("/")
def index():
    # 全件取得
    data = Employee.query.filter_by(del_flag=None)
    return render_template("index.html",data=data)

# 部署一覧
@app.route("/departments")
def departments():
    data = Department.query.filter_by(del_flag=None)
    return render_template("departments.html", data=data)

# フォームクラス(Employee)
class EmployeePersonForm(FlaskForm):
    name = StringField('お名前', validators=[
        DataRequired(message="名前を入力して下さい。"),
        Length(max=30,message="30文字以内で入力して下さい。")
    ])
    age = IntegerField('年齢',validators=[])
    gender = IntegerField('性別',validators=[])
    tel = TelField('TEL',validators=[])
    email = EmailField('メールアドレス', validators=[
        DataRequired(message="メールアドレスを入力して下さい。"),
        Email(message="正しいメール形式で入力して下さい。"),
        DataRequired(message="名前を入力して下さい。")
    ])
    salary = IntegerField('給与',validators=[])
    dept = SelectField('部署', coerce=int, validators=[])
    submit = SubmitField('登録')

class EmployeeAdd(MethodView):
    def get(self):
        form = EmployeePersonForm()
        # 部署の選択肢をセット
        form.dept.choices = [(0, "部署なし")] + [(d.id, d.name) for d in Department.query.all()]
        return render_template("employee.html",form=form)
    def post(self):
        form = EmployeePersonForm()
        form.dept.choices = [(0, "部署なし")] + [(d.id, d.name) for d in Department.query.all()]
        if form.validate_on_submit():
            # DBへ保存
            name = form.name.data
            age = form.age.data
            gender = form.gender.data
            tel = form.tel.data
            email = form.email.data
            salary = form.salary.data
            dept = None if form.dept.data == 0 else form.dept.data
            newPerson = Person(name=name,age=age,gender=gender,tel=tel,email=email)
            db.session.add(newPerson)
            db.session.flush()
            newEmp = Employee(id=newPerson.id,salary=salary,dept=dept)
            db.session.add(newEmp)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template("employee.html", form=form)

app.add_url_rule("/employee",view_func=EmployeeAdd.as_view("employee"))

# 従業員詳細
@app.route("/employee/<int:id>")
def employee_detail(id):
    emp = Employee.query.get_or_404(id)
    return render_template("employee_detail.html", emp=emp)

# 従業員情報・個人情報の更新
class EmployeeEdit(MethodView):
    def get(self, id):
        emp = Employee.query.get_or_404(id)
        person = emp.person
        form = EmployeePersonForm(obj=person)
        form.dept.choices = [(0, "部署なし")] + [(d.id, d.name) for d in Department.query.all()]
        form.salary.data = emp.salary
        form.dept.data = emp.dept if emp.dept else 0
        return render_template("employee.html", form=form)

    def post(self, id):
        emp = Employee.query.get_or_404(id)
        person = emp.person
        form = EmployeePersonForm()
        form.dept.choices = [(0, "部署なし")] + [(d.id, d.name) for d in Department.query.all()]
        if form.validate_on_submit():
            person.name = form.name.data
            person.age = form.age.data
            person.gender = form.gender.data
            person.tel = form.tel.data
            person.email = form.email.data
            emp.salary = form.salary.data
            emp.dept = None if form.dept.data == 0 else form.dept.data
            db.session.commit()
            return redirect(url_for('employee_detail', id=emp.id))
        return render_template("employee.html", form=form)

app.add_url_rule("/employee/edit/<int:id>", view_func=EmployeeEdit.as_view("employee_edit"))

# 従業員情報の削除
@app.route("/employee/delete/<int:id>", methods=['POST'])
def employee_delete(id):
    emp = Employee.query.get_or_404(id)
    person = emp.person
    emp.del_flag = 1
    # db.session.delete(emp)
    if person:
        person.del_flag = 1
    db.session.commit()
    return redirect(url_for('index'))

# --- Department (部署) CRUD ---
class DepartmentForm(FlaskForm):
    name = StringField('部署名', validators=[
        DataRequired(message="部署名を入力して下さい。"),
        Length(max=50, message="50文字以内で入力して下さい。")
    ])
    submit = SubmitField('登録')

# 部署の追加
class DepartmentAdd(MethodView):
    def get(self):
        form = DepartmentForm()
        return render_template("department_form.html", form=form)

    def post(self):
        form = DepartmentForm()
        if form.validate_on_submit():
            new_dept = Department(name=form.name.data)
            db.session.add(new_dept)
            db.session.commit()
            return redirect(url_for('departments'))
        return render_template("department_form.html", form=form)

app.add_url_rule("/department/add", view_func=DepartmentAdd.as_view("department_add"))

# 部署の編集
class DepartmentEdit(MethodView):
    def get(self, id):
        dept = Department.query.get_or_404(id)
        form = DepartmentForm(obj=dept)
        return render_template("department_form.html", form=form)

    def post(self, id):
        dept = Department.query.get_or_404(id)
        form = DepartmentForm()
        if form.validate_on_submit():
            dept.name = form.name.data
            db.session.commit()
            return redirect(url_for('departments'))
        return render_template("department_form.html", form=form)

app.add_url_rule("/department/edit/<int:id>", view_func=DepartmentEdit.as_view("department_edit"))

# 部署の削除
@app.route("/department/delete/<int:id>", methods=['POST'])
def department_delete(id):
    dept = Department.query.get_or_404(id)
    # 関連する従業員が存在する場合は削除しない等の制御を追加することもできますが、今回は単純に削除します
    dept.del_flag = 1
    db.session.commit()
    return redirect(url_for('departments'))
