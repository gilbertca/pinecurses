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
		self.FUNCTIONS.update({'x' : lambda:0}) # Ends program

	@log
	def handle_styles(self, *args):
		"""handle_styles adds class specific functionality to BaseObject's handle_styles.
		"""
		style_namespace = {}
		super().handle_styles(style_namespace)
