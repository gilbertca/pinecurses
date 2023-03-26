class FunctionsMixin:
	"""
	Mixin which provides self.functions, 
		the standard for the pycurses function/key-mapping 
		functionality.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.FUNCTIONS = {}
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))

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
