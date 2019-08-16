""" This is a web scraper class file. Websites included are:
  1. IRLG: America's Largest 350 Firms
          (https://www.ilrg.com/nlj250?)
  2. Wikipedia: List of largest law firms by revenue
          (https://en.wikipedia.org/wiki/List_of_largest_law_firms_by_revenue)
  3. Chambers Associate (CA): A to Z Firm List
          (http://www.chambers-associate.com/law-firms/a-to-z-firm-list)


Genereal Structure
  string: main_url = homepage of website we are scraping
  method: click_link (if applicable) -> clicks a link on a page and return an HTML soup
  method: parse_page -> parses the relevant data from a webpage and inputs it into a dictionary
  method: scrape -> calls parse_page and returns a list of dictionaries containing firm information

It is important that dictionary keys are consistent across scrapers otherwise there may be duplicates in
the MySQL database """

from bs4 import NavigableString

from driver import make_soup
from helper import *


class IRLG_Scraper:
    """ Class that scrapes https://www.ilrg.com/nlj250? """

    main_url = 'https://www.ilrg.com/nlj250?'

    def __init__(self):
        self._firms = []
        self._soup = make_soup(self.main_url)
        self._page = 1

    def click_link(self):
        self._page += 1
        self._soup = make_soup(f"https://www.ilrg.com/nlj250?page={self._page}")
        self.parse_page(self._soup)


    def parse_page(self, soup):
        parse = []

        for i, x in enumerate(soup.find_all('tr')):
            if i > 2:
                line = x.get_text().splitlines()
                line = [s for s in line if s != ""]
                parse.append(line)

        for i in parse:
            firm = {"name": i[1],
                    "city": i[2],
                    "attorneys": i[3],
                    "growth": float(i[7][:-1])
                    }
            self._firms.append(firm)

        if self._page < 4:
            self.click_link()

    def scrape(self) -> list[dict]:
        """ :rtype List[dicts]"""

        self.parse_page(self._soup)
        return self._firms


class WikiScraper1:
    """ Class that scrapes from https://en.wikipedia.org/wiki/List_of_largest_law_firms_by_revenue"""

    main_url = 'https://en.wikipedia.org/wiki/List_of_largest_law_firms_by_revenue'

    def __init__(self):
        self._firms = []
        self._soup = make_soup(self.main_url)

    def parse_page(self):
        parse = []

        for i, x in enumerate(self._soup.find_all('tr')):
            if i > 0:
                line = x.get_text().splitlines()
                line = [s for s in line if s != ""]
                parse.append(line)

        for i in parse:
            firm = {"name": i[1],
                    "revenue": i[2],
                    "country": i[5]
                    }
            self._firms.append(firm)

    def scrape(self):
        """:rtype List[dicts]"""

        self.parse_page()
        return self._firms

class CAScraper:
    """ Class that scrapes from http://www.chambers-associate.com/law-firms/a-to-z-firm-list """

    main_url = 'http://www.chambers-associate.com/law-firms/a-to-z-firm-list'

    def __init__(self):
        self._firms = []
        self._soup = make_soup(self.main_url)

    def parse_main_page(self):
        links = []
        for x in self._soup.find_all("div", class_="letter-container"):
            for y in x.find_all("div"):
                try:
                    links.append(y.a['href'])
                except:
                    pass
        self.click_links(links)

    def click_links(self, links):
        for i, link in enumerate(links):
            print("Parsing page: {}".format(i))
            if i not in [4, 22, 24, 29, 38, 49, 50, 63, 73, 88, 89, 105, 109]:
                page_soup = make_soup(f'http://www.chambers-associate.com{link}')
                self.parse_individual_page(page_soup)

    def parse_individual_page(self, soup):
        """ This website is  terrible formatted and the scraper reflects that.
            Lots of try-excepts because the main areas for each firm are located in
            completely different areas
        """

        name = soup.find('h1').get_text().replace(' - The Inside View', '')

        try:
            info = [t for t in soup.find('div', class_="profile").p]
        except:
            info = ["", ""]

        try:
            if isinstance(info[2], NavigableString):
                main_areas = info[2]
            else:
                main_areas = info[1]
        except IndexError:
            main_areas = None

        try:
            if info[3]['class']:
                main_areas = info[4]
        except (KeyError, IndexError, TypeError):
            pass

        if main_areas:
            main_areas = remove_multiple(str(main_areas), [' \r\n        ', '• '])

        firm = {'name': name,
                'mainAreas': main_areas}

        self._firms.append(firm)

    def scrape(self):
        """ :rtype List[dicts] """

        self.parse_main_page()
        return self._firms
