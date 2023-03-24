from abstract_base_item import AbstractBaseItem
from mixins import FunctionsMixin

def BaseItem(AbstractBaseItem, FunctionsMixin):
	"""
	Simplest Item which can be created and displayed.
	Inherits it's attributes from AbstractBaseItem
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = kwargs.get('name') # Item name for namespacing
		self.text = kwargs.get('text') # Item text to be displayed
		# Additional attributes the item displays:
		self.curses_attributes = kwargs.('curses_attributes')
