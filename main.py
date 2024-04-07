from pinecurses import Pinecurses

def main():
	"""
	The main method to run and test the suite.
	"""
	program = Pinecurses(styles_directory_name='./json_styles', file_type='json')
	program.CLASS_REFERENCES.update({
	})
	program.begin()


if __name__ == "__main__":
	main()
