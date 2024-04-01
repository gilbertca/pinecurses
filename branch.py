from baseobject import BaseObject
from mixins.cursormixins import SingleObjectCursor
from mixins.screenpositionmixins import ScreenPositioner
from logger import log


class Branch(SingleObjectCursor, ScreenPositioner, BaseObject):
	"""Branchs are typically the child objects of a Trunk instance. Branches are typically associated with *panes* of content, while the Leaves contained within Branches will contain any displayed content.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@log
	def handle_styles(self, **_style_namespace):
		"""Branch.handle_styles creates a window after all other style attributes are handled.
		"""
		style_namespace = {}
		style_namespace.update(_style_namespace)
		super().handle_styles(**style_namespace)
		self.create_curses_window()


	@log
	def create_curses_pad(self):
		"""create_curses_pad sets `self.window` to a window object created by `curses.newpad`.
		"""
		self.window = curses.newpad(self.height, self.width)

	@log
	def create_curses_window(self):
		"""create_curses_window sets `self.window` to a window object created by `curses.newwin`.
		"""
		self.window = self.pinecurses_instance.newwin(self.height, self.width, self.topy, self.leftx)

	@log
	def refresh(self):
		"""
		Refreshes self.window.
		"""
		self.window.refresh(*(0, 0, self.topy, self.leftx, self.boty-1, self.rightx-1))@log

	@log
	def draw(self):
		"""Branch.draw calls Leaf.draw to obtain *drawing instructions*, and then applies them to the screen.
		"""
		for leaf_key in self.children:
			leaf = self.child(child_key)
			leaf_text = leaf.draw()
			self.window.addstr(leaf_text)

