import curses
import logging
from trunk import Trunk
from branch import Branch
from leaf import Leaf
from logger import log
from parsers.json_parser import JsonParser

class Pinecurses():
	"""The Pinecurses object is the highest level Pinecurses object. It is intended to wrap a *Pine tree*, pass control to the Trunk of the interface, and to interact with curses allowing for curses-agnostic *Pine tree* object classes.

	:param style_directory: The string name of the base 'styles' directory (typically ./styles/)
	:type style_directory: str
	:param ParserClass: Reference to a Parser class which will be constructed by Pinecurses
	:type ParserClass: parsers.Parser
	"""
	log_level = logging.DEBUG
	def __init__(self, style_directory, ParserClass=JsonParser, BaseClass=Trunk, *args, **kwargs):
		logging.basicConfig(filename='runtime.log', filemode='w', level=Pinecurses.log_level)
		self.style_directory = style_directory
		self.ParserClass = ParserClass

	@log
	def begin(self):
		"""The main method of a PycursesProgram; this method only wraps Pinecurses._begin with curses.wrapper. By using self.begin to wrap self._begin, the functionality of self.begin can be extended by a Pinecurses creator.
		"""
		curses.wrapper(self._begin)

	@log
	def _begin(self, stdscr):
		"""_begin is the primary callback used with curses.wrapper. This method is called by Pinecurses.begin.

		:param stdscr: stdscr is the standard curses.Window object created by curses.wrapper, and is passed automatically.
		"""
		self.stdscr = stdscr
