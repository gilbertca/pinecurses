import curses
import logging
from pycurses_object import PycursesObject
from utils import log


class BaseController(PycursesObject):
	"""
	The base controller class which  controls all other aspects of a Pycurses program.
	"""
	def __init__(self, stdscr, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.stdscr = stdscr
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
