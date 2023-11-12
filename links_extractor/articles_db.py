import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime 
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()

from sqlalchemy.ext.declarative import declarative_base

class Articles(Base):

    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    text = Column(String)


class ChunkedArticles(Base):

    __tablename__ = 'chunked_articles'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    text = Column(String)

# def get_engine(postgre_password: str, postgre_port:str, postgre_host:str):
#     url = f'postgresql+psycopg2://postgres:{postgre_password}@{postgre_host}:{postgre_port}/emotion_bot'
#     engine = create_engine(url)
#     return engine


def get_engine(url="sqlite:///data/main.db"):
    engine = create_engine(url)
    return engine


def create_data_base_and_tables(engine):

    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"database was created, url={engine.url}")
    Base.metadata.create_all(engine)


def get_all_rows(table=Articles, url="sqlite:///data/main.db"):

    engine = get_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    row = session.execute(select(table)).all()
    return row

def get_session(url="sqlite:///data/main.db"):

    engine = get_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


if __name__ == '__main__':
    engine = get_engine()
    create_data_base_and_tables(engine)
