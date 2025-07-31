#!/usr/bin/python3

import requests
import ast
from bs4 import BeautifulSoup


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


def getInfo(data):
    """
    Extract valid internal Wikipedia links from page HTML content.

    Args:
        data: List of stringified dict records. Each record must contain
              the keys 'pageid', 'title', and 'text' (HTML content).

    Returns:
        list: A list of dicts, each with:
              - 'title': Title of the page.
              - 'links': List of dicts with 'title' and 'link' for each found link.
    """
    final_list = []
    for txt in data:
        load = ast.literal_eval(txt)
        page_id = load["pageid"]
        text = load["text"]
        identifiers = ("/wiki/Bestand", "/wiki/Speciaal", "/wiki/Wikipedia", "/wiki/Wikimedia")

        soup = BeautifulSoup(text, 'lxml')
        a_elements = soup.find_all('a')

        finals = []
        for item in a_elements:
            info = item.attrs
            if "href" in info: 
                if info["href"].startswith("/wiki") and not info["href"].startswith(identifiers):
                    link = info["href"]
                    title = info["title"]
                    finals.append({"title": title, "link": link})

        title = load["title"]
        if finals != []:
            final_list.append({"title": title, "links": finals})
    return final_list


def main():

    # define in- and output
    infile = "data/all_contents.txt"
    outfile = 'data/all_links.txt'

    # get data from file
    data = getData(infile)

    # get title and link of related pages from main page content
    info = getInfo(data)

    # write data to file
    writeData(outfile, info)

if __name__ == "__main__":
    main()
