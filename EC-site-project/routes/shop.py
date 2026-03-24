from flask import Blueprint, render_template, request
#DBのテーブルとDB操作のファイルをインポート
from app.model.itemM import ItemM
from app.extensions import db

shop = Blueprint("shop", __name__)



@shop.route('/top')
def index():
    # すべて
    items = ItemM.query.all()
    # おすすめがTrue、更新日で降順、上限3件分をすべて
    recommend_items = ItemM.query.filter_by(recmdFlg=True).order_by(ItemM.updDate.desc()).limit(3).all()




    # # 価格帯で絞り込み
    # if price_range:
    #     if price_range == '1000':
    #         filtered_products = [p for p in filtered_products if p['price'] <= 1000]
    #     elif price_range == '3000':
    #         filtered_products = [p for p in filtered_products if 1001 <= p['price'] <= 3000]
    #     elif price_range == '3001':
    #         filtered_products = [p for p in filtered_products if p['price'] >= 3001]

    return render_template("shop/index.html",items=items,reco=recommend_items)

@shop.route('/product/<int:id>')
def detail(id):
    item = ItemM.query.get(id)

    if not item:
        abort(404)

    return render_template("shop/detail.html", item=item)
    
 