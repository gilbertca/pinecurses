import math
from pycurses_object import PycursesObject
from base_item import BaseItem
from utils import log


class BaseView(PycursesObject):
	"""
	The base View class which controls all items of a Pycurses program.
	"""
	def __init__(self, parent_controller_instance, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		# Assign parent:
		self.controller = parent_controller_instance
