import curses
#from listview import ListView
#from gameview import GameView, InventoryView
from textview import TextView
from controller import Controller
from utils import parse_json

JSON_FILE1 = "json/textview.json"
JSON_TEXT = "json/texttext.json"
def main(stdscr):
	"""
	A method for testing the view
	"""
	# Required:
	controller = Controller(stdscr)
	# Arbitrary data:
	view_name = "text_view"
	view_atr = parse_json(JSON_FILE1)
	view_text = parse_json(JSON_TEXT)
	# To draw views:
	controller.create_view(view_name, view_atr, TextView, view_text)
	# Program ends upon returning 0:
	return controller.begin()

if __name__ == "__main__":
	curses.wrapper(main)
