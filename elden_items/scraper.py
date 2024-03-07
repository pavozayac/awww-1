from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from functools import reduce
from duckduckgo_search import DDGS
import os

BASE_URL = 'https://eldenring.wiki.fextralife.com'
TALISMAN_BASE_PATH = './elden_talismans/_talismans/'
SEARCH_BASE_PATH = './elden_talismans/_searches/'


class Talisman:
    def __init__(self, name: str, site: str, img: str, desc: str, lore: str) -> None:
        self.name = name
        self.site = site
        self.img = img
        self.desc = desc
        self.lore = lore

    def get_ddgs(self):
        pass

    def write_list_to_file(self):
        if not os.path.exists(TALISMAN_BASE_PATH):
            os.makedirs(TALISMAN_BASE_PATH)

        with open(f'{TALISMAN_BASE_PATH}{self.name.replace(" ", "")}.md', 'w') as file:

            file.write('---\n')
            file.write('layout: post\n')
            file.write(f'title: {self.name}\n')
            file.write(f'name: {self.name}\n')
            file.write(f'desc: {self.desc}\n\n')

            # file.write('categories: talisman\n')
            # file.write('permalink: /' + self.name.replace(' ', '') + '\n')
            file.write('---\n')
        
            file.write(f'# {self.name}\n')
            file.write(f'[Link to a detailed website]({self.site})' + '{:target="_blank"}' + '\n\n')
            file.write(f'![Icon of {self.name}]({self.img})\n\n')
            file.write(f'{self.desc}\n\n')
            file.write('>*' + self.lore.replace('\n', '').strip() + '*')
            file.write('\n')
            file.write('\n')
            file.write(f'[DuckDuckGo searches related to this talisman](/searches/' + self.name.replace(' ', '') + ')\n\n')
            file.write('\n')

        if not os.path.exists(SEARCH_BASE_PATH):
            os.makedirs(SEARCH_BASE_PATH)

        with open(f'{SEARCH_BASE_PATH}{self.name.replace(" ", "")}.md', 'w') as file:
            file.write('---\n')
            file.write('layout: post\n')
            file.write(f'title: {self.name} DuckDuckGo search results\n')
            # file.write(f'name: {self.name}\n')
            # file.write(f'desc: {self.desc}\n\n')
            file.write('---\n')

            for result in DDGS().text(self.name, max_results=5):
                file.write('* #### [' + result['title'] + '](' + result['href'] + '){:target="blank"}\n')
                file.write(result['body'] + '\n')

            
            


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

            if len(results) > 1:
                break

    return results


if __name__ == '__main__':
    scrape()

    for talisman in scrape():
        talisman.write_list_to_file()
