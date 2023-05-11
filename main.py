import curses
from utils import parse_json_folder 

def main(stdscr):
	"""
	The main method to run and test this suite.
	"""
	object_dict = parse_json_folder('./json')
	print(object_dict)
	# Begin the main loop. Any pycurses program should be relatively this simple.
	#controller.begin()


if __name__ == "__main__":
	curses.wrapper(main)
