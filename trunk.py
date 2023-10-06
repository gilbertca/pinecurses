import curses
from baseobject import BaseObject
from mixins.cursormixins import SingleObjectCursor
from logger import log

class Trunk(SingleObjectCursor, BaseObject):
	"""
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
	def begin(self, stdscr, **object_dict):
		"""
		The main loop of any pinecurses program. Once this function returns anything,
			then the program will end.
		"""
		self.window = stdscr
		self.initialize(**object_dict)
		self.map_all_colors()
		self.draw_all_views()
		# Once self.interact(..) returns a value, program will end.
		while True:
			# Get the keypress from a child window:
			keypress = self.get_selected_window().getch()
			if self.interact(keypress) == 0:
				return 0

	@log
	def color(self, view_name, color_name):
		"""
		A shortcut for accessing the nested structure of self.colors.
		self.colors = {
			"view_name" : {"color_name" : 1 <-- returns this},
		}
		"""
		return self.colors.get(view_name).get(color_name)

	@log
	def initialize(self):
		"""MAY NEED TO REMOVE THIS FUNCTION AS SCHEMA CHANGES.
		"""
		pass

	@log
	def draw_all_views(self):
		"""
		Draws all views within self's dictionary.
		"""
		for view_instance in self.children:
			view_instance.draw_self()

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
			pair_number = self._next_color_pair()
			# color_attributes will contain default values automatically!
			# TODO: NEED 3 CASES: 0 VALUE, STRING VALUE, LIST VALUE
			if color_value == 0: # Map default black on white case:
				# Remember: No need to initialize pair number 0
				#due to curses' hardcoded values.
				self.colors.get(view_name).update({color_key : 0})
			elif isinstance(color_value, str): # Map text on default background:
				# Request the Controller's default background:
				colors = [self.CURSES_COLOR_MAP.get(color_value), self.DEFAULT_BACKGROUND_COLOR]
				# Update self's reference from 'text_color' to a curses pair number:
				self.colors.get(view_name).update({color_key : pair_number})
				# Finally initialize the pair within curses:
				curses.init_pair(pair_number, *colors)
			elif isinstance(color_value, list): # Map text and background:
				# Begin by taking the names of the colors, and getting
				#their curses counterpart integers, and pack into a list:
				colors = [self.CURSES_COLOR_MAP.get(color) for color in color_value]
				# Update the reference in self.colors:
				self.colors.get(view_name).update({color_key : pair_number})
				# Initialize the pair within curses:
				curses.init_pair(pair_number, *colors)

	@log
	def _next_color_pair(self):
		"""
		Returns an integer equal to the next init-able curses color pair.
		"""
		count = 1
		# Iterate and count through all views:
		for view_instance in self.children:
			view_name = view_instance.name
			color_dict = self.colors.get(view_name)
			# Iterate through the View's color dictionary:
			for color_key in color_dict:
				# Remember: color_integer is a curses color pair.
				color_integer = color_dict.get(color_key)
				if color_integer > 0:
					count += 1
		return count
