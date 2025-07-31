#!/usr/bin/python3

import requests
import ast
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


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


def filterRelatedPagesCount(data):
    """
    Filter pages that have at least a minimum number of related links.

    Args:
        data (list): List of stringified dicts, each containing a "links" key
                     which is a list of related link dicts.

    Returns:
        list: A list of dicts with keys "title" and "links" for pages
              where the number of links is >= 3.
    """
    filtered = []
    for page in data:
        load = ast.literal_eval(page)
        links = load["links"]
        page_count = len(links)
        if page_count >= 3:
            row = {"title": load["title"], "links": load["links"]}
            filtered.append(row)
    return filtered


def filterODWNAppearance(data, file):
    """
    Retain only pages whose titles appear in the Open Dutch WordNet.

    This function loads an ODWNet XML file, extracts all lemma "writtenForm"
    values, and filters 'data' (a list of page dicts) to those whose titles
    match a lemma in the wordnet (case-insensitive).

    Args:
        data (list): List of dicts, each containing a "title" key.
        file (str): Path to the Open Dutch WordNet XML file.

    Returns:
        list: Subset of 'data' where page titles appear in the wordnet.
    """
    # open Open Dutch WordNet XML file and get all Lemma elements
    with open(file, 'r') as f:
        text = f.read()
    soup = BeautifulSoup(text, "xml")
    elements = soup.find_all('Lemma')

    # get value from attribute writtenForm from all Lemma tags
    all_words = []
    for item in elements:
        info = item.attrs
        if "writtenForm" in info:      
            word = info["writtenForm"]
            all_words.append(word.lower())
    
    # only save unique words
    all_words = list(set(all_words))

    # filter all filtered pages on appearance within Open Dutch WordNet
    filtered = []
    for page in data:
        title = page["title"]
        if title.lower() in all_words:
            filtered.append(page)
    return filtered


def filterMainPageTitleLenght(data, length):
    """
    Filter pages whose titles meet a minimum length requirement.

    Args:
        data (list): List of dicts, each containing a "title" key.
        length (int): Minimum number of characters required in the title.

    Returns:
        list: List of dicts from 'data' where title length >= 'length'.
    """
    filtered = []
    for page in data:
        title = page["title"]
        if len(title) >= length:
            filtered.append(page)
    return filtered


def main():

    # define API credentials
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not username or not password:
        raise EnvironmentError("USERNAME and PASSWORD must be set in .env file")

    # define in- and output
    infile = 'data/all_links.txt'
    outfile = 'data/all_filtered1.txt'

    # start session
    startSession(username, password)

    # get data from file
    data = getData(infile)

    # filter by related page count
    filtered = filterRelatedPagesCount(data)

    print(filtered)

    # filter by Open Dutch WordNet appearance
    wordnet_file = 'dependencies/odwn-lemmas-unique.xml'
    filtered = filterODWNAppearance(filtered, wordnet_file)
    print(filtered)

    #filter by main page title lenght
    filtered = filterMainPageTitleLenght(filtered, 4)
    print(filtered)

    # write data to file
    writeData(outfile, filtered)

if __name__ == "__main__":
    main()
