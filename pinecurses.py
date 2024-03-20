import curses
import logging
from logger import log
from parsers.json_parser import JsonParser
class Pinecurses():
	"""The Pinecurses object is the highest level Pinecurses object. It is intended to wrap a *Pine tree*, pass control to the Trunk of the interface, and to interact with curses allowing for curses-agnostic *Pine tree* object classes.

	:param styles_directory_name: The string name of the base 'styles' directory (typically ./styles/)
	:type styles_directory_name: str
	:param refresh_time: The amount of time used with curses.halfdelay; the screen will wait for input that amount of time before refreshing.
	:type refresh_time: int
	"""
	log_level = logging.DEBUG
	def __init__(self, styles_directory_name, file_type, base_class_style_filename='base', refresh_time=5, *args, **kwargs):
		logging.basicConfig(filename='runtime.log', filemode='w', level=Pinecurses.log_level)
		self.CLASS_REFERENCES = {} # Dict for name:class references
		self.class_references = lambda name : self.CLASS_REFERENCES.get(name)
		self.parser_dict = { # Enum for parsers
			'json' : JsonParser
		}
		self.parser_instance = self.parser_dict.get(file_type)(styles_directory_name)
		self.styles_directory_name = styles_directory_name
		self.base_class_style_filename = base_class_style_filename
		self.refresh_time = refresh_time

	@log
	def begin(self):
		"""The main method of a PycursesProgram; this method only wraps Pinecurses._begin with curses.wrapper. By using self.begin to wrap self._begin, the functionality of self.begin can be extended by a Pinecurses creator.
		"""
		curses.wrapper(self._begin)

	@log
	def get_style_attributes(self, file_name):
		"""get_style_attributes uses self.parser_instance to read a style file and returns the contents.
		"""
		return self.parser_instance.parse_file(file_name)

	@log
	def _begin(self, stdscr):
		"""_begin is the primary callback used with curses.wrapper. This method is called by Pinecurses.begin.

		:param stdscr: stdscr is the standard curses.Window object created by curses.wrapper, and is passed automatically.
		"""
		# Set up this object's instance variables:
		self.stdscr = stdscr
		# Set up curses parameters:
		curses.halfdelay(self.refresh_time)
		# Create base Pinecurses objects:
		base_class = self.BaseClassReference(pinecurses_instance=self, style_filename=self.base_class_style_filename, window=self.stdscr)
		while True:
			# Draw everything which needs to be drawn:
			base_class.draw()
			# Get the keypress from a child window:
			keypress_integer = base_class.window.getch()
			keypress_response = None
			# If keypress < 0, then no key was pressed, and the program can idle
			if keypress_integer >= 0:
				keypress_response = base_class.interact(keypress_integer)
			# Check to end program:
			if keypress_response == 0:
				return base_class.clean_up()

