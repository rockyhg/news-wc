from flask import Flask, render_template, request

from news_wc import NewsWordcloud
from models.models import get_date_list

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    NewsWordcloud()
    date_list = get_date_list()
    return render_template("index.html", date_list=date_list)


@app.route("/", methods=['POST'])
def post():
    date = request.form.get('date', '')
    print(date)
    NewsWordcloud(date)
    date_list = get_date_list()
    return render_template("index.html", date_list=date_list)
    # news_wc = NewsWordcloud()
    # wc = news_wc.generate_wordcloud(file_save=False)
    # wc_today = fig_to_base64_img(wc)


if __name__ == '__main__':
    app.run(debug=True)
