# This is a driver program for all web scraping
# To scrape any website, simply edit the site-specific script found in another file

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
import csv

# abovethelaw should be changed to the name of the script file
from tests import abovethelaw as script

context = ssl._create_unverified_context()


# Establishes an HTTP connection and returns a soup object of a page's HTML
def make_soup(url):

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req, context=context).read()
    page_html = web_byte.decode('utf-8')

    return BeautifulSoup(page_html, "html.parser")

# Takes a list of dictionaries to format into .csv file
# Must change names of columns and dictionary keywords depending on categories


def writeToCSV(pathname, items):
    with open(pathname, 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["FIRM", "INSIDER RATING", "INDUSTRY REPUTATION", "LIKED PERCENTAGE", "WEBSITE", "NEWS"])

        for item in items:
            writer.writerow([item['firm name'], item['insider rating'], item["industry reputation"],
                             item["liked percentage"], item['website'], item['news']])

def main():
    # result = script.driver()
    # file = "/Users/brendanlamishaw/Desktop/firms.csv"
    # writeToCSV(file, result)
    s = list('The final answer to the story, lies among the truths we\'ve been told')
    reverseString(s)
    print(''.join(s))

def reverseString(s):
    size = len(s)
    i = 0
    j = -1

    while size > 2:
        s[i], s[j] = s[j], s[i]
        i += 1
        j -= 1
        size -= 2







if __name__ == '__main__':
    main()

