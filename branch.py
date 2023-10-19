import math
from baseobject import BaseObject
from mixins.cursormixins import SingleObjectCursor
from mixins.screenpositionmixins import ScreenPositioner
from logger import log


class Branch(SingleObjectCursor, ScreenPositioner, BaseObject):
	"""Branchs are typically the child objects of a Trunk instance. Branches are typically associated with *panes* of content, while the Leaves contained within Branches will contain any displayed content.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)

	@log
	def create_curses_pad(self):
		"""create_curses_pad sets `self.window` to a window object created by `curses.newpad`.
		"""
		self.window = curses.newpad(self.height, self.width)

	@log
	def create_curses_window(self):
		"""create_curses_window sets `self.window` to a window object created by `curses.newwin`.
		"""
		self.window = curses.newwin(self.height, self.width, self.topy, self.leftx)

	@log
	def refresh(self):
		"""
		Refreshes self.window.
		"""
		self.window.refresh(*(0, 0, self.topy, self.leftx, self.boty-1, self.rightx-1))@log

