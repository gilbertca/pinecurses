class PycursesObject(dict):
	"""
	The base functionality which all Pycurses objects inherit.
	"""
	def __init__(self, *args, **kwargs):
		TODO: UNPACK A DICT INTO super().__init... for creation at beginning
		super().__init__()
		self.FUNCTIONS = {}
		# Shortcut for FUNCTIONS:
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		self.ATTRIBUTES = {}
		# Shortcut for ATTRIBUTES:
		self.attributes = lambda name : self.ATTRIBUTES.

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
		self.FUNCTIONS.update(function_dict)""
