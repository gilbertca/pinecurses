from pinecurses import Pinecurses
from example import *

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses(styles_directory_name='./styles', file_type='json')
	program.class_references.update({
		'base' : ExampleTrunk,
		'main_window' : ExampleBranch,
		'popup_window' : ExamplePopupBranch,
	})
	program.begin()


if __name__ == "__main__":
	main()
