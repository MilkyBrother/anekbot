import requests
import sqlite3
from bs4 import BeautifulSoup as bs

URLS = ["https://www.anekdot.ru/release/anekdot/day/"]


def site_parse(url):
    r = requests.get(url)
    print('status', r.status_code)
    soup = bs(r.text, "html.parser")
    return soup


def insert_to_database(soup, database: str):
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
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    for anek in soup.find_all('div', class_='text'):
        data_to_insert = anek.text
        cursor.execute(insert_data_query, (data_to_insert,))
        conn.commit()
    conn.close()


def get_aneks_to_db():
    pass
