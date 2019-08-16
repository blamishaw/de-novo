from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl, csv
import mysql.connector

context = ssl._create_unverified_context()

def make_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req, context=context).read()
    page_html = web_byte.decode('utf-8')

    return BeautifulSoup(page_html, "html.parser")

def connect_to_database():
    return mysql.connector.connect(
                host='localhost',
                user='root',
                password='denovosql',
                database='my_database'
            )



