import curses
from base_controller import BaseController

def main(stdscr):
	"""
	The main method to run and test this suite.
	"""
	# Create the controller:
	controller = Controller(stdscr)

if __name__ == "__main__":
	curses.wrapper(main)
