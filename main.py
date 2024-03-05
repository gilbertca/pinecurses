from pinecurses import Pinecurses
from example import ExampleTrunk

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses(styles_directory_name='./styles', BaseClassReference=ExampleTrunk, file_type='json')
	program.begin()


if __name__ == "__main__":
	main()
