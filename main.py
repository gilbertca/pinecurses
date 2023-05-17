import curses
from utils import parse_json_folder 

def main(stdscr):
	"""
	The main method to run and test this suite.
	"""
	object_dict = parse_json_folder('./json')
	controller = object_dict.get('controllers')[0]
	controller.begin(stdscr, **object_dict)


if __name__ == "__main__":
	curses.wrapper(main)
