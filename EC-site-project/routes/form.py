from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired,NumberRange
from flask_wtf.file import FileAllowed
from wtforms import SelectField

class ItemForm(FlaskForm):

    itemName = StringField("商品名", validators=[
        InputRequired("商品名は必須です")
    ], render_kw={"placeholder": "商品名"})

    categoryName = StringField("カテゴリー")

    itemDetail = StringField("商品説明", render_kw={"placeholder": "商品説明"})

    price = FloatField("価格", validators=[
        NumberRange(min=0, message="0以上で入力してください")
    ], default=0)

    #127Pを参照
    taxRate = SelectField(
    "税率",
    choices=[
        ("0.10", "10%"),
        ("0.08", "8%")
    ],
    validators=[InputRequired("税率は必須です")],
    default="0.10"
)

    stock = IntegerField("在庫", validators=[
        NumberRange(min=0, message="0以上で入力してください")
    ], render_kw={"min": 0}, default=0)

    recmdFlg = BooleanField("おすすめ")

    # 画像用 FileField、拡張子を限定
    imageFile = FileField("画像", validators=[FileAllowed(['jpg','png','jpeg','gif'], "画像ファイルのみ許可")])

