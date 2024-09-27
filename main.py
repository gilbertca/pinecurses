from pinecurses import Pinecurses

def main():
	"""
	The main method to run and test the suite.
	"""
	template_dir_name = './templates'
	template_file_type = 'json'
	custom_template_classes = {}
	custom_keybindings = {}
	program = Pinecurses(
			template_dir_name,
			template_file_type,
			template_classes=custom_template_classes,
			keybindings = custom_keybindings,
			)
	program.begin()


if __name__ == "__main__":
	main()
