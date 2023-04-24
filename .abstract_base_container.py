class AbstractContainer(list):
	"""
	The highest abstraction of a Container.
	To be inherited by BaseContainer.
	"""
	def __init__(self, item_list=None, *args, **kwargs):
		if item_list: super().__init__(item_list, *args, **kwargs)
