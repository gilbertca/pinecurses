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
		self.draw_all_views()
		self['base_view'].window.getch()
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
		for view_key in self:
			view_instance = self.get(view_key)
			self.draw_view(view_instance)

	@log
	def draw_view(self, view_instance):
		"""
		Draws a particular view from a View instance.
		"""
		# Get the iterable for the display string:
		for item_key in view_instance:
			item_instance = view_instance.get(item_key)
			display_string_iterable = item_instance.get_display_string_iterable()
			# Final step:
			# NOTE: The following must be replaced with more generic terms,
			#	and must allow for attributes, positions, etc.
			lines_written = 0
			for display_string in display_string_iterable:
				view_instance.window.addstr(lines_written, 0, display_string)
				lines_written += 1
			view_instance.refresh()
