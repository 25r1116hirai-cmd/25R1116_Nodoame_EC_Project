import csv
import io
import math
from flask import Blueprint, render_template, session, redirect, url_for, Response, request, flash
from app.extensions import db
from app.model.userM import UserM  # フォルダ名が 'model' か 'models' か確認してください

# Blueprintの名前を "test" に統一します
test = Blueprint("test", __name__)

# --- メイン画面の表示 ---
@test.route("/")
def index():
    # ここでちゃんと return することが重要です！
    return render_template('test/index.html')

# --- DB データを CSV に書き出す (DB書込) ---
@test.route('/export/users')
def export_users():
    users = UserM.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # ヘッダー
    header = ["userID", "userName", "role", "delFlg"]
    writer.writerow(header)
    
    # データ
    for user in users:
        writer.writerow([user.userID, user.userName, user.role, user.delFlg])
    
    response = Response(output.getvalue().encode('utf-8-sig'))
    response.headers["Content-Disposition"] = "attachment; filename=users_export.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

# --- CSV を読み込んで DB に登録する (DB取込) ---
@test.route('/import/users', methods=['POST'])
def import_users():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash("CSVファイルを選択してください")
        return redirect(url_for('test.index'))

    stream = io.StringIO(file.stream.read().decode("utf-8-sig"))
    csv_input = csv.DictReader(stream)

    try:
        for row in csv_input:
            user = UserM.query.filter_by(userID=row['userID']).first()
            if not user:
                user = UserM()
                db.session.add(user)
            
            user.userID = row['userID']
            user.userName = row['userName']
            user.role = int(row['role'])
            user.delFlg = row['delFlg'].lower() == 'true'
            
        db.session.commit()
        flash("インポートが完了しました")
    except Exception as e:
        db.session.rollback()
        flash(f"エラーが発生しました: {e}")

    # 処理が終わったらメイン画面に戻る
    return redirect(url_for('test.index'))