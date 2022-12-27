import base64
import os
import random
from datetime import date
from glob import glob
from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

NEWS_DIR = "./models/news"
FONT_PATH = "./static/fonts/NotoSansJP-Bold.otf"
MASK_PATH = "./static/images/cloud.jpeg"
# "./static/images/bubble.jpeg"
TODAY_WC_PATH = "./static/images/today_wc.png"
PAST_WC_PATH = "./static/images/past_wc.png"


class NewsWordcloud:
    """ワードクラウドを生成し、画像ファイルに保存する
    news_date: str
        ニュースの日付 ("yyyy-mm-dd")"""
    def __init__(self, date_str: str = None, file_save: bool = False) -> None:
        if date_str:
            self.date_str = date_str
            self.save_path = PAST_WC_PATH
        else:
            self.date_str = date.today().strftime("%Y-%m-%d")
            self.save_path = TODAY_WC_PATH

        self.news_words = self._set_news_words()

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
            random_state=99,
            mask=_mask,
        ).generate_from_frequencies(tfidf_dict)

        self.wc_img = wc.to_image()
        if file_save:
            self._clean_cache()
            wc.to_file(self.save_path)

    def _set_news_words(self) -> str:
        """DBから news_words を取得"""
        dir = f"{NEWS_DIR}/{self.date_str}"
        news_file_list = glob(os.path.join(dir, "*.csv"))
        words_list = []
        for news_file in news_file_list:
            with open(news_file, "r") as f:
                df_news = pd.read_csv(f)
            words = df_news["words"].to_list()
            words_list.append(" ".join(words))
        return " ".join(words_list)

    def _choose_colormap(self) -> str:
        colormap_candidate = ["viridis", "plasma", "inferno", "magma", "cividis"]
        return random.choice(colormap_candidate)

    def _clean_cache(self):
        """前に保存した画像を削除する"""
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

    def to_base64(self) -> str:
        '''WordCloud画像をHTML埋め込み用に変換する'''
        buf = BytesIO()
        self.wc_img.save(buf, 'png')
        base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        base64_data = f"data:image/png;base64,{base64_str}"
        return base64_data


if __name__ == "__main__":
    news_wc = NewsWordcloud(file_save=True)
    # img_data = news_wc.to_base64()
    # print(img_data)
