import os
from datetime import date, datetime
# from pprint import pprint
# from time import sleep

import pandas as pd
import requests
import schedule
from bs4 import BeautifulSoup
from janome.analyzer import Analyzer
from janome.tokenfilter import CompoundNounFilter, POSKeepFilter, POSStopFilter
from requests.exceptions import RequestException

# NEWS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "models/news")
NEWS_DIR = "./models/news"
URL = {
    "yahoo": "https://news.yahoo.co.jp/ranking/access/news/domestic",
    "goo": "https://news.goo.ne.jp/ranking/nation/",
    "dmenu": "https://topics.smt.docomo.ne.jp/ranking/nation",
    "excite": "https://www.excite.co.jp/news/view-ranking/domestic-topic/",
    "jiji": "https://sp.m.jiji.com/ranking/newest",
    "mainichi": "https://mainichi.jp/ranking/",
    "nikkei": "https://www.nikkei.com/access/index/?bd=hKijiSougou",
}
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/108.0.0.0 Safari/537.36"


class News:
    def __init__(self) -> None:
        self.media = ""
        self.url = ""
        self.dir = f"{NEWS_DIR}/{date.today().strftime('%Y-%m-%d')}"
        self.file_name = ""
        self.df_news = pd.DataFrame()

    def fetch_news(self, file_save: bool = True):
        """Webページからニュース一覧を取得する"""
        headers = {"UserAgent": USER_AGENT}
        res = requests.get(self.url, headers=headers, timeout=(3.0, 7.5))
        try:
            res.raise_for_status()
        except RequestException as e:
            print(e)
            # TODO: logger.exception("request failed. error=(%s)", e.response.text)
            return
        self._parse_html(res.text)
        self._tokenize()
        if file_save:
            self._store_news()

    def _parse_html(self, text: str) -> None:
        """HTMLからニュース情報を取得し、self.df_news を更新する（Mediaごとにオーバーライドする）"""
        pass

    def _tokenize(self) -> None:
        """ニュース見出しを分かち書きし、self.df_news を更新する"""
        token_filters = [
            CompoundNounFilter(),
            POSKeepFilter("名詞"),
            # POSKeepFilter(["名詞", "動詞", "形容詞"]),
            POSStopFilter(["名詞,代名詞", "名詞,非自立", "名詞,数"]),
        ]
        a = Analyzer(token_filters=token_filters)

        news_list = self.df_news["title"].to_list()
        words_wakati = []
        for item in news_list:
            tokens = a.analyze(item)
            word_list = [token.surface for token in tokens]
            words_wakati.append(" ".join(word_list))
        self.df_news["words"] = words_wakati

    def _store_news(self) -> None:
        # TODO: Database
        os.makedirs(self.dir, exist_ok=True)
        with open(os.path.join(self.dir, self.file_name), "w") as f:
            self.df_news.to_csv(f, index=False)


class YahooNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "yahoo"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select("#contentsWrap > div.newsFeed > ol > li > a")
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            item_title = item.select(
                "div.newsFeed_item_text > div.newsFeed_item_title"
            )[0]
            _title = item_title.text.replace("…", " ").replace("\u3000", " ")
            _url = item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class GooNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "goo"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select(
            "section.gn-container > div.column-1 > ul > li > a"
        )
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            item_title = item.select("p.list-title-news")[0]
            _title = item_title.text.replace("…", " ").replace("\u3000", " ")
            _url = "https://news.goo.ne.jp" + item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class DmenuNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "dmenu"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select(
            "#wrapper > #content > #newsranking > div.m-newsRanking > ul > li > a"
        )
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            item_title = item.select("div.rankingText > h3.rankingTitle")[0]
            _title = item_title.text.replace("…", " ").replace("\u3000", " ")
            _url = "https://topics.smt.docomo.ne.jp" + item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class ExciteNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "excite"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select("main > div.content > ul > li > a")
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            item_title = item.select("div.list-body > p.title")[0]
            _title = item_title.text.replace("…", " ").replace("\u3000", " ")
            _url = item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class NikkeiNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "nikkei"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select(
            "#JSID_baseCheckMaxRkichiran > div > ul > li > span.m-miM32_itemTitle > span.m-miM32_itemTitleText > a"
        )
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            _title = item.text.replace("…", " ").replace("\u3000", " ")
            _url = "https://www.nikkei.com" + item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class JijiNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "jiji"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select(
            "#main > main > section > ol.ranking > li.ranking__item > a"
        )
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            _title = (
                item.text.strip()
                .split("\n")[-1]
                .strip()
                .replace("…", " ")
                .replace("\u3000", " ")
            )
            _url = item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


class MainichiNews(News):
    def __init__(self) -> None:
        super().__init__()
        self.media = "mainichi"
        self.url = URL[self.media]
        self.file_name = f"{self.media}_{date.today().strftime('%Y%m%d')}.csv"

    def _parse_html(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
        soup_item_list = soup.select("section#ranking-body > ul.articlelist > li > a")
        news: list[dict] = []
        for i, item in enumerate(soup_item_list, 1):
            item_title = item.select("div.articlelist-detail > h3")[0]
            _title = item_title.text.replace("…", " ").replace("\u3000", " ")
            _url = item.attrs["href"]
            item_dict = {
                "media": self.media,
                "date": date.today(),
                "ranking": i,
                "title": _title,
                "url": _url,
            }
            news.append(item_dict)
        self.df_news = pd.DataFrame(news)


def main():
    print("------------------------------------")
    print(f"Crawl at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    YahooNews().fetch_news()
    GooNews().fetch_news()
    DmenuNews().fetch_news()
    ExciteNews().fetch_news()
    NikkeiNews().fetch_news()
    JijiNews().fetch_news()
    MainichiNews().fetch_news()
    print("End")


schedule.every(15).minutes.do(main)


if __name__ == "__main__":
    main()
    # while True:
    #     schedule.run_pending()
    #     sleep(1)
