from abstract_base_view import AbstractBaseView
from mixins import FunctionsMixin
from utils import log

class BaseView(AbstractBaseView, FunctionsMixin):
	"""
	The simplest View which may be instantiated.
	Inherits it's attributes from AbstractBaseView.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def _calculate_height(self):
		"""
		Method which calculates and returns the value for self.height
		"""
		pass

	def _calculate_width(self):
		"""
		Method which calculates and returns the value for self.width
		"""
		pass
