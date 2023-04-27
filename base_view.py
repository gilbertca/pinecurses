import curses
import math
from pycurses_object import PycursesObject
from utils import log


class BaseView(PycursesObject):
	"""
	The base View class which controls all items of a Pycurses program.
	"""
	super().__init__(self, parent_controller_instance, *args, **kwargs)
	self.controller = parent_controller_instance
