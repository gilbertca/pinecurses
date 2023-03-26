import math
import curses
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

	def set_background(self):
		"""
		Sets the background attributes of the screen.
		"""
		pass

	def _calculate_helper(self, atr_dict):
		"""
		Method which takes an *atr_dict*, iterates, runs the lambda function,
			and returns the final attribute.
		"""
		for atr_key in atr_dict: # Iterate
			attribute = self.atr(atr_key) # Actual attribute value
			if attribute: # Call the given height function with the attribute:
				return atr_dict.get(atr_key)(attribute)
		default_method = atr_dict.get('default')
		if default_method:
			return default_method()
		raise AttributeError(f"_calculate_helper was unable to find a required attribute or default value. Attribute dict: - {atr_dict} -"

	def _calculate_height(self):
		"""
		Method which calculates and returns the value for self.height
		"""
		# Namespace for attributes related to height:
		height_atr_namespace = {
			'height' : lambda height_int : height_int, # Simple height
			'vborder' : lambda vborder_int : self.window.getmaxyx()[0] - (2 * vborder), # Cells from vertical edge to content.
			'vpercent' : lambda vpercent_int : math.floor(self.window.getmaxyx()[0] * vpercent_int / 100), # Percent of window height.
			'default' : lambda : self.window.getmaxyx()[0],
		}
		calculated_value = _calculate_helper(height_atr_namespace)
		self.height = calculated_value

	def _calculate_width(self):
		"""
		Method which calculates and returns the value for self.width
		"""
		# Namespace for attributes related to width:
		width_atr_namespace = {
			'height' : lambda width_int : width_int, # Simple width
			'hborder' : lambda hborder_int : self.window.getmaxyx()[1] - (2 * hborder), # Cells from horizontal edge to content.
			'hpercent' : lambda hpercent_int : math.floor(self.window.getmaxyx()[1] * hpercent_int / 100), # Percent of window width.
		}
		try: # Error results in default width being whole window.
			calculated_value = _calculate_helper(width_atr_namespace)
		except AttributeError: # AttributeError thrown when no attribute from the namespace could be found.
			calculated_value = self.window.getmaxyx()[1]
		self.width = calculated_value

