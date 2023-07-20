import math
import curses
from pycurses_object import PycursesObject
from mixins import ScreenPositioner
from logger import log


class BaseView(ScreenPositioner, PycursesObject):
	"""
	The base View class which controls all items of a Pycurses program.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)

	@log
	def create_item(self, **attributes):
		"""
		Causes a View to create an Item instance,
			and assign it to self's dictionary.
		"""
		# Instantiate instance of an Item:
		item_instance = BaseItem(self, **attributes)
		# Update self's dictionary as {name : instance}:
		self.update({item_instance.attributes('name') : item_instance})

	@log
	def initialize(self, parent_controller_instance, **object_dict):
		"""
		Runs all calculations and sets all attributes for a View instance.
		Perhaps this should be run with each resize after the parent Controller
			modifies the View-Instance's attributes.
		"""
		self.name = self.attributes('name')
		self.parent = parent_controller_instance
		self.background_character = self.attributes('background_character') if self.attributes('background_character') else ' '
		self._calculate_height()
		self._calculate_width()
		self._calculate_window_y_coords()
		self._calculate_window_x_coords()
		self._calculate_padding()
		self.create_curses_pad()
		self.initialize_all_items(**object_dict)

	@log
	def initialize_all_items(self, **object_dict):
		"""
		Runs Item.initialize(..) on all ItemInstances from
			the object_dict.
		Also adds references to the items in self's dict.
		"""
		self.children = object_dict.get('items')
		for item_instance in self.children:
			item_instance.initialize(self)

	@log
	def create_curses_pad(self):
		"""
		After all 'calculate' methods are called, this method
			can create a curses pad instance.
		"""
		self.window = curses.newpad(self.height, self.width)

	@log
	def draw_all_items(self):
		"""
		Iterates through all items and calls self.draw_item(..) on each.
		"""
		for item_key in self: # Iterate through self's dict:
			item_instance = self.get(item_key)
			writable_height = self.get_writable_height()
			writable_width = self.get_writable_width()
			# Determine if item CAN be written to the screen:
			if writable_height != 0 and writable_width != 0:
				self.draw_all_lines(item_instance, writable_height, writable_width)
				# Finish by assigning True to item_instance.is_drawn:
				item_instance.is_drawn = True

	@log
	def draw_all_lines(self, item_instance, writable_height, writable_width):
		"""
		Takes an Item instance and adds all lines to the screen.
		"""
		display_string_iterable = item_instance.get_display_string_iterable()
		lines_written = 0
		# x and y values can be assigned to the length of the 'unwritable' length,
		# 	because the *next writable index* is equal to that length.
		x = self.xpadding
		y = self.ypadding + self.get_height_of_items()
		color_integer = self.parent.color(self.name, 'text_color')
		# Remember: Items format themselves!
		for display_string in display_string_iterable:
			if (writable_height - lines_written) > 0:
				# Add the string to the window (does not refresh).
				self.window.addstr(y+lines_written, x, display_string, curses.color_pair(color_integer))
				# Populate the Item's dictionary with the display strings:
				item_instance.update({lines_written : display_string})
				# Increment line counter:
				lines_written += 1
		item_instance.height = lines_written
		item_instance.width = writable_width

	@log
	def draw_background(self):
		"""
		Sets the background character and color.
		"""
		color_integer = self.parent.color(self.name, 'background_color')
		self.window.bkgd(self.background_character, curses.color_pair(color_integer))

	@log
	def draw_self(self):
		"""
		Draws self by running self.draw_all_items() and self.refresh()
		"""
		self.draw_all_items()
		self.draw_background()
		self.refresh()

	@log
	def get_color_attributes(self):
		"""
		Returns all attributes which contain "color" within their key.
		Returns "text_color" : 0 and "background_color" : 0 if they
			are not contained within self.ATTRIBUTES.
		"""
		# TODO: REPLACE HARD-CODING FOR DEFAULTS
		_defaults = {'text_color' : 0, 'background_color': 0}
		color_dict = {}
		# Find all attributes which contain "color":
		for attribute_key in self.ATTRIBUTES:
			if "color" in attribute_key:
				color_dict.update({attribute_key : self.attributes(attribute_key)})
		# Ensure default attributes are contained within color_dict:
		for default_key in _defaults:
			# If color_dict does not contain one of the default values:
			if not color_dict.get(default_key):
				color_dict.update({default_key : _defaults.get(default_key)})
		# Finally, return the color dictionary for self.
		return color_dict

	@log
	def get_writable_width(self):
		"""
		Returns an integer equal to the number of writable columns in the current window.
		"""
		writable_width = self.width - (self.xpadding * 2)
		return writable_width
			
	@log
	def get_writable_height(self):
		"""
		Returns an integer equal to the number of writable lines in the current window.
		"""
		height_of_items = self.get_height_of_items()
		# Formula: total height - top and bottom padding - used height
		return (self.height - (2 * self.ypadding) - height_of_items)
		
	@log
	def get_height_of_items(self):
		"""
		Returns an integer as the height of all items where
			Item.is_drawn is True.
		"""
		height = 0
		for item_key in self:
			item_instance = self.get(item_key)
			if item_instance.is_drawn:
				height += item_instance.height
		return height

	@log
	def refresh(self):
		"""
		Refreshes self.window.
		"""
		self.window.refresh(*(0, 0, self.topy, self.leftx, self.boty, self.rightx))
