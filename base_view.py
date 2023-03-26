import math
from abstract_base_view import AbstractBaseView
from mixins import FunctionsMixin
from utils import log

class BaseView(AbstractBaseView, FunctionsMixin):
	"""
	The simplest View which may be instantiated.
	Inherits it's attributes from AbstractBaseView.
	Is based on a window object.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def _calculate_height(self):
		"""
		Method which calculates and returns the value for self.height
		"""
		# Namespace for attributes related to height:
		height_atr_namespace = {
			# Simple height assignment
			'height' : lambda height_int : height_int, 
			# Number of cells between content and edge in y direction
			'vborder' : lambda vborder_int : self.window.getmaxyx()[0] - (2 * vborder),
			# Percent of total window in y direction
			'vpercent' : lambda vpercent_int : math.floor(self.window.getmaxyx()[0] * vpercent_int / 100)
		}
		for atr_key in height_atr_list: # Iterate
			attribute = self.atr(atr_key) # Actual attribute value
			# If attribute exists, call function from namespace:
			if attribute: # Call the given height function with the attribute:
				self.height = height_atr_namespace.get(atr_key)(attribute)

	def _calculate_width(self):
		"""
		Method which calculates and returns the value for self.width
		"""
		pass
