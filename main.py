from pinecurses import Pinecurses
from example import ExampleTrunk

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses('./styles', BaseClassReference=ExampleTrunk)
	program.begin()


if __name__ == "__main__":
	main()
