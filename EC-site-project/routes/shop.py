from flask import Blueprint, abort, render_template, request,session
#DBのテーブルとDB操作のファイルをインポート
from app.model.itemM import ItemM
from app.extensions import db

shop = Blueprint("shop", __name__)



@shop.route('/top')
def index():

    # 共通：論理削除は除く
    # すべて 
    all_items = ItemM.query.filter_by(delFlg=False).all()
    
    # おすすめ、更新日で降順、上限3件分をすべて
    recommend_items = ItemM.query.filter_by(recmdFlg=True,delFlg=False).order_by(ItemM.updDate.desc()).limit(3).all()
    print(all_items)
  

    return render_template("shop/index.html",
                           all_items=all_items,
                           reco=recommend_items,
                          )

@shop.route('/product/<int:id>')
def detail(id):
    item = ItemM.query.get(id)

    if not item:
        abort(404)

    return render_template("shop/detail.html", product=item)
    
 