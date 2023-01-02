# coding: utf-8
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://nfgauqauvwafae:cddeab18de5706a0bd700dad56c59a5f81c72d5e204cb058aced438d1f4ac624@ec2-52-54-212-232.compute-1.amazonaws.com:5432/d6klbef1mfhlj7"

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "news.sqlite")
engine = create_engine(
    DATABASE_URL,
    # "sqlite:///" + databese_file,
    convert_unicode=True,
    echo=False,
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.models

    Base.metadata.create_all(bind=engine)
