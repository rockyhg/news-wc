from flask import Flask, render_template  # , request

# from models.models import get_date_list
from news_wc import NewsWordcloud, get_words_from_csv, get_words_by_crawling


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # date_list = get_date_list()
    # words = get_words_from_csv()
    words = get_words_by_crawling()
    news_wc = NewsWordcloud(words, file_save=False)
    wc_img_data = news_wc.to_base64()
    return render_template("index.html", todays_wc=wc_img_data)
    # return render_template("index.html", todays_wc=news_wc.save_path)

# @app.route("/", methods=["POST"])
# def post():
#     date = request.form.get("date", "")
#     print(date)
#     NewsWordcloud(date)
#     date_list = get_date_list()
#     return render_template("index.html", date_list=date_list)


if __name__ == "__main__":
    app.run(debug=False)
