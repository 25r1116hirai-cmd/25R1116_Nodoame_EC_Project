from flask import Blueprint, abort, render_template, request
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
    # カテゴリから重複を除去
    categories = sorted({item.categoryName for item in all_items})

    # カテゴリで絞り込み
    selected_category = request.args.get("category")
    if selected_category and selected_category != "all":
        filtered_items = [item for item in all_items if item.categoryName == selected_category]
    else:
        filtered_items = all_items

    # 価格帯で絞り込み（もし price パラメータがある場合）
    price_filters = {
    '1000': lambda p: p <= 1000,
    '3000': lambda p: 1001 <= p <= 3000,
    '3001': lambda p: p >= 3001,
}
    price_range = request.args.get("price") 
    if price_range in price_filters:
        filtered_items = [item for item in filtered_items if price_filters[price_range](item.price)]

    return render_template("shop/index.html",
                           items=filtered_items,
                           all_items=all_items,
                           reco=recommend_items,
                           categories=categories,
                           selected_category=selected_category
                          )

@shop.route('/product/<int:id>')
def detail(id):
    item = ItemM.query.get(id)

    if not item:
        abort(404)

    return render_template("shop/detail.html", product=item)
    
 