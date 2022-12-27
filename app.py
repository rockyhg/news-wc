from flask import Flask, render_template  # , request

from models.models import get_date_list
from news_wc import NewsWordcloud


app = Flask(__name__)


@app.route("/")
def index():
    # news_wc = NewsWordcloud()
    # wc_img_data = news_wc.to_base64()
    # date_list = get_date_list()
    # return render_template("index.html", todays_wc=wc_img_data, date_list=date_list)
    return render_template("index.html")


# @app.route("/", methods=["POST"])
# def post():
#     date = request.form.get("date", "")
#     print(date)
#     NewsWordcloud(date)
#     date_list = get_date_list()
#     return render_template("index.html", date_list=date_list)


if __name__ == "__main__":
    app.run(debug=False)
