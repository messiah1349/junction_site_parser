from links_extractor.articles_db import Articles, get_all_rows, ChunkedArticles, get_session
import psycopg2
from pgvector.sqlalchemy import Vector
from sqlalchemy import create_engine, Column, Integer, String, DateTime 
from sqlalchemy.orm import sessionmaker
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.vectorstores.pgvector import PGVector
# from pgvector.psycopg2 import register_vector, connect
import numpy as np
from sqlalchemy import insert, select
from sqlalchemy.sql import text
from pgvector.sqlalchemy import Vector

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import database_exists, create_database

from constants.constants import POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER

# conn = psycopg2.connect(
#     host=POSTGRES_HOST,
#     database="vectordb",
#     user="user",
#     password=POSTGRES_PASSWORD
# )

# host="localhost"
# dbname="vectordb"
# user="testuser"
# password="testpwd"
# port=5432
# CONNECTION_STRING = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

def get_connection_string():
    user=POSTGRES_USER
    dbname="vectordb"
    host=POSTGRES_HOST
    password=POSTGRES_PASSWORD
    port='5432'

    CONNECTION_STRING = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    # print(f"{CONNECTION_STRING=}")

    return CONNECTION_STRING

CONNECTION_STRING = get_connection_string()
 

def get_engine(url=CONNECTION_STRING):
    engine = create_engine(url)
    return engine

def get_session(url=CONNECTION_STRING):

    engine = get_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def create_data_base_and_tables(engine):

    if not database_exists(engine.url):
        create_database(engine.url)
        # logger.info(f"database was created, url={engine.url}")
    Base.metadata.create_all(engine)


engine = get_engine()
session = get_session()
session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))


class VectorDB(Base):
    __tablename__ = 'vector_db'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    text = Column(String)
    embedding = mapped_column(Vector(768))

# session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
# session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))

# item = Item(embedding=np.array([1, 2, 3]))
# session.add(item)
# session.commit()


def add_vector(link: str, text: str, embedding: np.ndarray):
    # engine = get_engine()
    session = get_session()
    vecor_row = VectorDB(link=link, text=text, embedding=embedding)
    session.add(vecor_row)
    session.commit()

def get_top_neighbors(embedding: np.ndarray, k:int=5):
    session = get_session()
    top_k = session.scalars(select(VectorDB).order_by(VectorDB.embedding.l2_distance(embedding)).limit(k))
    return top_k


if __name__ == "__main__":
    create_data_base_and_tables(engine)

# conn = psycopg.connect(CONNECTION_STRING)
# register_vector(conn)
# cur = conn.cursor()
# create_query = "CREATE TABLE documents (text text, source text, embedding vector(3));"
# cur.execute(create_query)
# embedding = np.array([1, 2, 3])
# cur.execute('INSERT INTO documents (text, source, embedding) VALUES (%s, %s, %s)', ('aa', 'bb', embedding))

# engine=get_engine()
# session = get_session()
#
# db = PGVector.from_documents(
#     documents= docs,
#     embedding = embeddings,
#     collection_name= "blog_posts",
#     distance_strategy = DistanceStrategy.COSINE,
#     connection_string=CONNECTION_STRING)
#
#
# create_query = "CREATE TABLE documents (text text, source text, embedding vector(768));"
#
# cur = conn.cursor()
#
# cur.execute(create_query)
# cur.close()
