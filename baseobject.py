class BaseObject:
	"""
	The base functionality which all Pycurses objects inherit.
	"""
	style_filename = None
	def __init__(self, *args, **attributes):
		# TODO: UNPACK A DICT INTO super().__init... for creation at beginning
		super().__init__()
		self.CHILD_NAMESPACE = {}
		# def self.getchild = return CHILD_NAMESPACE.get(child_class_name).get(ChildClassReference)(**parse(CHILD_NAMESPACE.get(child_class_name).get(style_directory)))
		self.FUNCTIONS = {}
		# Shortcut for FUNCTIONS:
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		self.RESPONSES = {}
		# Shortcut for RESPONSES:
		self.responses = lambda response_name : self.RESPONSES.get(response_name)
		self.ATTRIBUTES = attributes
		# Shortcut for ATTRIBUTES:
		self.attributes = lambda name : self.ATTRIBUTES.get(name)
		# Child/Parent objects:
		self.parent = None
		self.children = None
		self.window = None

	def interact(self, keypress):
		"""
		The interact function is an integral part of any Pinecurses application.
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
		if function_for_keypress:
			response = self.handle_function(function_for_keypress)
			response_function = self.responses(response)
			# If there is a response, handle and return:
			if response_function is not None: 
				return self.handle_function(response)
			if response is not None:
				return response
		# If there is no function for a keypress, then call the selected
		#	child's interact method.
		elif self.children is not None:
			return self.get_selected_object().interact(keypress)

	def select(self, *args, **kwargs):
		"""
		Must be overridden by a child class.
		"""
		raise Exception("This method must be overridden by a child class.")

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
		"""BaseObject.handle_function takes a *key_function* parameter, which can either be a callable method reference, or an iterable of callable references, runs the function, and returns any values returned by the function.
		"""
		responses_iterable = None
		# If function is iterable:
		if hasattr(key_function, '__iter__'):
			# Run each function, and pack their responses into a list:
			responses_iterable = [func() for func in key_function]
		# Else: return the return from the function:
		else:
			return key_function()
		# Return for first if statement:
		return responses_iterable
