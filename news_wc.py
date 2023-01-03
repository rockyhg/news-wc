import base64
import random
from datetime import datetime
from io import BytesIO

import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

from models.database import db_session
from models.models import News
from utils import jp_today

NEWS_DIR = "./models/news"
FONT_PATH = "./static/fonts/NotoSansJP-Bold.otf"
MASK_PATH = "./static/images/cloud.jpeg"
# "./static/images/bubble.jpeg"
WC_PATH = "./static/images/wordcloud.png"
HIGH_TFIDF_THRESHOLD = 0.1


class NewsWordcloud:
    """ワードクラウドを生成し、画像ファイルに保存する
    news_words: str
        ニュースの単語（スペース区切り）
    date_str: str
        ニュースの日付 (YYYY-MM-DD) -> ファイル名"""

    def __init__(self, news_words: str, file_save: bool = False) -> None:
        if not news_words:
            print("データがありません")
            return
        self.news_words = news_words
        self.tfidf_dict = dict()
        self.high_rank_news = []

        # TF-IDFで重み付け
        vectorizer = TfidfVectorizer()
        tfidf_vec = vectorizer.fit_transform([self.news_words]).toarray().reshape(-1)
        words = vectorizer.get_feature_names_out()
        self.tfidf_dict = dict(zip(words, tfidf_vec))

        _stop_words = []
        _mask = np.array(Image.open(MASK_PATH))

        wc = WordCloud(
            font_path=FONT_PATH,
            # width=1600, height=900,
            background_color="white",
            colormap=self._choose_colormap(),
            stopwords=set(_stop_words),
            max_font_size=None,
            min_font_size=4,
            max_words=300,
            random_state=99,
            mask=_mask,
        ).generate_from_frequencies(self.tfidf_dict)

        self.wc_img = wc.to_image()
        if file_save:
            wc.to_file(WC_PATH)
        self._get_high_rank_news()

    def _choose_colormap(self) -> str:
        colormap_candidate = ["viridis", "plasma", "inferno", "magma", "cividis"]
        return random.choice(colormap_candidate)

    def _get_high_rank_news(self):
        # tf-idf上位の単語を取得
        tfidf_sorted = sorted(self.tfidf_dict.items(), key=lambda x: x[1], reverse=True)
        high_rank_words = [word for (word, tfidf) in tfidf_sorted if tfidf > HIGH_TFIDF_THRESHOLD]
        # 上位単語を含むニュースを抽出
        for word in high_rank_words:
            news = db_session.query(News).filter(News.words.like(f'%{word}%')).all()
            item = random.choice(news)  # ランダムに1件抽出
            item_dict = {
                'word': word,
                'title': item.title,
                'url': item.url
            }
            self.high_rank_news.append(item_dict)

    def to_base64(self) -> str:
        """WordCloud画像をHTML埋め込み用に変換する"""
        buf = BytesIO()
        self.wc_img.save(buf, "png")
        base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        base64_data = f"data:image/png;base64,{base64_str}"
        return base64_data


def get_words_from_db(date_str: str = None) -> str:
    """DBから news_words を取得
    date_str: str
        ニュースの日付 (YYYY-MM-DD)"""
    if not date_str:
        news_date = jp_today()
    else:
        news_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    news_data = db_session.query(News).filter_by(date=news_date).all()
    if news_data == []:
        return ""
    words_list = [news.words for news in news_data]
    return " ".join(words_list)


if __name__ == "__main__":
    words = get_words_from_db()
    news_wc = NewsWordcloud(words, file_save=True)
    # from pprint import pprint
    # pprint(news_wc.high_rank_news)
