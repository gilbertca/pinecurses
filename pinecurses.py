import curses
import logging
from trunk import Trunk
from branch import Branch
from leaf import Leaf
from logger import log
from parsers.json_parser import JsonParser

class Pinecurses():
	"""The Pinecurses object is the highest level Pinecurses object. It is intended to wrap a *Pine tree*, pass control to the Trunk of the interface, and to interact with curses allowing for curses-agnostic *Pine tree* object classes.

	:param: style_directory

	"""
	def __init__(self, style_directory, ParserClass=JsonParser, *args, **kwargs):
		logging.basicConfig(filename='runtime.log', filemode='w', level=logging.DEBUG)
		self.class_namespace = {
			'trunk' : Trunk,
			'branch' : Branch,
			'leaf' : Leaf,
		}
		self.style_directory = style_directory
		self.ParserClass = ParserClass

	@log
	def load_objects(self, directory):
		"""
		Creates a PycursesParser instance and requests a dictionary
			of name:PycursesObjectInstance pairs created by the
			PycursesParser from the provided directory.
		"""
		parser = self.ParserClass(directory)
		self.pinecurses_objects_dict = parser.parse(self.class_namespace)

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
		self.load_objects(self.style_directory)
