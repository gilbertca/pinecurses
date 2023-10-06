from baseobject import BaseObject
from logger import log


class Leaf(BaseObject):
	"""A Leaf is the highest object in a *Pine tree*. A basic Leaf should be used for simple screen elements, such as title bars.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.is_drawn = False
		self.height = 0
		self.width = 0
		self.display_dictionary = {}

	def draw(self):
		"""Requests the Leaf's parent window object, and draws itself to the window.
		"""
		branch_window = self.parent.window
		drawing_instruction_list = self._get_drawing_instructions()
		for instruction in drawing_instruction_list:
			branch_window.addstr(instruction)

	def _get_drawing_instructions(self):
		"""Returns a list of instructions which are to be used by self.draw. This method must be overloaded by a child element.
		"""
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

