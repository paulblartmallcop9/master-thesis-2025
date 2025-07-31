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


def filterRelatedPagesCount(data):
    """
    Filters pages that have at least 3 related links.

    Args:
        data (list): List of pages as stringified dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered list of dictionaries with 'title' and 'links' keys.
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


def filterRelatedPagesCountParsed(data):
    """
    Filters pages that have at least 3 related links (expects pre-parsed dictionaries).

    Args:
        data (list): List of dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered list of dictionaries with 'title' and 'links' keys.
    """
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        page_count = len(links)
        if page_count >= 3:
            row = {"title": load["title"], "links": load["links"]}
            filtered.append(row)
    return filtered


def filterRelatedPagesDescriptionExact(data):
    """
    Removes links from each page that match exactly with predefined non-informative descriptions.

    Args:
        data (list): List of page dictionaries containing 'title' and 'links'.

    Returns:
        list: Updated list with filtered links.
    """
    exact = [
        None,
        "Wikimedia-lijst",
        "gemeenschappelijk project om een \u200b\u200bmeertalig woordenboek te maken",
        "Wikimedia-doorverwijspagina",
        "algemeen",
        "Nederland",
        "jaar",
        "rivier",
        "gemeente",
        "nummer",
        "stad",
        "regio",
        "provincie",
        "historisch land",
        "streek",
        "gebied",
        "taxon",
        "kalenderjaar",
        "decennium",
        "Londen"
    ]
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        new_links = []
        for link in links:
            aspect = link["description"]
            if all(word != aspect for word in exact):
                new_links.append(link)
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def filterRelatedPagesDescriptionPartial(data):
    """
    Removes links whose descriptions partially match predefined patterns.

    Args:
        data (list): List of page dictionaries containing 'title' and 'links'.

    Returns:
        list: Updated list with filtered links.
    """
    part = [
        "soort uit ",
        "buurtschap ",
        "gemeente ",
        "schip uit ",
        "geslacht uit ",
        "familie uit ",
        "stad in ",
        "provincie van ",
        "provincie in ",
        "plein in ",
        "boek van ",
        "eiland van ",
        "straat in ",
        "geslacht van ",
        "plaats in ",
        "gebouw in ",
        "stadsdeel in ",
        "land in ",
        "park in ",
        "hoofdstad van ",
        "museum in ",
        "familie van ",
        "orde van ",
        "deelstaat van ",
        "district van ",
        "wijk in ",
        "regio in ",
        "buurt in ",
        "regio van ",
        "SI-prefix ",
        "kanaal in ",
        "streek in ",
        "departement in ",
        "staat in ",
        "haven in ",
        "gebied in ",
        "meer in ",
        "rivier in ",
        "staat van ",
        "gebied van ",
        "woonbuurt in ",
        "metrolijn in ",
        "heuvel in ",
        "windmolen in ",
        "bouwwerk in ",
        "politieke partij uit ",
        "wijk van ",
        "beek in ",
        "dierentuin in ",
        "politieke partij in ",
        "taal.",
        "familienaam"
    ]
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        new_links = []
        for link in links:
            aspect = link["description"] + "."
            if all(word not in aspect.lower() for word in part):
                new_links.append(link)  
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def filterPersonRelevanceCountryDemonym(data, threshold):
    """
    Keeps links with a demonym mention if their count is above a threshold.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.
        threshold (int): Minimum relevance count to retain a link.

    Returns:
        list: Filtered data with links related to nationalities if relevant.
    """
    list = [
        "nederlands",
        "belgisch",
        "duits",
        "amerikaans",
        "portugees",
        "indiaas",
        "brits",
        "spaans",
        "frans",
        "turks",
        "mexicaans",
        "vlaams",
        "italiaans",
        "deens",
        "zweeds",
        "hongaars",
        "engels",
        "fries",
        "zuid-afrikaans",
        "braziliaans",
        "canadees",
        "iraans",
        "oostenrijks",
        "luxemburgs",
        "surinaams",
        "russisch",
        "iers",
        "zwitsers",
        "romeins",
        "portuges",
        "surinaams",
        "ivoriaans",
        "kazachstaans"
    ]
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        new_links = []
        for link in links:
            aspect = link["description"]
            aspect_low = aspect.lower()
            if any(word in aspect_low for word in list):
                count = link["count"]
                if count >= threshold:
                    new_links.append(link)
            else:
                new_links.append(link)      
        filtered.append({"title": load["title"], "links": new_links})
    return filtered
    
def filterPersonRelevanceCountryName(data, threshold):
    """
    Filters links based on whether a country name is mentioned in a specific format.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.
        threshold (int): Relevance threshold for inclusion.

    Returns:
        list: Filtered list of dictionaries.
    """
    countries_file = "dependencies/dutch_country_names.txt"
    f = open(countries_file, "r")
    countries = f.read().splitlines()
    
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        new_links = []
        for link in links:
            aspect = link["description"]
            aspect_split = aspect.split()
            if len(aspect_split) >= 3:
                if aspect_split[1] == "uit" and aspect_split[2] in countries and len(aspect_split) >= 3 and "(" in aspect and ")" in aspect:
                    count = link["count"]
                    if count >= threshold:
                        new_links.append(link)
                else:
                    if aspect_split[1] == "uit" and aspect_split[2] in countries and len(aspect_split) >= 3:
                        count = link["count"]
                        if count >= 350:
                            new_links.append(link)
                    else:
                        new_links.append(link)
            else:
                new_links.append(link)      
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def filterRelatedPagesNoNumber(data):
    """
    Removes links where the description consists only of digits.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered list with non-numeric links.
    """
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        new_links = []
        for link in links:
            aspect = link["description"]
            aspect = aspect.replace("-", "")
            if str(aspect).isdigit() != True:
                new_links.append(link)
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def filterRelatedPageCategory(data):
    """
    Filters out links belonging to certain undesired Wikipedia categories.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered pages excluding specified categories.
    """
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        excluded = [
            "Muziekalbum ",
            "Film ",
            "Plaats ",
            "Gemeente ",
            "County ",
            "Wijk ",
            "Parochie "
        ]
        present = 0
        new_links = []
        for link in links:
            categories = link["categories"]
            for exclude in excluded:
                for category in categories:
                    if exclude.lower() in category.lower():
                        present = 1
            if present != 1:
                new_links.append(link)
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def sortRelatedPages(data):
    """
    Sorts links for each page in descending order by 'count'.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.

    Returns:
        list: Sorted pages with an added index number.
    """
    filtered = []
    i = 1
    for page in data:
        load = page
        links = load["links"]
        top_links = sorted(links, key=lambda d: d['count'], reverse=True)
        filtered.append({"number": i, "title": load["title"], "links": top_links})
        i += 1
    return filtered


def filterSimilarAspects(data):
    """
    Removes duplicate descriptions from the same page's links (case-insensitive).

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered list without duplicated aspect descriptions.
    """
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        aspects = []
        compare = []
        for link in links:
            aspect = link["description"]
            aspects.append(aspect)
            compare.append(aspect)
        new_links = []
        i = 0
        for aspect in aspects:
            present = 0
            for comp in compare:
                if aspect.lower() == comp.lower():
                    present += 1
            if present == 1:
                new_links.append(links[i])
            compare[i] = ""
            i += 1
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


def filterAnswerInQuestion(data):
    """
    Removes links that contain the answer (page title) in their description.

    Args:
        data (list): List of page dictionaries with 'title' and 'links'.

    Returns:
        list: Filtered list where answer is not part of any link description.
    """
    filtered = []
    for page in data:
        load = page
        links = load["links"]
        answer = load["title"]
        new_links = []
        for link in links:
            aspect = link["description"]
            if answer.lower() not in aspect.lower():
                new_links.append(link)
        filtered.append({"title": load["title"], "links": new_links})
    return filtered


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
    infile = "data/all_aspects.txt"
    outfile = 'data/all_filtered2.txt'

    # get data from file
    data = getData(infile)

    # filter by related page count
    filtered = filterRelatedPagesCount(data)

    # filter related pages by description exact
    filtered = filterRelatedPagesDescriptionExact(filtered)

    # filter related pages by description not being a number
    filtered = filterRelatedPagesNoNumber(filtered)

    # filter related pages by aspect category
    filtered = filterRelatedPageCategory(filtered)

    # filter by answer in question
    filtered = filterAnswerInQuestion(filtered)

    # filter by similar aspects
    filtered = filterSimilarAspects(filtered)

    # filter by person relevance based on country demonym
    filtered = filterPersonRelevanceCountryDemonym(filtered, 3000)

    # filter by person relevance based on country name
    filtered = filterPersonRelevanceCountryName(filtered, 3000)

    # filter related pages by description partially
    filtered = filterRelatedPagesDescriptionPartial(filtered)

    # filter by related page count
    filtered = filterRelatedPagesCountParsed(filtered)

    # sort related pages by page view count
    filtered = sortRelatedPages(filtered)

    # write data to file
    writeData(outfile, filtered)

if __name__ == "__main__":
    main()
