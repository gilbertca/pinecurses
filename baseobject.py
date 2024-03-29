from logger import log

class BaseObject:
	"""BaseObject is an *abstract* object which all Pinecurses objects are to inherit. It contains most of the logic regarding **Pinecurses tree traversal**, i.e. handling child objects and parent objects. BaseObject is to be included with several mixins to create a proper Pinecurses object.
	"""
	def __init__(self, pinecurses_instance, style_filename=None, style_attributes=None, parent_object_instance=None, *args, **kwargs):
		# Functions and shortcut:
		self.FUNCTIONS = {}
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		# Responses and shortcut:
		self.RESPONSES = {}
		self.responses = lambda response_name : self.RESPONSES.get(response_name)
		# Child/Parent objects:
		self.parent = parent_object_instance
		self.children = None
		self.child = lambda child_name : self.children.get(child_name)
		self.window = kwargs.get('window')
		self.pinecurses_instance = pinecurses_instance
		# Style attributes and shortcut:
		if style_filename is not None: # I.E. if there is a style filename
			self.style_filename = style_filename
			self.STYLE = self.pinecurses_instance.get_style_attributes(self.style_filename)
		elif style_attributes is not None: # I.E. if there is a style dictionary
			self.STYLE = style_attributes
		self.style = lambda style_key : self.STYLE.get(style_key)
		self.handle_styles()
		
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

	@log
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

	@log
	def handle_styles(self, **_style_namespace):
		"""handle_styles iterates through self.STYLES and runs functions based on the attribute name.
		"""
		style_namespace = {
			"children" : self.handle_children,
		}
		style_namespace.update(style_namespace)
		# Iterate through and run all functions associated from the namespace:
		for style_key in style_namespace:
			style_value = self.style(style_key)
			if style_value is not None: # If namespace key matches a style value:
				style_function = style_namespace.get(style_key)
				style_function(style_value)

	@log
	def handle_children(self, child_style_iterable):
		"""handle_children
		"""
		# Iterate through the iterable of key-value pairs:
		for child_style in child_style_iterable:
			self.handle_child(child_style)

	@log
	def handle_child(self, child_style):
		"""handle_child handles a single child object using a key-value pair child_style
		"""
		# If there are children, then BaseObject's self.children becomes a dictionary:
		if self.children is None: self.children = {}
		# Variables for creating child objects:
		child_object_instance = None
		# Reference name used to get a class reference from a Pinecurses object
		child_class_reference_name = child_style.get('class_reference_name')
		child_class_reference = self.pinecurses_instance.class_references(child_class_reference_name)
		# If style_filename is None, then the attributes are nested within the parent's style file.
		style_filename = child_style.get('style_filename')
		style_attributes = child_style if style_filename is None else None
		# Create and add the object instance to self.children
		child_object_instance = child_class_reference(
			self.pinecurses_instance, 
			style_filename=style_filename, 
			style_attributes=style_attributes
		)
		child_object_name_dict = {child_class_reference_name : child_object_instance}
		self.children.update(child_object_name_dict)
