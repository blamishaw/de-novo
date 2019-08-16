""" A file for helper functions used throughout the program """

import json

def remove_multiple(name, toBeReplaced):
    """ Takes a name, List[chars to be removed]
        :rtype string with removed characters """

    for elem in toBeReplaced:
        name = name.replace(elem, '')
    return name

def remove_after_parens(name):
    """ Removes all characters after the first parens character is encountered
        :rtype string
    """

    parens_start = name.find('(')
    if parens_start == -1:
        return name
    return name[:parens_start-1]


def convert_to_json(filename, scrape_data):
    """ Appends a dictionary returned from a scraper to a JSON file for processing by the database"""

    try:
        data = load_from_json(filename)
    except json.JSONDecodeError:
        data = []
    data.append(scrape_data)

    with open(filename, 'w') as file:
        json.dump(data, file)
        file.close()


def load_from_json(filename):
    """ Loads the data stored in a JSON file
        :rtype dict
    """

    with open(filename, 'r') as file:
        data = json.load(file)
        file.close()
    return data
