from logger import log

class BaseObject:
	"""BaseObject is an *abstract* object which all Pinecurses objects are to inherit. It contains most of the logic regarding **Pinecurses tree traversal**, i.e. handling child objects and parent objects. BaseObject is to be included with several mixins to create a proper Pinecurses object.
	"""
	def __init__(self, style_filename=None, *args, **kwargs):
		# Children and shortcut:
		self.CHILD_NAMESPACE = {}
		self.child = lambda child_name : self.CHILD_NAMESPACE.get(child_name)
		# Functions and shortcut:
		self.FUNCTIONS = {}
		self.functions = lambda key_press : self.FUNCTIONS.get(chr(key_press))
		# Responses and shortcut:
		self.RESPONSES = {}
		self.responses = lambda response_name : self.RESPONSES.get(response_name)
		# Child/Parent objects:
		self.parent = None
		self.children = None
		self.window = kwargs.get('window')
		self.pinecurses_instance = kwargs.get('pinecurses_instance')
		# Style attributes and shortcut:
		self.style_filename = style_filename
		self.STYLE = {}
		self.style = lambda style_key : self.STYLE.get(style_key)
		self.handle_styles() # This function must be defined by all BaseObject children!

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

	def handle_styles(self, **style_namespace):
		"""handle_styles iterates through self.STYLES and runs functions based on the attribute name.
		"""
		_style_namespace = {
			"children" : self.handle_children,
		}
		_style_namespace.update(style_namespace)