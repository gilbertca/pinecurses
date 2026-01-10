from dataclasses import dataclass

from bs4 import BeautifulSoup

@dataclass
class Parser:
    filename: str
    parser_library: str = "html.parser"

    def extract_all_tags_from_file(self):
        """Extracts **ALL** tags which are understood by Pinecurses."""
        with open(filename, 'r') as file:
            soup = Beautifulsoup(file, 'lxml')

        # Extract ALL tags we want:
        all_tags = {}

        # Finish by decomposing and returning the tags
        soup.decompose()
        return all_tags
