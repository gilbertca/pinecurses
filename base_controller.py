from abstract_base_controller import AbstractBaseController
from mixins import FunctionsMixin

class BaseController(AbstractBaseController, FunctionsMixin):
	"""
	The simplest controller which can be instantiated.
	It inherits it's attributes from AbstractBaseController.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.VIEWS = {}
		self.views = lambda key : self.VIEWS.get(key)

	def add_view(self, view_instance):
		"""
		Takes a View instance and appends it to self.views.
		"""
		self.VIEWS.update({view_instance.atr('name') : view_instance})

	def remove_view(self, view_instance):
		"""
		Takes a View instance and removes it from self.VIEWS.
		"""
		self.VIEWS.pop(view_instance.name)

	def draw_all_views(self):
		"""
		Draws all views in self.VIEWS by calling self.draw_view iteratively.
		"""
		# Iterate through dictionary:
		for view_key in self.VIEWS:
			view_instance = self.views(view_key)
			# Run self.draw_view(..) on all view_instance's:
			self.draw_view(view_instance)

	def draw_view(self, view_instance):
		"""
		Draws a view by:
			1. Setting background characteristics
			2. Drawing items iteratively	
		"""
		# Y, X values are relative to the window,
		# 	so we are able to start calculations at 0 + C.
		view_instance.window.addstr(

	def draw_item(self, item_instance):
		"""
		Draws an item by:
			1. Getting the current View's line the Item will be added to
			2. Getting the height of the Item (i.e. number of vertical lines)
			3. Getting the width of the Item (i.e. number of characters in a line)
			4. Determine if the View can fit the Item vertically:
				No: Determine vertical truncation, if any, if applicable
			5. Determine if View can fit the Item horizontally:
				No: Determine horizontal truncation, if any, if applicable

		"""

