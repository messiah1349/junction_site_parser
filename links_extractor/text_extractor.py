from bs4 import BeautifulSoup
from urllib.request import urlopen
from links_extractor.articles_db import Articles, get_engine
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker


engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def get_links() -> list[str]:
    with open('links/links.txt', 'r') as f:
        links = f.readlines()
    return links

links = get_links()

# links = links[:1]

articles = []
for link in links:
    # print(link)

    html_page = urlopen(link)
    soup = BeautifulSoup(html_page, "lxml")
    mydivs = soup.find_all("div", {"class": "entry-content"})
    # print(len(mydivs))
    # print(mydivs)
    try:
        el = mydivs[0]
        text = el.get_text(separator='. ')
        only_news = text.split('Latest news')[0]
        article = Articles(link=link, text=only_news)
        articles.append(article)
    except IndexError:
        print(link)

    # texts = el.find_all(string=True, recursive=True)
    # print(texts)
    # uf = urllib.request.urlopen(link)
    # html = uf.read()
    # print(html, '\n\n\n\n\n')

session.add_all(articles)
session.commit()
