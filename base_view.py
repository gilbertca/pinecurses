import math
import curses
from pycurses_object import PycursesObject
from base_item import BaseItem
from utils import log


class BaseView(PycursesObject):
	"""
	The base View class which controls all items of a Pycurses program.
	"""
	def __init__(self, parent_controller_instance, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		# Assign parent:
		self.controller = parent_controller_instance

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
	def initialize(self):
		"""
		Runs all calculations and sets all attributes for a View instance.
		Perhaps this should be run with each resize after the parent Controller
			modifies the View-Instance's attributes.
		"""
		self.name = self.attributes('name')
		self.background_character = self.attributes('background_character') if self.attributes('background_character') else ' '
		self._calculate_height()
		self._calculate_width()
		self._calculate_window_y_coords()
		self._calculate_window_x_coords()
		self._calculate_padding()
		self.create_curses_pad()

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
		color_integer = self.controller.color(self.name, 'text_color')
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
		color_integer = self.controller.color(self.name, 'background_color')
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
	
	@log
	def _calculate_helper(self, attribute_dict):
		"""
		Method which takes an *atr_dict*, iterates, runs the function,
			and returns the final attribute.
		EX: {'key' : callback}
		If a keyword is found this method will run the associated function
			with an attribute from self.ATR,
			otherwise it will call the 'default'.
		Default functions can take *args to prevent errors, while returning a static value.
		"""
		for attribute_key in attribute_dict: # Iterate
			attribute = self.attributes(attribute_key) # Actual attribute value
			if attribute: # Call the given function with the attribute:
				return attribute_dict.get(attribute_key)(attribute)
		default_method = attribute_dict.get('default')
		if default_method:
			return default_method(attribute)
		raise AttributeError(f"_calculate_helper was unable to find a required attribute or default value. Attribute dict: - {attribute_dict} -")

	@log
	def _calculate_height(self):
		"""
		Method which calculates and assigns the value for self.height
		"""
		# Namespace for attributes related to height:
		height_atr_namespace = {
			'height' : lambda height_int : height_int, # Simple height
			'vborder' : lambda vborder_int : curses.LINES - (2 * vborder), # Cells from vertical edge to content.
			'vpercent' : lambda vpercent_int : math.floor(curses.LINES * vpercent_int / 100), # Percent of window height.
			'default' : lambda *default : curses.LINES, # Default is full width
		}
		calculated_value = self._calculate_helper(height_atr_namespace)
		self.height = calculated_value

	@log
	def _calculate_width(self):
		"""
		Method which calculates and assigns the value for self.width
		"""
		# Namespace for attributes related to width:
		width_atr_namespace = {
			'width' : lambda width_int : width_int, # Simple width
			'hborder' : lambda hborder_int : curses.COLS - (2 * hborder), # Cells from horizontal edge to content.
			'hpercent' : lambda hpercent_int : math.floor(curses.COLS * hpercent_int / 100), # Percent of window width.
			'default' : lambda *default : curses.COLS, # Default is full width
		}
		calculated_value = self._calculate_helper(width_atr_namespace)
		self.width = calculated_value

	@log
	def _calculate_window_y_coords(self):
		"""
		Method which calculates self.topy and self.boty
		"""
		# Callback for valign:
		def valign(attribute):
			"""
			Runs calulations for vertical keyword alignment
			"""
			# Callback for top:
			def top(*args):
				topy = 0
				boty = 0 + self.height -1
				return topy, boty
			# Callback for center:
			def center(*args):
				maxy = curses.LINES
				center = math.floor(maxy/2) # Always move up 1 from center if odd!
				topy = center - math.floor(self.height/2) # Always move up 1!
				boty = center + math.ceil(self.height/2) # Always move up 1!
				return topy, boty
			# Callback for bottom:
			def bottom(*args):
				maxy = curses.LINES
				topy = maxy - self.height
				boty = maxy - 1
				return topy, boty
			
			# Vertical alignment namespace:
			valign_namespace = {
				'top' : top, # Window to top
				'center' : center, # Window to center
				'bottom' : bottom, # Window to bottom
				'default' : center, # Window to center
			}
			return self._calculate_helper(valign_namespace)
		 
		# Callback for given topy value
		def topy_given(self, topy):
			"""
			Runs calculations for a given topy.
			Will create boty from height if only topy is given.
			"""
			boty = self.atr('boty')
			if not boty: # No boty means calculate it:
				boty = topy + self.height
			return topy, boty

		# Namespace for attributes related to vertical alignment:
		# NOTE: CAN TAKE A GIVEN TOPY ONLY, BUT NOT ONLY BOTY
		y_align_namespace = {
			'valign' : valign, # Returns (topy, boty) for screen alignment
			'topy' : topy_given, # Returns (topy, boty) for given topy value
			'default' : valign,
		}
		# Calculate and assign variables:
		self.topy, self.boty = self._calculate_helper(y_align_namespace)
		
	@log
	def _calculate_window_x_coords(self):
		"""
		Method which calculates self.leftx and self.rightx
		"""
		# Callback for halign
		def halign(attribute):
			"""
			Runs calulations for horizontal keyword alignment
			"""
			# Callback for left:
			def left(*args):
				leftx = 0
				rightx = 0 + self.width -1
				return leftx, rightx
			# Callback for center:
			def center(*args):
				maxx = curses.COLS
				center = math.floor(maxx/2) # Always move up 1 from center if odd!
				leftx = center - math.floor(self.width/2) # Always move right 1!
				rightx = center + math.ceil(self.width/2) # Always move right 1!
				return leftx, rightx
			# Callback for bottom:
			def right(*args):
				maxx = curses.COLS
				leftx = maxx - self.width
				boty = maxx - 1
				return leftx, rightx

			# Horizontal alignment namespace:
			halign_namespace = {
				'left' : left, # Window to left
				'center' : center, # Window to center
				'right' : right, # Window to right
				'default' : center, # Window to center
			}
			return self._calculate_helper(halign_namespace)

		# Callback for a given leftx value
		def leftx_given(self, leftx):
			rightx = self.atr('rightx')
			if not rightx:
				rightx = leftx + self.width
			return leftx, rightx

		# Namespace for attributes related to horizontal alignment
		x_align_namespace = {
			'halign' : halign,
			'leftx' : leftx_given,
			'default' : halign,
		}
		# Calculate and assign variables:
		self.leftx, self.rightx = self._calculate_helper(x_align_namespace)
	
	@log
	def _calculate_padding(self):
		"""
		Figures and assigns hpadding and ypaddinng values
		"""
		def asym_padding(*args):
			"""
			Calculates and returns padding if xpadding or ypadding is used.
			"""
			ypadding = self.atr('ypadding')
			xpadding = self.atr('xpadding')
			if not ypadding:
				ypadding = 0
			if not xpadding:
				xpadding = 0
			return ypadding, xpadding
			
		padding_namespace = {
			'padding' : lambda padding : (padding, padding),
			'xpadding' : asym_padding,
			'ypadding' : asym_padding,
			'default' : lambda *default : (0, 0),
		}
		self.ypadding, self.xpadding = self._calculate_helper(padding_namespace)
