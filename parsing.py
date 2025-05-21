from bs4 import BeautifulSoup

class Parser:

    def __init__(self, filename, parser_library="html.parser"):
        with open(filename) as file:
            self.soup = BeautifulSoup(file, parser_library)
