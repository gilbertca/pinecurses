from bs4 import BeautifulSoup

def parse_pinecurses_config(filename):
    with open(filename) as file:
        soup = BeautifulSoup(file, "html.parser")

    tags = {}
    # Extract important tags from the soup:


    return tags
