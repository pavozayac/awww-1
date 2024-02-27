from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

BASE_URL = 'https://eldenring.wiki.fextralife.com'


class Talisman:
    def __init__(self, name: str, site: str, img: str, desc: str) -> None:
        self.name = name
        self.site = site
        self.img = img
        self.desc = desc
            
    def write_list_to_file(self, file):
        file.write(f'# {self.name}\n')
        # file.write('---\n')
        file.write(f'[Link to a detailed website]({self.site})\n')
        file.write(f'![Icon of {self.name}]({self.img})\n\n')
        file.write(f'{self.desc}\n')
        file.write('\n')


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
            results.append(Talisman(
                name=talisman.text,
                site=urljoin(BASE_URL, talisman['href']),
                img=urljoin(BASE_URL, talisman.find('img')['src']),
                desc=talisman.parent.parent.parent.find('p').text
            ))

    return results


if __name__ == '__main__':
    scrape()

    with open('./talisman.md', 'w') as file:
        for talisman in scrape():
            talisman.write_list_to_file(file)
