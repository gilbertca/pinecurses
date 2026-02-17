"""**parsing** contains the logic for converting an expanded template
into objects and data usable by **curses**
(see the **templating** module for details on expanding templates)."""
import xml.etree.ElementTree as ET

class PinecursesParser:
    def __init__(self, parser_options):
        self.parser_options = parser_options

    def parse_pinecurses_config(self, expanded_template):
        """Accepts an expanded template
        and pulls all Pinecurses tags from it."""
        tags = {}
        # Extract important tags, convert to curses equivalents
        return tags
