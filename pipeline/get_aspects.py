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


def displayInfo(link, load, result_desc, result_cats, new_links):
    """
    Print formatted information about a related page and its parent page.

    This function displays the title of the related page, the parent page title,
    its description, and its categories in a readable format.

    Args:
        link (dict): A dict with keys 'title' and 'link' of the related page.
        load (dict): The parent page record containing at least 'title'.
        result_desc (str): The description text for the related page.
        result_cats (list[str]): List of category names for the related page.
        new_links (list[dict]): Current list of processed related pages.
    """
    print(f"{link['title']}")
    print(f"\tHoofdpagina: {load['title']}")
    if result_desc == "No description":
        print(f"\tBeschrijving: Geen beschrijving")
    else:
        print(f"\tBeschrijving: {result_desc}")
    if result_cats == []:
        print(f"\tCategorieën: Geen categorie")
    else:
        print(f"\tCategorieën: {', '.join(result_cats)}\n")


def getDescription(page):
    """
    Retrieve the Dutch description from Wikidata for a given Wikipedia page link.

    This function queries the Wikipedia API for page properties to find the
    Wikibase item ID, then retrieves the nl-language description from the
    Wikidata API. If no description is available, returns 'No description'.

    Args:
        page (dict): A dict with keys 'title' and 'link' representing a related page.

    Returns:
        str: The Dutch description text, or 'No description' if none is found.
    """
    title = page["title"]
    links = page["link"]

    URL_NL = 'https://nl.wikipedia.org/w/api.php'
    PARAMS_NL = {
    "action": "query",
    "titles": title,
    "format": "json",
    "prop": "pageprops"
    }

    s = requests.Session()
    r = s.get(url=URL_NL, params=PARAMS_NL)
    data = r.json()
    page = next(iter(data['query']['pages'].values()))
    if "pageprops" in page:
        if "wikibase_item" in page['pageprops']:
            id = page['pageprops']['wikibase_item']

            wikidata_url = "https://www.wikidata.org/w/api.php"
            params = {
            "action": "wbgetentities",
            "format": "json",
            "ids": id,
            "props": "descriptions",
            "languages": "nl"
            }

            response = requests.get(wikidata_url, params=params).json()
            description = response['entities'][id]['descriptions']

            if "nl" in description:
                desc = description["nl"]["value"]
                return desc
            else:
                return "No description"
    else:
        return "No description"


def getCategory(page):
    """
    Fetch all non-Wikipedia/Wikimedia categories for a given Wikipedia page.

    This function queries the Wikipedia API for page categories, filters out
    any categories starting with 'Categorie:Wikipedia' or 'Categorie:Wikimedia',
    and returns the remaining category titles without the 'Categorie:' prefix.

    Args:
        page (dict): A dict with keys 'title' and 'link' representing a related page.

    Returns:
        list[str]: A list of category names, or an empty list if none are found.
    """
    title = page["title"]
    links = page["link"]

    URL_NL = 'https://nl.wikipedia.org/w/api.php'
    PARAMS_NL = {
    "action": "query",
    "titles": title,
    "format": "json",
    "prop": "categories"
    }
    s = requests.Session()
    r = s.get(url=URL_NL, params=PARAMS_NL)
    data = r.json()
    page = next(iter(data['query']['pages'].values()))
    cats = []
    if "categories" in page:
        for item in page["categories"]:
            if not item["title"].startswith("Categorie:Wikipedia") or item["title"].startswith("Categorie:Wikimedia"):
                cats.append(item["title"].replace('Categorie:', ''))
        return cats
    else:
        return []


def getRelatedPageViewCount(title, days):
    """
    Sum the page views for a Wikipedia page over a given number of days.

    This function queries the Wikipedia API for the pageviews property and
    returns the total views over the past 'days' days. If data is missing,
    returns 0.

    Args:
        title (str): The title of the Wikipedia page.
        days (int): Number of past days to include in the view count.

    Returns:
        int: Total pageview count over the specified period, or 0 on error.
    """
    URL_NL = 'https://nl.wikipedia.org/w/api.php'
    PARAMS_NL = {
    "action": "query",
    "titles": title,
    "format": "json",
    "prop": "pageviews",
    "pvipdays": days
    }

    s = requests.Session()
    r = s.get(url=URL_NL, params=PARAMS_NL)
    data = r.json()
    try:
        response = next(iter(data['query']['pages'].values()))
        total_count = 0
        j = 0
        for item in response["pageviews"]:
            count = response["pageviews"][item]
            j += 1
            if count is not None:
                total_count = total_count + count
        return total_count
    except KeyError:
        return 0


def getInfo(data):
    """
    Process a list of pages, retrieving descriptions, categories, and view counts
    for each linked page, and assemble the enriched data.

    For each page in data (stringified dict with 'title' and 'links'), this function:
      - Evaluates the string to a dict record
      - For each related link, fetches its description, categories, and 30-day view count
      - Includes only links with both a description and at least one category
      - Appends the processed links to the parent page record

    Args:
        data (list[str]): List of stringified dicts, each containing 'title' and 'links'.

    Returns:
        list[dict]: List of dicts with keys 'title' and 'links', where 'links' is a list
                    of dicts with 'title', 'link', 'description', 'categories', and 'count'.
    """
    i = 0
    full_pages = []
    for page in data:
        load = ast.literal_eval(page)
        # get information for each related page
        new_links = []
        for link in load["links"]:
            result_desc = getDescription(link) # retreive central description
            result_cats = getCategory(link) # retreive all categories
            if result_desc != "No description" and result_cats != []:
                count = getRelatedPageViewCount(link["title"], 30) # retreive page view count
                new_row = {"title": link["title"], "link": link["link"], "description": result_desc, "categories": result_cats, "count": count}
                new_links.append(new_row)                
                # display retreived info
                #displayInfo(link, load, result_desc, result_cats, new_links)

        full_pages.append({"title": load["title"], "links": new_links})
        # update and display progress
        i += 1
        print(f"{i}/{len(data)} ({(i / len(data)) * 100})")

    return full_pages


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
    infile = "data/all_filtered1.txt"
    outfile = 'data/all_aspects.txt'

    # get data from file
    data = getData(infile)

    # get description and category for each related page for each main page
    info = getInfo(data)

    # write data to file
    writeData(outfile, info)

if __name__ == "__main__":
    main()
