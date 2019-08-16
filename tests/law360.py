from tests.main import *

# def import_firms(file):
#     firms = []
#
#     with open(file) as firm_file:
#         readCSV = csv.reader(firm_file, delimiter= ',')
#         for i, row in enumerate(readCSV):
#             if i > 0:
#                 firm = row[0].replace(" ", "%20").replace("'", "%27").replace(",", "")
#                 firms.append(firm)
#
#     return firms

def format_name(firm_name):
    return firm_name.replace(" ", "%20").replace("\u2019", "%27").replace(",", "").replace(".", "")



def click_link(firm_name):

    news = []

    soup = make_soup(f'https://www.law360.com/search?q={firm_name}')
    hits = soup.find_all("li", class_="result")



    for item in hits:
        try:
            summary = item.p.get_text().replace('\n', " ").replace('\r', "")
        except:
            summary = "NULL"

        try:
            title= item.a.get_text()
        except:
            title = "NULL"

        article = {
            'title': title,
            'summary': summary

        }
        news.append(article)

    return news
