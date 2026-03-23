from flask import Flask, render_template
from routes.shop import shop
from routes.checkout import checkout
from routes.admin import admin
app = Flask(__name__, template_folder="app/templates")

app.register_blueprint(shop, url_prefix="/shop")
app.register_blueprint(checkout, url_prefix="/checkout")
app.register_blueprint(admin, url_prefix="/admin")

print(type(shop))

@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)


  