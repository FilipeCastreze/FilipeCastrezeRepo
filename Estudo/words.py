"""
Retrieve and print words from URL.

Usage:
    py words.py <URL>
"""

import sys
from urllib.request import urlopen

#"http://sixty-north.com/c/t.txt"

def fetch_words(url):
    """
    Fetch a list of words from URL.

    Args:
        url: The URL of a UTF-8 text document.

    Returns:
        A list of strings containing the words from
        the document
    """
    story = urlopen(url)
    story_words = []

    for line in story:
        line_words = line.decode('utf-8').split()
        for word in line_words:
            story_words.append(word)

    story.close()
    return story_words


def print_items(items):
    """
    Prints the item one per line

    Args:
        An interable series of printable items

    """
    for item in items:    
        print (item)


def main(url):
    words = fetch_words(url)
    print_items(words)


if __name__ == '__main__':
    main(sys.argv[1]) #The 0th arg is the module filename.