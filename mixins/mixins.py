import math
from logger import log

class ScreenPositioner:

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@log
	def calculate(self):
		"""
		Called by a child PycursesObject to run all _calculate_* functions.
		"""
		# List comprehension which provides a list of functions which contain '_calculate'
		#	in their definition name.
		calculate_function_names = [
			function_name for function_name in dir(self) if '_calculate' in function_name
		]
		# Iterate and run all functions:
		for function_name in calculate_function_names:
			calculate_function = self.__getattribute__(function_name)
			calculate_function()

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
			attribute = self.attributes(attribute_key) # Actual attribute value
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
			'vborder' : lambda vborder_int : self.parent.window.getmaxyx()[0] - (2 * vborder), # Cells from vertical edge to content.
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

"""
NOTE: Any object that inherits a Cursor object MUST
inherit from a PycursesObject as their top-level parent.
I.E. PycursesObject must be the farthest right inherited object.
"""


class Cursor:
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def select_item(self, item_instance):
		"""
		Takes an instance of an Item and runs it's on_select function.
		"""
		pass

class SingleObjectCursor(Cursor):
	  
	def __init__(self, *args, **kwargs):
		 """
		 NOTE: wrap_objects relies on an attribute in a json file.
		 """
		 super().__init__(*args, **kwargs)
		 wrap_objects = kwargs.get('wrap_objects')
		 self.wrap_objects = False if wrap_objects is None else wrap_objects
		 self.selected_object_index = 0
		 self.selected_object = lambda : self.children[self.selected_object_index]

	def get_selected_object(self):
		return self.selected_object()

	def select(self, *args, **kwargs):
		"""
		Runs the select method of the child currently selected by the Cursor.
		"""
		selected_child = self.get_selected_object()
		return selected_child.select(*args, **kwargs)
		@log
	def handle_mouse_click(self, x, y):
		"""
		This method is called when a mouse click is detected.
		It checks if the click coordinates correspond to the position of any item,
		and if so, it calls the item's OnClick() method.
		"""
		print("Handling breh")
		# Iterate over all items
		for item in self.children:
   		 # If the click occurred within the item's bounds
			if item.x <= x < item.x + item.width and item.y <= y < item.y + item.height:
				# Call the item's OnClick() method
				item.OnClick()
				break  # Exit the loop once we've found a clicked item

	def next_object(self):
		"""
		Increments self.selected_object_index by 1.
		If wrap_objects = True, and the Cursor is pointing at the last object,
			then self.selected_object_index will become 0 (to indicate returning to the top of the list).
		If wrap_objects = False, and the Cursor is pointing at the last object,
			then nothing happens.
		"""
		# end_of_list is True when self.selected_object_index is at the end of the selected_object_list
		end_of_list = lambda : self.selected_object_index == len(self.selected_object_list) - 1
		# If EOL and wrapping enabled: set self.selected_object_index to 0
		if end_of_list() and (self.wrap_objects == True):
			self.selected_object_index = 0
		# If EOL and wrapping disabled: do nothing
		elif end_of_list() and (self.wrap_objects == False):
			pass
		# If not EOL: increment self.selected_object_index by 1
		else:
			self.selected_object_index += 1

	def previous_object(self):
		"""
		Decrements self.selected_object_index by 1.
		If wrap_objects = True, and the Cursor is pointing at the first object,
			then self.selected_object_index will be set to 
			the length of self.selected_object_list minus 1 (to indicate going to the end of the list).
		If wrap_objects = False, and the Cursor is pointing at the first object,
			then nothing happens.
		"""
		# start_of_list is True when self.selected_object_index is at the beginning of the selected_object_list
		start_of_list = lambda : self.selected_object_index == 0
		# If SOL and wrapping enabled: set self.selected_object_index to length of self.selected_object_list minus 1
		if start_of_list() and (self.wrap_objects == True):
			self.selected_object_index = len(self.selected_object_list) - 1
		# If SOL and wrapping disabled: do nothing
		elif start_of_list() and (self.wrap_objects == False):
			pass
		# If not EOL: increment self.selected_object_index by 1
		else:
			self.selected_object_index += 1

