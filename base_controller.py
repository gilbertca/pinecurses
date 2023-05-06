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

	@log
	def begin(self):
		"""
		The main loop of any pycurses program. Once this function returns anything,
			then the program will end.
		"""
		self.initialize_all_views()
		self.draw_all_views()
		self.map_all_colors()
		view_instance = self['base_view']
		view_instance.window.getch()
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
	def initialize_all_views(self):
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
		view_instance.draw_self()

	@log
	def map_all_colors(self):
		"""
		Iterates through all Views contained within self's dict
		and maps their colors in self.colors..
		"""
		for view_key in self:
			view_instance = self.get(view_key)
			self.map_colors(view_instance)

	@log
	def map_colors(self, view_instance):
		"""
		Maps all colors within the Controller.
		"""
		view_name = view_instance.attributes('name')
		self.colors.update({view_name : {}})
		color_attributes = view_instance.get_color_attributes()
		# Iterate through color defining attributes:
		for color_key in color_attributes:
			color_value = color_attributes.get(color_key)
			if color_value == 0:
				self.colors.get(view_name).update({color_key : 0})

	@log
	def _next_color_pair(self):
		"""
		Returns an integer equal to the next init-able curses color pair.
		"""
		count = 0
		# Iterate and count through all views:
		for view_key in self:
			view_name = self.get(view_key).attributes('name')
			color_dict = self.colors.get(view_name)
			# Iterate through the View's color dictionary:
			for color_key in color_dict:
				# Remember: color_integer is a curses color pair.
				color_integer = color_dict.get(color_key)
				if color_integer > 0:
					count += 1
		return count
