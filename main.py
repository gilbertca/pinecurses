import curses
from base_controller import BaseController
from base_view import BaseView
from base_item import BaseItem
from utils import parse_json

CONTROLLER_FILE = "json/controllers/controller.json"
VIEW_FILE = "json/views/view.json"
ITEM_FILE = "json/items/item.json"
def main(stdscr):
	"""
	The main method to run and test this suite.
	"""
	# Create the Controller:
	controller_kwargs = parse_json(CONTROLLER_FILE) # Controller attributes are usually sparse.
	controller = BaseController(stdscr, **controller_kwargs)
	# Load Views into the Controller:
	view_attributes = parse_json(VIEW_FILE)
	controller.create_view(**view_attributes)
	# Load Items into the View:
	item_attributes = parse_json(ITEM_FILE)
	controller.get('base_view').create_item(**item_attributes)
	"""Now the entire logical structure has been populated.
	It may be wise to automate this process above for production.
	"""
	# We should arrive at a blank screen which clears upon keypress if we reach this point:
	controller.stdscr.getch()


if __name__ == "__main__":
	curses.wrapper(main)
