from abstract_base_container import AbstractContainer

class Container(AbstractContainer):
	"""
	A list of Items is held within a Container.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
