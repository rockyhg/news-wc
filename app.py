from flask import Flask, render_template

from news_wc import NewsWordcloud, get_words_from_db
from utils import jp_today, generate_news_text

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    words = get_words_from_db()
    news_wc = NewsWordcloud(words)
    wc_img_data = news_wc.to_base64()
    news_list = news_wc.high_rank_news
    high_rank_words = " ".join([item["word"] for item in news_wc.high_rank_news])
    text = generate_news_text(high_rank_words)

    return render_template(
        "index.html",
        todays_date=jp_today().strftime("%Y-%m-%d"),
        todays_wc=wc_img_data,
        news_list=news_list,
        words_for_gen=high_rank_words,
        generated_text=text
    )


# @app.route("/generate", methods=["GET"])
# def update():
#     text = generate_news_text(high_rank_words)
#     return render_template(
#         "generate.html",
#         todays_date=jp_today().strftime("%Y-%m-%d"),
#         todays_wc=wc_img_data,
#         news_list=news_list,
#         generated_text=text
#     )


if __name__ == "__main__":
    app.run(debug=False)
