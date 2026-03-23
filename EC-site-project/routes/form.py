from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired,NumberRange
from flask_wtf.file import FileAllowed

class ItemForm(FlaskForm):

    itemName = StringField("商品名", validators=[
        InputRequired("商品名は必須です")
    ], render_kw={"placeholder": "商品名"})

    categoryName = StringField("カテゴリー")

    itemDetail = StringField("商品説明", render_kw={"placeholder": "商品説明"})

    price = FloatField("価格", validators=[
        InputRequired("価格は必須です"),
        NumberRange(min=0, message="0以上で入力してください")
    ], default=0)

    taxRate = FloatField("税率", validators=[
        InputRequired("税率は必須です"),
        NumberRange(min=0, message="0以上で入力してください")
    ], default=0)

    stock = IntegerField("在庫", validators=[
        InputRequired("在庫は必須です"),
        NumberRange(min=0, message="0以上で入力してください")
    ], render_kw={"min": 0}, default=0)

    recmdFlg = BooleanField("おすすめ")

    # 画像用 FileField、拡張子を限定
    imageFile = FileField("画像", validators=[FileAllowed(['jpg','png','jpeg','gif'], "画像ファイルのみ許可")])
