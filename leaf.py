from baseobject import BaseObject
from logger import log


class Leaf(BaseObject):
	"""

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

	def _get_drawing_instructions(self):
		"""Returns a list of instructions which are to be used by self.draw. This method must be overloaded by a child element.
		"""
		pass

	def initialize(self, parent_view_instance):
		"""
		Sets attributes for the ItemInstance once all
			objects have been created.
		"""
		self.parent = parent_view_instance


class BarLeaf(Leaf):
	"""A BarLeaf is a Leaf which requests an integer, and displays iteself as a horizontal bar across a Branch. The height is assumed to be 1, unless explicitly set.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class ListLeaf(Leaf):
	"""A ListLeaf is a Leaf which requests a list of strings, and displays each string in a vertical list. The height of each item is assumed to be 1, unless explicitly set.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

