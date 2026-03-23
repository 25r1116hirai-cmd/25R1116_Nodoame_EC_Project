from flask import Blueprint, render_template


shop = Blueprint("shop",__name__)

@shop.route("/")
def index():

    
    return render_template("shop/index.html")