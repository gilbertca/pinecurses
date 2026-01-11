import curses
from dataclasses import dataclass

from parsing import parse_pinecurses_config

@dataclass
class PinecursesApp:
    filename: str
    function_namespace: dict
    RUNNING: bool = False

    def run(self):
        # Parse all the tags:
        self.tags = parse_pinecurses_config(self.filename)

        # Enter the main loop:
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        # Initial setup
        self.RUNNING = True

        # Main loop
        while self.RUNNING:
            pass
