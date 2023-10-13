import curses
from baseobject import BaseObject
from mixins.cursormixins import SingleObjectCursor
from logger import log

class Trunk(SingleObjectCursor, BaseObject):
	"""A Trunk is considered the Base of a Pinecurses program, and is typically created by a Pinecurses object. After creation, running `trunk_instance.begin(..)` will begin the program.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.CURSES_COLOR_MAP = {
			'black' : curses.COLOR_BLACK,
			'red' : curses.COLOR_RED,
			'green' : curses.COLOR_GREEN,
			'yellow' : curses.COLOR_YELLOW,
			'blue' : curses.COLOR_BLUE,
			'magenta' : curses.COLOR_MAGENTA,
			'cyan' : curses.COLOR_CYAN,
			'white' : curses.COLOR_WHITE,
		}
		self.colors = {}
		self.DEFAULT_BACKGROUND_COLOR = self.CURSES_COLOR_MAP.get('black')
		self.FUNCTIONS.update({'x' : lambda:0})

	@log
	def begin(self, stdscr):
		"""The main loop of any pinecurses program. Once this function returns anything, then the program will end.
		"""
		self.window = stdscr
		# Once self.interact(..) returns a value, program will end.
		while True:
			# Get the keypress from a child window:
			keypress = self.get_selected_window().getch()
			if self.interact(keypress) == 0:
				return 0

