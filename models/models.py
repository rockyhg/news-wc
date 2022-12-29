# coding: utf-8
from datetime import datetime as dt

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from models.database import Base


class News(Base):
    __tablename__ = "news"

    # Columns
    id = Column(Integer, primary_key=True)
    media = Column(String(128), unique=False)
    date = Column(Date, unique=False)
    ranking = Column(Integer, unique=False)
    title = Column(Text, unique=False)
    url = Column(String(256), unique=False)
    words = Column(Text, unique=False)
    timestamp = Column(DateTime, default=dt.now())

    def __init__(
        self,
        media=None,
        date=None,
        ranking=None,
        title=None,
        url=None,
        words=None,
        timestamp=None,
    ):
        self.media = media
        self.date = date
        self.ranking = ranking
        self.title = title
        self.url = url
        self.words = words
        self.timestamp = timestamp
