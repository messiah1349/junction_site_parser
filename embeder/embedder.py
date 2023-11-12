from links_extractor.articles_db import Articles, get_all_rows, ChunkedArticles, get_session
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import psycopg2
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.vectorstores.pgvector import PGVector
from embeder.vector_db import add_vector
import numpy as np

sql_url = 'sqlite:///links_extractor/data/main.db'
articles = get_all_rows(table=ChunkedArticles, url=sql_url)

texts = [article[0].text for article in articles]
links = [article[0].link for article in articles]


class Embedder:

    def __init__ (self,
            model_name:str,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"device": "cpu", "batch_size": 100},
    ):

        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

    def embedd(self, texts: list[str]):
        embeddings = self.model.embed_documents(texts)
        return embeddings

if __name__ == "__main__":

    model_name = 'thenlper/gte-base'
    embedder = Embedder(model_name=model_name)
    embeddings = embedder.embedd(texts)
    print(len(embeddings[0]))

    for link, text, embedding in zip(links, texts, embeddings):
        embedding = np.array(embedding)
        add_vector(link, text, embedding)
