import sys

from tests.law360 import *

# This is a script to scrape abovethelaw.com

main_url = 'https://abovethelaw.com/careers/law-firms/'

def iterateDropDownLinks(soup):
    firms = []

    links = soup.find_all("option", value=(lambda href: href and not ""))
    bar = "#"

    for num, i in enumerate(links):
        firm_page_soup = make_soup(i['value'])
        firm_name = i.get_text()
        firms.append(parsePage(firm_name, firm_page_soup))
        sys.stdout.write('\r' + f"{round(num/len(links) * 100, 2)}% " + f"{bar}")
        if num % 4 == 0:
            bar = bar + "#"
    return firms


def parsePage(firm_name, soup):

    news = click_link(format_name(firm_name))

    insider_rating = ""
    industry_reputation = ""

    for i in soup.find_all('dl', class_='grade blow-up'):
        if insider_rating == "":
            insider_rating = i.strong.get_text()
        else:
            industry_reputation = i.strong.get_text()
    try:
        liked = soup.find('dl', class_='grade questionnaire').strong.get_text()
    except:
        liked = "Insufficient Data"

    try:
        firm_link = soup.find('ul', class_='social social-basic inline-list').li.a['href']
    except:
        firm_link = "No Link"

    firm = {
        "firm name": firm_name,
        "insider rating": insider_rating,
        "industry reputation": industry_reputation,
        "liked percentage": liked,
        "website": firm_link,
        "news": news
    }

    return firm


def driver():
    return iterateDropDownLinks(make_soup(main_url))



