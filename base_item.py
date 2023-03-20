from abstract_base_item import AbstractBaseItem

def BaseItem(AbstractBaseItem):
	"""
	Simplest Item which can be created and displayed.
	Inherits it's attributes from AbstractBaseItem
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		pass
