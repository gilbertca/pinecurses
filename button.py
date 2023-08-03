from base_item import BaseItem


class Button(BaseItem):
	"""
	Gives a select function to an Item making it clickable.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.FUNCTIONS.update({curses.KEY_ENTER:self.select})

	def select(self, keypress, *args, **kwargs):
		"""
		Runs a function associated with a keypress.
		"""
		return self.functions(keypress)

