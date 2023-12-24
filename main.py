from pinecurses import Pinecurses
from parsers.json_parser import JsonParser
from example import ExampleTrunk

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses(styles_directory_name='./styles', BaseClassReference=ExampleTrunk, ParserClassReference=JsonParser)
	program.begin()


if __name__ == "__main__":
	main()
