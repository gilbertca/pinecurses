import curses
from pycurses_program import PycursesProgram

class DevelopmentProgram(PycursesProgram):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.class_namespace.update({
		
		})

def main():
	"""
	The main method to run and test the suite.
	"""
	program = DevelopmentProgram('./json')
	program.begin()


if __name__ == "__main__":
	main()
