import requests
import sqlite3
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
    def _parse_data(html):
        site_soup = bs(html, 'html.parser')
        parsed_data = []
        for anek in site_soup.find_all('div', class_='text'):
            parsed_data.append(anek.text)
        return parsed_data

    def _process_data(self, parsed_data):
        create_table_query = '''
                CREATE TABLE IF NOT EXISTS aneki (
                    id INTEGER PRIMARY KEY,
                    text TEXT UNIQUE
                )
            '''
        insert_data_query = '''
                INSERT OR IGNORE INTO aneki (text)
                VALUES (?)
            '''
        conn = sqlite3.connect(self.data_base)
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        for anek in parsed_data:
            cursor.execute(insert_data_query, (anek,))
            conn.commit()
        conn.close()

    def run(self):
        page_content = self._load_page(url=self.base_url)
        if page_content:
            data = self._parse_data(html=page_content)
            if data:
                self._process_data(parsed_data=data)


if __name__ == '__main__':
    parser = AnekdotruParser(base_url='https://www.anekdot.ru/release/anekdot/day/', data_base='aneki.db')
    parser.run()
