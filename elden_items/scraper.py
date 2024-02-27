from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from functools import reduce
from duckduckgo_search import DDGS

BASE_URL = 'https://eldenring.wiki.fextralife.com'


class Talisman:
    def __init__(self, name: str, site: str, img: str, desc: str, lore: str) -> None:
        self.name = name
        self.site = site
        self.img = img
        self.desc = desc
        self.lore = lore
            
    def write_list_to_file(self, file):
        file.write(f'# {self.name}\n')
        # file.write('---\n')
        file.write(f'[Link to a detailed website]({self.site})\n')
        file.write(f'![Icon of {self.name}]({self.img})\n\n')
        file.write(f'{self.desc}\n\n')
        file.write(reduce(lambda a, b: a + b, map(lambda line: '>*'+line+'*\n', self.lore.split('\n')))+'\n')
        file.write('\n')

    def get_ddgs(self):
        with DDGS() as ddgs:
            return ddgs.answers(self.name)


def get_page(url):
    response = requests.get(url)
    return response.content


def scrape() -> list[Talisman]:
    url = urljoin(BASE_URL, '/Talismans')
    page = get_page(url)
    soup = BeautifulSoup(page, 'html.parser')

    talismans = soup.find_all('a', class_='wiki_link wiki_tooltip')

    results = []

    for talisman in talismans:
        if talisman.find('img') is not None:
            talisman_page = get_page(urljoin(BASE_URL, talisman['href']))

            talisman_soup = BeautifulSoup(talisman_page, 'html.parser')

            lore_div = talisman_soup.find_all('div', class_='lineleft')[1]

            results.append(Talisman(
                name=talisman.text,
                site=urljoin(BASE_URL, talisman['href']),
                img=urljoin(BASE_URL, talisman.find('img')['src']),
                desc=talisman.parent.parent.parent.find('p').text,
                lore=lore_div.text,
            ))

    return results


if __name__ == '__main__':
    scrape()

    with open('./talisman.md', 'w') as file:
        for talisman in scrape():
            talisman.write_list_to_file(file)
