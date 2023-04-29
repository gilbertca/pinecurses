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

	@log
	def begin(self):
		"""
		The main loop of any pycurses program. Once this function returns anything,
			then the program will end.
		"""
		self.initialize_views()

		# End program:
		return 0

	@log
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
	
	@log
	def initialize_views(self):
		"""
		Iterates through self's dictionary and calls 'initialize' on all views.
		"""
		for view_name in self:
			self.get(view_name).initialize()

	@log
	def draw_all_views(self):
		"""
		Draws all views within self's dictionary.
		"""
		pass

	@log
	def draw_view(self, view_instance):
		"""
		Draws a particular view from a View instance.
		"""
		pass
