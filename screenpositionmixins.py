import math
from logger import log


class ScreenPositioner:

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@log
	def handle_styles(self, *args, **kwargs):
		"""ScreenPositioner.handle_styles runs all style-related calculations before passing control to the next module.
		"""
		self.calculate()
		super().handle_styles(*args, **kwargs)

	@log
	def calculate(self):
		"""
		Called by a child PycursesObject to run all _calculate_* functions.
		"""
		# List comprehension which provides a list of functions which start with '_calculate'
		calculate_function_names = [
			function_name for function_name in dir(self) if function_name.startswith('_calculate')
		]
		# Iterate and run all functions:
		for function_name in function_name_iterable:
			current_function = getattr(self, function_name)
			current_function()

	@log
	def calculate_helper(self, attribute_dict):
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
			attribute = self.style(attribute_key) # Actual attribute value
			if attribute is not None: # Call the given function with the attribute:
				return attribute_dict.get(attribute_key)(attribute)
		default_method = attribute_dict.get('default')
		if default_method:
			return default_method(attribute)
		raise AttributeError(f"calculate_helper was unable to find a required attribute or default value. Attribute dict: - {attribute_dict} -")

	@log
	def _calculate_height(self):
		"""
		Method which calculates and assigns the value for self.height
		"""
		# Namespace for attributes related to height:
		height_atr_namespace = {
			'height' : lambda height_int : height_int, # Simple height
			'vborder' : lambda vborder_int : self.parent.window.getmaxyx()[0] - (2 * vborder_int), # Cells from vertical edge to content.
			'vpercent' : lambda vpercent_int : math.floor(self.parent.window.getmaxyx()[0] * vpercent_int / 100), # Percent of window height.
			'default' : lambda *default : self.parent.window.getmaxyx()[0], # Default is full width
		}
		calculated_value = self.calculate_helper(height_atr_namespace)
		self.height = calculated_value

	@log
	def _calculate_width(self):
		"""
		Method which calculates and assigns the value for self.width
		"""
		# Namespace for attributes related to width:
		width_atr_namespace = {
			'width' : lambda width_int : width_int, # Simple width
			'hborder' : lambda hborder_int : self.parent.window.getmaxyx()[1] - (2 * hborder), # Cells from horizontal edge to content.
			'hpercent' : lambda hpercent_int : math.floor(self.parent.window.getmaxyx()[1] * hpercent_int / 100), # Percent of window width.
			'default' : lambda *default : self.parent.window.getmaxyx()[1], # Default is full width
		}
		calculated_value = self.calculate_helper(width_atr_namespace)
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
				maxy = self.parent.window.getmaxyx()[0]
				center = math.floor(maxy/2) # Always move up 1 from center if odd!
				topy = center - math.floor(self.height/2) # Always move up 1!
				boty = center + math.ceil(self.height/2) # Always move up 1!
				return topy, boty
			# Callback for bottom:
			def bottom(*args):
				maxy = self.parent.window.getmaxyx()[0]
				topy = maxy - self.height
				boty = maxy
				return topy, boty
			
			# Vertical alignment namespace:
			valign_namespace = {
				'top' : top, # Window to top
				'center' : center, # Window to center
				'bottom' : bottom, # Window to bottom
				'default' : center, # Window to center
			}
			if attribute is None: attribute = 'default'
			valign_function = valign_namespace.get(attribute)
			return valign_function()
		 
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
		self.topy, self.boty = self.calculate_helper(y_align_namespace)
		
	@log
	def _calculate_window_x_coords(self):
		"""
		Method which calculates self.leftx and self.rightx
		"""
		# Callback for halign
		def halign(attribute=None):
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
				maxx = self.parent.window.getmaxyx()[1]
				center = math.floor(maxx/2) # Always move up 1 from center if odd!
				leftx = center - math.floor(self.width/2) # Always move right 1!
				rightx = center + math.ceil(self.width/2) # Always move right 1!
				return leftx, rightx
			# Callback for bottom:
			def right(*args):
				maxx = self.parent.window.getmaxyx()[1]
				leftx = maxx - self.width
				boty = maxx
				return leftx, rightx

			# Horizontal alignment namespace:
			halign_namespace = {
				'left' : left, # Window to left
				'center' : center, # Window to center
				'right' : right, # Window to right
				'default' : center, # Window to center
			}
			if attribute is None: attribute = 'default'
			halign_function = halign_namespace.get(attribute)
			return halign_function()

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
		self.leftx, self.rightx = self.calculate_helper(x_align_namespace)
	
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
		self.ypadding, self.xpadding = self.calculate_helper(padding_namespace)


