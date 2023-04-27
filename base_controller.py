import curses
import logging
from pycurses_object import PycursesObject
from base_view import BaseView
from utils import log


class BaseController(PycursesObject):
	"""
	The base controller class which  controls all other aspects of a Pycurses program.
	"""
	def __init__(self, stdscr, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		self.stdscr = stdscr

	def create_view(self, **attributes):
		"""
		Since Views are to be ignorant of curses,
			their window object must be created by
			their parent Controller instance.
		"""
		# Instantiate instance of a view:
		view_instance = BaseView(self, **attributes)
		# Update self's dictionary as {name : instance}:
		self.update({view_instance.attributes('name') : view_instance})
