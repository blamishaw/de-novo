""" This is a web scraper class file. Websites included are:
        1. Altman Weil: MergerLine
            (http://www.altmanweil.com/index.cfm/fa/m.home/bl/1/dtYear/2019/altman-weil-merger-line-for-2019.cfm)
        2. Reuters News
            (https://www.reuters.com/)
        3. AbovetheLaw
            (https://abovethelaw.com/)


Genereal Structure
  string: main_url = homepage of website we are scraping
  method: click_link (if applicable) -> clicks a link on a page and return an HTML soup
  method: parse_page -> parses the relevant data from a webpage and inputs it into a dictionary
  method: scrape -> calls parse_page and returns a list of dictionaries containing firm information

It is important that dictionary keys are consistent across scrapers otherwise there may be duplicates in
the MySQL database """

from driver import make_soup
from readdata import ReadData
from helper import *


class MergerLineScraper:
    main_url = 'http://www.altmanweil.com/index.cfm/fa/m.home/bl/1/dtYear/2019/altman-weil-merger-line-for-2019.cfm'

    def __init__(self):
        self._firms = []
        self._soup = make_soup(self.main_url)

    def parse_page(self):
        table = self._soup.find_all('tr')

        for i in range(7, len(table)-2):
            data = table[i].find_all('td')

            if int(data[4].get_text()) > 99:

                firm = {'name': data[2].get_text(),
                        'acquired': data[6].get_text()}

                self._firms.append(firm)

    def scrape(self):
        self.parse_page()
        return self._firms

class ReutersScraper:
    """ No main_url on this one as we are not scraping from a main page
        Firms are stored as {firm_name: List[(article_title, link),]},
    """

    def __init__(self):
        self._firms = []

    def special_chars_to_hex(self, name, toReplace):
        for c in toReplace:
            name = name.replace(c, '%' + hex(ord(c))[-2:])
        return name

    def get_page(self, name: str):
        name = self.special_chars_to_hex(name, [" ", "'", "&"])
        name = name.split(' (')[0]

        return make_soup(f'https://www.reuters.com/search/news?sortBy=&dateRange=&blob={name}')

    def parse_pages(self, names):
        for i, (ID, name) in enumerate(names):
            print('Parsing name: {}'.format(i))
            soup = self.get_page(name)

            results = soup.find_all('div', class_="search-result-indiv")

            for i in range(len(results)-3):
                if results[i].img:
                    continue
                headline = results[i].a.get_text()
                link = 'https://www.reuters.com' + results[i].a['href']
                time_posted = results[i].h5.get_text()

                self._firms.append(
                    {'name': name,
                     'headline': headline,
                     'link': link,
                     'time_posted': time_posted}
                )

    def scrape(self):
        names = ReadData().get_all_names()
        self.parse_pages(names)
        return self._firms


class AboveTheLawScraper(ReutersScraper):
    """ No main_url on this one as we are not scraping from a main page
        Firms are stored as {firm_name: List[(article_title, link),]},

        This class inherits from ReutersScraper as many of the class methods are the same
    """

    def __init__(self):
        super().__init__()

    def get_page(self, name: str):
        name = super().special_chars_to_hex(name, [" ", "'", "&"])
        name = name.split(' (')[0]

        return make_soup(f'https://abovethelaw.com/?s={name}')

    def parse_pages(self, names):
        for i, (ID, name) in enumerate(names):
            print(f'Parsing name {i}, {name}')
            soup = self.get_page(name)

            results = soup.find_all('div', class_="content", limit=5)


            for x in results:
                source = x.find('p', class_="title")
                if len(source) < 3:
                    break

                try:
                    headline = source.get_text().strip('\n')
                    time_posted = x.span.get_text()[3:]
                except AttributeError:
                    headline = ''
                    time_posted = ''

                self._firms.append(
                    {'name': name,
                     'headline': headline,
                     'link': source.a['href'],
                     'time_posted': time_posted,
                    }
                )

    def scrape(self):
        return super().scrape()

def push_to_json():
    a = AboveTheLawScraper()
    firm_data = a.scrape()

    convert_to_json('data.json', firm_data)


push_to_json()