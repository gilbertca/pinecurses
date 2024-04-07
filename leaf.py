from baseobject import BaseObject
import re
from logger import log


class Leaf(BaseObject):
	"""A Leaf is the highest object in a *Pine tree*. A basic Leaf should be used for simple screen elements, such as title bars.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Style / content linking and shortcut:
		self.CONTENTS = {}

	@log
	def content(self, content_key):
		"""Leaf.content takes a key from a style dictionary, and returns a string from the function in the self.CONTENTS namespace.
		"""
		content_function = self.CONTENTS.get(content_key)
		content_string = None # Returns None if there is no function matching the key
		if content_function is not None: content_string = content_function()
		return content_string

	@log
	def draw(self):
		"""Leaf.draw returns a list of *drawing instructions* which will be used by Branch.draw to create the application on screen.
		"""
		regex_string = r"{.*}" # Regex includes brackets {}
		content_template = self.style('content') # Read style
		# Get keys from style
		for content_key in re.findall(regex_string, content_template): # Get all keys, and format content_template
			content = self.contents(content_key[1:-1]) # Ensure brackets are shaved
			content_template = content_template.replace(content_key, content)
		height, width = self.parent.window.getmaxyx() # Get bounds
		# Namespace for special methods which calculate spacing based on halign and valign
		alignment_cases = {
			('center') : self._center_case,
			('left','top') : self._beginning_case,
			('right','bottom') : self._end_case
		}
		# Iterate through the keys:
		for content_row in content_template.split('\n') # Rows are split by newlines
			pass # TODO MOVE ALIGNMENT CASES TO SCREENPOSITIONER

	@log
	def _center_case(self):
		pass

	@log
	def _beginning_case(self):
		pass

	@log
	def _end_case(self):
		pass


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

