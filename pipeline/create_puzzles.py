#!/usr/bin/python3

import requests
import ast
import json
import os
import random
from dotenv import load_dotenv
from itertools import permutations


def getData(file):
    """
    Read lines from a file and return them as a list of strings.

    Args:
        file: Path to the input file.

    Returns:
        A list of strings, each representing a line from the file.
    """
    with open(file, "r") as f:
        return f.readlines()

def writeData(file, data):
    """
    Write each item in a list to a new line in a file.

    Args:
        file: Path to the output file.
        data: List of items to write (will be stringified).
    """
    with open(file, 'w') as f:
        for line in data:
            f.write(f"{json.dumps(line)}\n")

def combineClues(clue1, clue2, clue3):
    """
    Combines three textual clues into a single formatted Dutch puzzle sentence.

    Args:
        clue1 (str): The first clue.
        clue2 (str): The second clue.
        clue3 (str): The third clue.

    Returns:
        str: A sentence combining the three clues in a specific format.
    """
    return f"Het is {clue1[0].lower() + clue1[1:].strip()}, {clue2[0].lower() + clue2[1:].strip()}, en {clue3[0].lower() + clue3[1:].strip()}"


def writePuzzle(data):
    """
    Generates puzzle prompts using the default clue order for each item in the input data.

    Args:
        data (list of str): Raw input data where each string is a dictionary containing 'clue1', 'clue2', 'clue3', and 'answer'.

    Returns:
        list of dict: Each dictionary contains 'puzzle' (the prompt) and 'answer' (the solution).
    """
    puzzles = []
    for page in data:
        load = ast.literal_eval(page)
        clues = (load["clue1"], load["clue2"], load["clue3"])
        answer = load["answer"]
        prompt = combineClues(*clues)
        puzzles.append({"puzzle": prompt, "answer": answer})
    return puzzles


def generatePermutations(data):
    """
    Generates all 6 possible permutations of the three clues for each puzzle in the input data.

    Args:
        data (list of str): Raw input data where each string is a dictionary containing 'clue1', 'clue2', 'clue3', and 'answer'.

    Returns:
        list of list of dict: A list of 6 lists, each containing puzzles with a different permutation of clues.
    """
    permuted_sets = [[] for _ in range(6)]
    for page in data:
        load = ast.literal_eval(page)
        clues = (load["clue1"], load["clue2"], load["clue3"])
        answer = load["answer"]
        perms = list(permutations(clues))
        for i in range(6):
            prompt = combineClues(*perms[i])
            permuted_sets[i].append({"puzzle": prompt, "answer": answer})
    return permuted_sets


def splitData(data, test_ratio=0.9):
    """
    Randomly splits the raw input data into a test set and a development set.

    Args:
        data (list of str): The full dataset, where each item is a stringified dictionary.
        test_ratio (float): The proportion of data to include in the test set. Default is 0.9 (90%).

    Returns:
        tuple: Two lists (test_data, dev_data) containing the split data.
    """
    random.shuffle(data)
    split_index = int(len(data) * test_ratio)
    return data[:split_index], data[split_index:]


def main():

    # define input
    infile = "data/all_annotations_in.txt"

    # get data from file
    data = getData(infile)

    # split data into test and dev with ratio
    test_data, dev_data = splitData(data, test_ratio=0.9)

    # create puzzles
    writeData("data/test_puzzles.txt", writePuzzle(test_data))
    writeData("data/dev_puzzles.txt", writePuzzle(dev_data))

    # create permutations
    test_perms = generatePermutations(test_data)
    dev_perms = generatePermutations(dev_data)

    for i in range(6):
        writeData(f"data/test_puzzles_{i+1}.txt", test_perms[i])
        writeData(f"data/dev_puzzles_{i+1}.txt", dev_perms[i])

if __name__ == "__main__":
    main()
