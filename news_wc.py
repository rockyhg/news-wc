import base64
import os
import random
from datetime import date, datetime
from glob import glob
from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

from models.database import db_session
from models.models import News

NEWS_DIR = "./models/news"
FONT_PATH = "./static/fonts/NotoSansJP-Bold.otf"
MASK_PATH = "./static/images/cloud.jpeg"
# "./static/images/bubble.jpeg"
WC_DIR = "./static/images"
TODAY_WC_PATH = "./static/images/today_wc.png"
PAST_WC_PATH = "./static/images/past_wc.png"


class NewsWordcloud:
    """ワードクラウドを生成し、画像ファイルに保存する
    news_words: str
        ニュースの単語（スペース区切り）
    date_str: str
        ニュースの日付 (YYYY-MM-DD) -> ファイル名"""

    def __init__(
        self, news_words: str, date_str: str = None, file_save: bool = False
    ) -> None:
        if not news_words:
            print('データがありません')
            return
        self.news_words = news_words
        if not date_str:
            date_str = date.today().strftime("%Y-%m-%d")
        self.save_path = os.path.join(WC_DIR, f"wc_{date_str}.png")

        # TF-IDFで重み付け
        vectorizer = TfidfVectorizer()
        tfidf_vec = vectorizer.fit_transform([self.news_words]).toarray().reshape(-1)
        words = vectorizer.get_feature_names_out()
        tfidf_dict = dict(zip(words, tfidf_vec))

        _stop_words = []
        _mask = np.array(Image.open(MASK_PATH))

        wc = WordCloud(
            font_path=FONT_PATH,
            # width=1600,
            # height=900,
            background_color="white",
            colormap=self._choose_colormap(),
            stopwords=set(_stop_words),
            max_font_size=None,
            min_font_size=4,
            max_words=300,
            # random_state=99,
            mask=_mask,
        ).generate_from_frequencies(tfidf_dict)

        self.wc_img = wc.to_image()
        if file_save:
            # self._clean_cache()
            wc.to_file(self.save_path)

    def _choose_colormap(self) -> str:
        colormap_candidate = ["viridis", "plasma", "inferno", "magma", "cividis"]
        return random.choice(colormap_candidate)

    def _clean_cache(self):
        """前に保存した画像を削除する"""
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

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
        news_date = date.today()
    else:
        news_date = datetime.strptime(date_str, "%Y-%m-%d")
    # 指定した日付の行を検索
    news_data = db_session.query(News).filter_by(date=news_date).all()
    if news_data == []:
        return ""
    words_list = [news.words for news in news_data]
    return " ".join(words_list)


if __name__ == "__main__":
    words = get_words_from_db()
    # print(words)
    news_wc = NewsWordcloud(words, file_save=True)
    # img_data = news_wc.to_base64()
    # print(img_data)
