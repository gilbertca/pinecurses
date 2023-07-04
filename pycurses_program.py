import curses
import logging
from logger import log
from parsers import JsonParser

class PycursesProgram():
	
	def __init__(self, json_directory, *args, **kwargs):
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		self.class_namespace = {}
		self.json_directory = json_directory

	@log
	def load_objects(self, json_directory):
		"""
		Creates a PycursesParser instance and requests a dictionary
			of name:PycursesObjectInstance pairs created by the
			PycursesParser from the provided json_directory.
		"""
		parser = JsonParser(json_directory)
		self.pycurses_objects_dict = parser.parse(self.class_namespace)

	@log
	def begin(self):
		"""
		The main method of a PycursesProgram, which must be called as:
		return *Program.begin()
		This will read all JSON files and create the corresponding PycursesObjects,
		Initialize the proper relationships between classes,
		Pass control to a Controller and return its interact method.
		"""
		curses.wrapper(self._begin)

	@log
	def _begin(self, stdscr):
		"""
		_begin is the primary callback used by PycursesProgram.begin(..).
		The 'begin' function only wraps the '_begin' function with
			'curses.wrapper'.
		"""
		self.stdscr = stdscr
		self.load_objects(self.json_directory)
