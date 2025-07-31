#!/usr/bin/python3

import requests
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


def getDisambiguation():
    """
    Retrieve all Dutch Wikipedia disambiguation pages in the specified category.

    Returns:
        A list of page dictionaries as returned by the API.
    """
    URL_NL = 'https://nl.wikipedia.org/w/api.php'
    PARAMS_NL = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Categorie:Wikipedia:Doorverwijspagina",
        "cmlimit": 500
    }

    i = 0
    all_pages = []
    cmcontinue = None
    while True:
        if cmcontinue:
            PARAMS_NL["cmcontinue"] = cmcontinue
        else:
            PARAMS_NL.pop("cmcontinue", None)
        
        R = requests.get(url=URL_NL, params=PARAMS_NL)
        data = R.json()

        if "query" in data:
            all_pages.extend(data["query"]["categorymembers"])
        cmcontinue = data.get("continue", {}).get("cmcontinue")

        if not cmcontinue:
            break
    return all_pages


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
    infile = None
    outfile = 'data/all_pages.txt'

    # get all Dutch Wikipedia disambiguation pages
    pages = getDisambiguation()
    print(f"Total pages retrieved: {len(pages)}")

    # write data to file
    writeData(outfile, pages)

if __name__ == "__main__":
    main()
