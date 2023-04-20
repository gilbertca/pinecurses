from abstract_base_controller import AbstractBaseController
from mixins import FunctionsMixin

class BaseController(AbstractBaseController, FunctionsMixin):
	"""
	The simplest controller which can be instantiated.
	It inherits it's attributes from AbstractBaseController.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = self.atr('name')
		self.VIEWS = {}
		self.views = lambda key : self.VIEWS.get(key)

	def add_view(self, view_instance):
		"""
		Takes a View instance and appends it to self.views.
		"""
		self.VIEWS.update({view_instance.name : view_instance})

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
		for view in self.VIEWS:
			self.draw_view(self.views(view))

	def draw_view(self, view_instance):
		"""
		Draws a view by:
			1. Setting background characteristics
			2. Drawing items iteratively
		"""
		pass
