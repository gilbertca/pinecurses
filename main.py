import curses
from pycurses_program import PycursesProgram
from base_controller import BaseController
from base_view import BaseView
from base_item import BaseItem

class DevelopmentProgram(PycursesProgram):

	def __init__(self, json_directory, *args, **kwargs):
		super().__init__(self, json_directory, *args, **kwargs)
		self.class_namespace.update({
			'base_controller' : BaseController,
			'base_view' : BaseView,
			'base_item' : BaseItem
		})
		self.initialize()

def main(stdscr):
	"""
	The main method to run and test the suite.
	"""
	program = DevelopmentProgram('./json')
	return program.begin()


if __name__ == "__main__":
	curses.wrapper(main)
