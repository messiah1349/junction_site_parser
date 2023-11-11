from bs4 import BeautifulSoup
from urllib.request import urlopen
from articles_db import Articles, get_engine
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker


engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

row = session.execute(select(Articles)).first()
print(row[0].text)
