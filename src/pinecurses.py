import curses
from dataclasses import dataclass

from parsing import Parser

@dataclass
class PinecursesApp:
    filename: str
    function_namespace: dict

    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        stdscr.addstr("Hello bitch")
        stdscr.getch()

