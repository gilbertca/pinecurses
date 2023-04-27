import curses
from base_controller import BaseController
from utils import parse_json

CONTROLLER_FILE = "json/controllers/controller.json"
VIEW_FILE = "json/views/view.json"
ITEM_FILE = "json/items/item.json"
def main(stdscr):
	"""
	The main method to run and test this suite.
	"""
	# Create the controller:
	# Controller json files should be relatively sparse.
	controller_kwargs = parse_json(CONTROLLER_FILE)
	controller = BaseController(stdscr, **controller_kwargs)

if __name__ == "__main__":
	curses.wrapper(main)
