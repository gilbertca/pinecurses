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

	def get_display_string(self, available_width):
		"""
		This function determines truncation and other effects
			which may happen to self.text.
		It takes into account the provided width, and chops
			the display string following a determined pattern.
		For now: only takes a display width, and then truncates
			the self.text string using two '.' characters.
		WE HAVE TO THINK ABOUT VERTICAL WIDTH AND HORIZONTAL WIDTH
		"""
		split_list = self.text
		return display_string

	def calculate_text_height(self):
		"""
		Returns length of self.text, as self.text is a list of display strings.
		"""
		return len(self.text)
