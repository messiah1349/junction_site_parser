import sys
sys.path.append('../links_extractor/')
from articles_db import Articles, get_all_rows, ChunkedArticles, get_session
from langchain.text_splitter import RecursiveCharacterTextSplitter

sql_url = 'sqlite:///../links_extractor/data/main.db'
articles = get_all_rows(url=sql_url)

texts = [article[0].text for article in articles]
links = [{'source': article[0].link} for article in articles]


# Text splitter
chunk_size = 300
chunk_overlap = 50
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    add_start_index=True,
)

print(len(links), len(texts))

# Chunk a sample section
chunks = text_splitter.create_documents(
    texts=texts, 
    # metadatas=[{"source": links}]
    metadatas=links
)

chunked_articles = []

for chunk in chunks:
    new_item = ChunkedArticles(text=chunk.page_content, link=chunk.metadata['source'])
    chunked_articles.append(new_item)


session = get_session(sql_url)
session.add_all(chunked_articles)
session.commit()
