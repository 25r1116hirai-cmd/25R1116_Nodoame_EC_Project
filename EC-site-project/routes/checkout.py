from flask import Blueprint, render_template


checkout = Blueprint("checkout",__name__)


@checkout.route("/")
def index():


    return render_template("checkout/confirm.html")