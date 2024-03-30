from baseobject import BaseObject
import re
from logger import log


class Leaf(BaseObject):
	"""A Leaf is the highest object in a *Pine tree*. A basic Leaf should be used for simple screen elements, such as title bars.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		# Style / content linking and shortcut:
		self.CONTENTS = {}

	@log
	def contents(self, content_key):
		"""Leaf.contents takes a key from a style dictionary, and returns a string from the function in the self.CONTENTS namespace.
		"""
		content_function = self.CONTENTS.get(content_key)
		content_string = None # Returns None if there is no function matching the key
		if content_function is not None: content_string = content_function()
		return content_string

	@log
	def draw(self):
		"""Leaf.draw returns a list of *drawing instructions* which will be used by Branch.draw to create the application on screen.
		"""
		content_template = self.style('content')
		contents = []
		content_keys = re.findall(r"{.*}", contents)
		

class BarLeaf(Leaf):
	"""A BarLeaf is a Leaf which requests an integer, and displays itself as a horizontal bar across a Branch. The height is assumed to be 1, unless explicitly set.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class ListLeaf(Leaf):
	"""A ListLeaf is a Leaf which requests a list of strings, and displays each string in a vertical list. The height of each item is assumed to be 1, unless explicitly set.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class TextboxLeaf(Leaf):
	"""A TextboxLeaf is a Leaf which relies on a curses Textbox to gather user input, and to return that input to the User's programmed API.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

