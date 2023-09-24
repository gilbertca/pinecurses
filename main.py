from pinecurses import Pinecurses

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses('./json')
	program.begin()


if __name__ == "__main__":
	main()
