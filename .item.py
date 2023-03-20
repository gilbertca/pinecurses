class Item:

	def __init__(self, parent_view *args, **kwargs):
		# A reference to the view which this item is displayed in:
		self.parent_view = parent_view

	def get_addstr_values(self):
		"""
		Returns an iterable which will be unpacked
			into ViewInstance.screen.addstr(*iterable)
		"""
		pass
