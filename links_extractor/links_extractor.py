import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url_mask = 'https://steelnews.biz/steel-news/page/{page_num}/' 
 
def get_links_from_site(url: str) -> set[str]:

    html_page = urlopen(url)

    soup = BeautifulSoup(html_page, "lxml")

    links = set()
    for link in soup.findAll('a'):
        links.update((link.get('href'),))

    return links

def wirte_link_to_file(links: set[str]):
    with open('links/links.txt', 'a') as f:
        for link in links:
            if 'steel-news/page' in link:
                continue
            f.write(f"{link}\n")

url2 = 'https://steelnews.biz/steel-news/page/2/'
url3 = 'https://steelnews.biz/steel-news/page/3/'

links2 = get_links_from_site(url2)
links3 = get_links_from_site(url3)

connom_articles = links2 & links3
separate_articles = links2.symmetric_difference(links3)
wirte_link_to_file(separate_articles)

# print(f"{connom_articles=}")
# print()
# print(f"{separate_articles=}")

for ix in range(4, 51):
    print(f"{ix=}")
    url = url_mask.format(page_num=ix)
    links = get_links_from_site(url)
    new_links = links - connom_articles

    wirte_link_to_file(new_links)
    # separate_articles = separate_articles | new_links

    
