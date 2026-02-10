"""**pinecurses** contains the primary class: PinecursesApp.

A hypothetical user simply needs to:
    1. Create an html template that defines their app's structure
    2. Create a namespace that links the names and classes
    from their template file to their custom data and functions
    3. Instantiate a PinecursesApp with the template directory and namespace
    4. Call the `run` function, and let Pinecurses do the heavy-lifting
"""
import curses
from dataclasses import dataclass

from src.parsing import PinecursesParser
from src.templating import PinecursesTemplater

class PinecursesApp:
    def __init__(
        self,
        root_template_name,
        function_namespace,
        template_directory="templates",
    ):
        self.root_template_name = root_template_name # First rendered template
        self.function_namespace = function_namespace # For dynamic text
        self.pinecurses_templater = ( # jinja2 templating
            PinecursesTemplater(template_directory) 
        )
        self.pincurses_parser = ( # bs4 parsing
            PinecursesParser(function_namespace)
        )
        self.RUNNING = False # Application status

    def run(self):
        # Expand the root template:
        expanded_template = (
            self.pinecurses_templater
            .expand_pinecurses_template(self.template_root_file)
        )

        # Parse tags from root template:
        self.tags = parse_pinecurses_config(expanded_template)

        # Enter the main loop:
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        # Initial setup
        self.RUNNING = True

        # Main loop
        while self.RUNNING:
            pass
