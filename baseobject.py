from logger import log

class BaseObject:
	"""BaseObject is an *abstract* object which all Pinecurses objects are to inherit. It contains most of the logic regarding **Pinecurses tree traversal**, i.e. handling child objects and parent objects. BaseObject is to be included with several mixins to create a proper Pinecurses object.
	"""
	style_filename = None
	def __init__(self, *args, **kwargs):
		self.CHILD_NAMESPACE = {}
		self.FUNCTIONS = {}
		# Shortcut for FUNCTIONS:
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		self.RESPONSES = {}
		# Shortcut for RESPONSES:
		self.responses = lambda response_name : self.RESPONSES.get(response_name)
		# TODO: UPDATE STYLE ATTRIBUTES
		#self.ATTRIBUTES =
		# Shortcut for ATTRIBUTES:
		#self.attributes = lambda name : self.ATTRIBUTES.get(name)
		# Child/Parent objects:
		self.parent = None
		self.children = None
		self.window = kwargs.get('window')
		self.pinecurses_instance = kwargs.get('pinecurses_instance')

	@log
	def draw(self, *args, **kwargs):
		"""draw checks if anything from this object needs to be drawn, and then checks all children. Therefore, all children check if they are to be drawn to the screen.
		"""
		pass

	@log
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
