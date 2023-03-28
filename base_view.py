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
		Method which takes an *atr_dict*, iterates, runs the function,
			and returns the final attribute.
		EX: {'key' : callback}
		If a keyword is found this method will run the associated function
			with an attribute from self.ATR,
			otherwise it will call the 'default' function with no arguments.
		"""
		for atr_key in atr_dict: # Iterate
			attribute = self.atr(atr_key) # Actual attribute value
			if attribute: # Call the given function with the attribute:
				return atr_dict.get(atr_key)(attribute)
		default_method = atr_dict.get('default')
		if default_method:
			return default_method()
		raise AttributeError(f"_calculate_helper was unable to find a required attribute or default value. Attribute dict: - {atr_dict} -"

	def _calculate_height(self):
		"""
		Method which calculates and assigns the value for self.height
		"""
		# Namespace for attributes related to height:
		height_atr_namespace = {
			'height' : lambda height_int : height_int, # Simple height
			'vborder' : lambda vborder_int : self.window.getmaxyx()[0] - (2 * vborder), # Cells from vertical edge to content.
			'vpercent' : lambda vpercent_int : math.floor(self.window.getmaxyx()[0] * vpercent_int / 100), # Percent of window height.
			'default' : lambda : self.window.getmaxyx()[0], # Default is full width
		}
		calculated_value = _calculate_helper(height_atr_namespace)
		self.height = calculated_value

	def _calculate_width(self):
		"""
		Method which calculates and assigns the value for self.width
		"""
		# Namespace for attributes related to width:
		width_atr_namespace = {
			'height' : lambda width_int : width_int, # Simple width
			'hborder' : lambda hborder_int : self.window.getmaxyx()[1] - (2 * hborder), # Cells from horizontal edge to content.
			'hpercent' : lambda hpercent_int : math.floor(self.window.getmaxyx()[1] * hpercent_int / 100), # Percent of window width.
			'default' : lambda : self.window.getmaxyx()[1], # Default is full width
		}
		calculated_value = _calculate_helper(width_atr_namespace)
		self.width = calculated_value

	def _calculate_window_y_coords(self):
		"""
		Method which calculates self.topy and self.boty
		"""
		# Callback for valign:
		def valign(attribute):
			"""
			Runs calulations for vertical keyword alignment
			"""
			# Callback for top:
			def top(*args):
				topy = 0
				boty = 0 + self.height -1
				return topy, boty
			# Callback for center:
			def center(*args):
				maxy = self.window.getmaxyx()[0]
				center = math.floor(maxy/2) # Always move up 1 from center if odd!
				topy = center - math.floor(self.height/2) # Always move up 1!
				boty = center + math.ceil(self.height/2) # Always move up 1!
				return topy, boty
			# Callback for bottom:
			def bottom(*args):
				maxy = self.window.getmaxyx()[0]
				topy = maxy - self.height
				boty = maxy - 1
				return topy, boty
			# Vertical alignment namespace:
			valign_namespace = {
				'top' : top, # Window to top
				'center' center, # Window to center
				'bottom' : bottom, # Window to bottom
				'default' : center, # Window to center
			}
			return _calculate_helper(valign_namespace)
		 
		# Callback for given topy value
		def topy_given(self, topy):
			"""
			Runs calculations for a given topy.
			Will create boty from height if only topy is given.
			"""
			boty = self.atr('boty')
			if not boty: # No boty means calculate it:
				boty = topy + self.height
			return topy, boty

		# Namespace for attributes related to vertical alignment:
		# NOTE: CAN TAKE A GIVEN TOPY ONLY, BUT NOT ONLY BOTY
		y_align_namespace = {
			'valign' : valign, # Returns (topy, boty) for screen alignment
			'topy' : topy_given, # Returns (topy, boty) for given topy value
		}
		self.topy, self.boty = _calculate_helper(y_align_namespace)
		
	def _calculate_window_x_coords(self):
		"""
		Method which calculates self.leftx and self.rightx
		"""
		# Callback for halign
		def halign(attribute):
			"""
			Runs calulations for horizontal keyword alignment
			"""
			# Callback for left:
			def left(*args):
				leftx = 0
				rightx = 0 + self.width -1
				return leftx, rightx
			# Callback for center:
			def center(*args):
				maxx = self.window.getmaxyx()[1]
				center = math.floor(maxx/2) # Always move up 1 from center if odd!
				leftx = center - math.floor(self.width/2) # Always move right 1!
				rightx = center + math.ceil(self.width/2) # Always move right 1!
				return leftx, rightx
			# Callback for bottom:
			def right(*args):
				maxx = self.window.getmaxyx()[1]
				leftx = maxx - self.width
				boty = maxx - 1
				return leftx, rightx

		# Horizontal alignment namespace:
		halign_namespace = {
			'left' : left, # Window to left
			'center' center, # Window to center
			'right' : right, # Window to right
			'default' : center, # Window to center
		}
		return _calculate_helper(halign_namespace)

		# Callback for a given leftx value
		def leftx_given(self, leftx):
			rightx = self.atr('rightx')
			if not rightx:
				rightx = leftx + self.width
			return leftx, rightx

		# Namespace for attributes related to vertical alignment
		x_align_namespace = {
			'halign' : halign,
			'leftx' : leftx_given,
		}
		self.leftx, self.rightx = _calculate_helper(x_align_namespace)

    def _calculate_padding(self):
        """
        Figures and assigns hpadding and ypaddinng values
        """
        def asym_padding(*args):
            """
            Calculates and returns padding if xpadding or ypadding is used.
            """
            ypadding = self.atr('ypadding')
            xpadding = self.atr('xpadding')
            if not ypadding:
                ypadding = 0
            if not xpadding:
                xpadding = 0
            return ypadding, xpadding
            
        padding_namespace = {
            'padding' : lambda padding : (padding, padding),
            'xpadding' : asym_padding,
            'ypadding' : asym_padding,
            'default' : lambda : (0, 0),
        }
        self.ypadding, self.xpadding = _calculate_helper(padding_namespace)

    def create_curses_pad(self):
        """
        After all 'calculate' methods are called, this method
            can create a curses pad instance.
        """
        self.window = curses.newpad(self.height, self.width)
