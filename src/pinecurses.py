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

from src.parsing import parse_pinecurses_config
from src.templating import expand_pinecurses_template

@dataclass
class PinecursesApp:
    template_root_file: str
    template_dir: str
    function_namespace: dict
    RUNNING: bool = False

    def run(self):
        # Expand the root template:
        expanded_template = expand_pinecurses_template

        # Parse tags from root template:
        self.tags = parse_pinecurses_config(expanded)

        # Enter the main loop:
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        # Initial setup
        self.RUNNING = True

        # Main loop
        while self.RUNNING:
            pass
