import curses
import math
import logging
from argparse import ArgumentParser

# Logging setup:
logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)

class Focusable:
	"""An inheritable abtract class which allows a window object to take focus"""
	pass

class Scrollable:
	"""
	An inheritable abstract class which allows a window object to scroll
	Objects should override the .draw() method
	"""
	pass

def errorh(function):
	"""Decorator to handle simple try/except statements"""
	def errh(*args, **kwargs):
		try:
			function(*args, **kwargs)
		except Error as e:
			logging.warning("Error {e}")
					
	return errh

class ListView:
	"""
	A class to display a curses list given a window/pad object, and a list
	Also accepts several key word parameters
	The object can be created as a list, or as a pad
	Like half, quarter, third, etc.
	Also top, bottom, left right, center
	Width can be a keyword string, or a numeric value
	"""
	def __init__(self, iterable, **atr):
		# Required setup:
		self.iterable = iterable
		self.atr_dict = atr
		self.atr = self.atr_dict.get # use self.atr('key') saving typing .get()
		# Steps to create window:
		self.create_window() # create a pad of fixed dimensions based on string keywords
		# Temporary line:
		stri = f"""Height:{self.height} Width:{self.width}
			Top-Left-Y-X:({self.topy},{self.leftx})
			Bot-Right-Y-X:({self.boty},{self.rightx})"""
		self.iterable = [string.strip() for string in stri.split("\n")]
		# ^Temporary line^
		self.draw_window() # draw text to screen using given colors

	def create_window(self):
		"""Creates a pad or window object based on given parameters"""
		self._calculate_size()
		self._calculate_window_valign()
		self._calculate_window_halign()
		self._define_colors() # init color pairs for use using provided string keywords
		self.screen = curses.newpad(self.height, self.width)

	def draw_window(self):
		"""Draw the contents to self.screen"""
		for n in self.iterable:
			self.screen.addstr(f"{n}\n")
		self.screen.refresh(0, 0, self.topy, self.leftx, self.boty, self.rightx)

	def draw_content(self):
		pass

	def _init_colors():
		# Run curses.init_pair() for all colors
		# This function runs init
		count = 0
		curses.init_pair(1, self.atr('text_color')[0], self.atr('text_color')[1])
	
	def _define_colors(self):
		# Run curses.init_color() for all colors
		pass

	def _map_colors(self):
		# Map all colors to keywords
		# This function
		self.CONSTANTUPTOP
		count = 0
		_color_map = {
			'text' : ,
			'background' : self.text_color
		}
		for color in self.atr_dict: # Loop through self.atr
			if color.contains("color"): # Ensure only grab color arguments
				key = color.split('_')[0]
				value = _color_map.get(key)

	def _calculate_size(self):
		"""Method run by create_window to calculate height and width"""
		height = self.atr('height') if self.atr('height') is not None else -1
		width = self.atr('width') if self.atr('width') is not None else -1
		vborder = self.atr('vborder') if self.atr('vborder') is not None else -1
		hborder = self.atr('hborder') if self.atr('hborder') is not None else -1
		# Height calculations:
		# TODO: Check else statements for truthiness
		if height == -1  and vborder == -1:
			self.height = curses.LINES
		elif height == -1  and vborder >= 0:
			self.height = curses.LINES - (2 * vborder)
		elif height > 0 and vborder == -1:
			self.height = height
		else:
			raise ValueError("Can not define a custom height AND vertical padding or height=0.")
		# Width calculations:
		# TODO: Check else statements for truthiness
		if width == -1 and hborder == -1:
			self.width = curses.COLS
		elif width == -1 and hborder >= 0:
			self.width = curses.COLS - (2 * hborder)
		elif width > 0 and hborder == -1:
			self.width = width
		else:
			raise ValueError("Can not define a custom width AND horizontal borders, or width=0.")

	def _calculate_window_valign(self):
		"""Method run by create_window() to calculate topy and boty for draw_window()"""
		# Note: assignment of -1 is to prevent type errors when comparing int to nonetype
		topy = self.atr('topy') if self.atr('topy') is not None else -1
		boty = self.atr('boty') if self.atr('boty') is not None else -1
		valign = self.atr('valign')
		if topy >= 0 and boty >= 0:
			self.topy = topy
			self.boty = boty
		if valign == 'center' or valign == None:
			center = math.floor(curses.LINES/2) # Always move up 1 from center if odd!
			self.topy = center - math.floor(self.height/2) # Always move up 1!
			self.boty = center + math.ceil(self.height/2) # Always move up 1!
		if valign == 'top':
			self.topy = 0
			self.boty = 0 + self.height - 1
		if valign == 'bottom':
			self.topy = curses.LINES - 1
			self.boty = curses.LINES - self.height

	def _calculate_window_halign(self):
		"""Method run by create_window() to calculate topx and botx for draw_window()"""
		leftx = self.atr('leftx') if self.atr('leftx') is not None else -1
		rightx = self.atr('rightx') if self.atr('rightx') is not None else -1
		halign = self.atr('halign')
		if leftx >= 0 and rightx >= 0:
			self.leftx = leftx
			self.rightx = rightx
		if halign == 'center' or halign == None:
			center = math.floor(curses.COLS/2) # Always move left 1 from center if odd!
			self.leftx = center - math.floor(self.width/2) # Alwas move left 1!
			self.rightx = center + math.ceil(self.height/2) # Always move left 1!
		if halign == 'left':
			self.leftx = 0
			self.rightx = 0 + self.width - 1
		if halign == 'right':
			self.leftx = curses.COLS - 1
			self.rightx = curses.COLS - width

	def close(self):
		"""Close the window"""
		# Does not work!
		pass
		#self.screen.clear()
		#self.screen.refresh()

def main(stdscr):
	"""
	A method for testing the view
	"""
	# Creating bogus data
	iterable = ""
	atrs = {
		'valign' : 'center',
		'halign' : 'center',
		'height' : 20,
		'width' : 20,
		'text_color' : (curses.COLOR_RED, curses.COLOR_BLUE),
		'background_color' : (curses.COLOR_YELLOW, curses.COLOR_BLUE),
	}
	# Running actual code:
	listview = ListView(iterable, **atrs)
	listview.screen.getch()

	"""stdscr.refresh()
	noneview = ListView("NONEVIEW", 
		height=None, width=None,
		valign=None, halign=None,
		back_color=None, fore_color=None,
	)
	noneview.screen.getch()
	stdscr.touchwin()
	stdscr.refresh()
	noneview.screen.getch()"""

	return 0

if __name__ == "__main__":
	curses.wrapper(main)
	print("Success!")
