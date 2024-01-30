import requests
import database_api as db
from bs4 import BeautifulSoup as bs


class AnekdotruParser:
    def __init__(self, base_url, data_base):
        self.base_url = base_url
        self.data_base = data_base

    @staticmethod
    def _load_page(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f'Failed to load page: {url}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'Requests error: {e}')
            return None

    @staticmethod
    def _parse_data(html) -> list:
        site_soup = bs(html, 'html.parser')
        parsed_data = []
        for anek in site_soup.find_all('div', class_='text'):
            parsed_data.append(anek.text)
        return parsed_data

    @staticmethod
    def _process_data(parsed_data):
        db.insert_aneks_to_akekidb(data=parsed_data)

    def run(self):
        page_content = self._load_page(url=self.base_url)
        if page_content:
            data = self._parse_data(html=page_content)
            if data:
                self._process_data(parsed_data=data)


if __name__ == '__main__':
    parser = AnekdotruParser(base_url='https://www.anekdot.ru/release/anekdot/day/', data_base='aneki.db')
    parser.run()
