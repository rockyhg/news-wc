from flask import Flask, render_template

from news_wc import NewsWordcloud, get_words_from_db

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    words = get_words_from_db()
    news_wc = NewsWordcloud(words)
    wc_img_data = news_wc.to_base64()
    return render_template("index.html", todays_wc=wc_img_data, news_list=news_wc.high_rank_news)


if __name__ == "__main__":
    app.run(debug=False)
