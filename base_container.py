from abstract_base_container import AbstractContainer

class Container(AbstractContainer):
	"""
	A list of Items is held within a Container.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def assign_item(self, item, start_index, height):
		# Assign n spaces for the item's height:
		for n in range(start_index, height):
			self[n] = item
