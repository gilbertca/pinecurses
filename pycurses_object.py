class PycursesObject(dict):
	"""
	The base functionality which all Pycurses objects inherit.
	"""
	def __init__(self, *args, **attributes):
		# TODO: UNPACK A DICT INTO super().__init... for creation at beginning
		super().__init__()
		self.FUNCTIONS = {}
		# Shortcut for FUNCTIONS:
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		self.ATTRIBUTES = attributes
		# Shortcut for ATTRIBUTES:
		self.attributes = lambda name : self.ATTRIBUTES.get(name)
		# Child/Parent objects:
		self.parent = None
		# Cursor object:
		class Cursor:
			# NOTE: This Cursor class is a temporary representation to accomodate
			# a future implementation of a Cursor object.
			def get_keypress(self):
				return None
		self.cursor = Cursor()

	def interact(self, keypress):
		"""
		The interact function is an integral part of any pycurses application.
		The interact function begins by being called at the Controller 
			(or highest level Pycurses Object).
		If a keypress does not have an associated function within the Controller,
			then is will call the interact method on one (or all)
			of its children (typically a View) until an associated keypress is found.
		After reaching a PycursesObject which has no children,
			and no method has been found associated with that particular keypress,
			then control is returned from the object at the 'bottom'
			of the the parent/child tree 
			back to the object at the top (ex. Controller).
		If a keypress is found to have an associated function, 
			then that function will be executed and control will be returned.
		"""
		# Check if self has a function mapped to the keypress:
		function_for_keypress = self.functions(keypress)
		# If there is a function for a keypress:
		if function_for_keypress:
			# Then run that function (or list of functions):
			response = self.handle_function(function_for_keypress)
			# If there is a response, handle and return:
			if response: 
				self.handle_response(response)
				return response
		# If there is no function for a keypress, then call the selected
		#	child's interact method.
		else:
			return self.cursor.get_selected_object().interact(keypress)

	def add_function(self, key, callback):
		"""
		Saves a key-value pair to self.FUNCTIONS in the form of:
			{key:callback}
		Where 'key_press' is a chr instance, and 'callback' references
			the function called when the key is pressed.
		"""
		new_mapping = {key : callback}
		self.FUNCTIONS.update(new_mapping)

	def add_function_dict(self, function_dict):
		"""
		Same as self.add_function, but takes a dict object
			as an argument.
		"""
		self.FUNCTIONS.update(function_dict)

	def handle_function(self, key_function):
		"""
		Takes either a reference to a function and calls it,
			or a list/tuple of functions and calls them in order.
		"""
		# If function is iterable:
		if hasattr(key_function, '__iter__'):
			for func in key_function:
				func() # Run each function
		# Otherwise, just run the function:
		else:
			return key_function()
		
	def handle_response(self, response):
		"""
		Pass
		"""
		pass