from pycurses_object import PycursesObject
from utils import log


class BaseItem(PycursesObject):
	"""
	The base Item which determines how strings / buttons / etc. should be displayed.
	"""
	def __init__(self, parent_view_instance, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.view = parent_view_instance
