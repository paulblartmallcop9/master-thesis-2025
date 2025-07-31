#!/usr/bin/python3

import requests
import ast
import json
import os
from dotenv import load_dotenv


def startSession(username, password):
    """
    Log in to the MediaWiki API using a session.

    Args:
        username: Wiki username.
        password: Wiki password.

    Raises:
        AssertionError: If login does not succeed.
    """
    s = requests.Session()
    url = "https://www.mediawiki.org/w/api.php"
    params_token = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }
    r = s.get(url=url, params=params_token)
    data = r.json()
    login_token = data['query']['tokens']['logintoken']
    params_login = {
        'action': "login",
        'lgname': username,
        'lgpassword': password,
        'lgtoken': login_token,
        'format': "json"
    }
    r = s.post(url, data=params_login)
    data = r.json()


def getData(file):
    """
    Read lines from a file and return them as a list of strings.

    Args:
        file: Path to the input file.

    Returns:
        A list of strings, each representing a line from the file.
    """
    f = open(file, "r")
    pages = f.readlines()
    return pages


def writeData(file, data):
    """
    Write each item in a list to a new line in a file.

    Args:
        file: Path to the output file.
        data: List of items to write (will be stringified).
    """
    with open(file, 'w') as f:
        for line in data:
            f.write(f"{line}\n")


def getContent(data):
    """
    Fetch and parse the full HTML content of each Wikipedia page in data.

    Args:
        data: List of page records as dictionaries (with keys 'pageid' and 'title').

    Returns:
        A list of dictionaries, each containing:
            'pageid': The page ID.
            'title': The page title.
            'text': The raw HTML content of the page.
    """
    s = requests.Session()
    URL_NL = 'https://nl.wikipedia.org/w/api.php'
    i = 0
    full_list = []
    for page in data:
        load = ast.literal_eval(page)
        page_id = load["pageid"]
        title = load["title"]
        
        PARAMS_NL = {
        "action": "parse",
        "page": title,
        "format": "json"
        }
        
        r = s.get(url=URL_NL, params=PARAMS_NL)
        data = r.json()
        text = data["parse"]["text"]["*"]
        
        full_list.append({"pageid": page_id, "title": title, "text": text})

    return full_list


def main():

    # define API credentials
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    if not username or not password:
        raise EnvironmentError("USERNAME and PASSWORD must be set in .env file")

    # start session
    startSession(username, password)

    # define in- and output
    infile = "data/all_pages.txt"
    outfile = 'data/all_contents.txt'

    # get data from file
    data = getData(infile)

    # get contents (HTML) from Wikipedia pages
    content = getContent(data)

    # write data to file
    writeData(outfile, content)

if __name__ == "__main__":
    main()
