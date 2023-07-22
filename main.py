import curses
from pycurses_program import PycursesProgram
from base_controller import BaseController
from base_view import BaseView
from base_item import BaseItem

class DevelopmentProgram(PycursesProgram):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.class_namespace.update({
			'controllers': BaseController,
			'views': BaseView,
			'items': BaseItem,
		})
def main():
	"""
	The main method to run and test the suite.
	"""
	program = DevelopmentProgram('./json')
	program.begin()


if __name__ == "__main__":
	main()
