"""**parsing** contains the logic for converting an expanded template
into objects and data usable by **curses**
(see the **templating** module for details on expanding templates)."""
from bs4 import BeautifulSoup

def parse_pinecurses_config(filename):
    with open(filename) as file:
        soup = BeautifulSoup(file, "html.parser")

    tags = {}
    # Extract important tags, convert to curses equivalents


    return tags
