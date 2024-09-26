import os
from utils.parser import parse_file

class Pinecurses:
	"""**`Pinecurses`** is the object representation of the entire application.

	An instance of **`Pinecurses`** will contain all `curses` related logic.
	This allows other components to be `curses` agnostic,
	and allows the developer to focus on their application's presentation.

	Initialization:
		template_dir
		template_type
		template_classes
		keybindings
	"""

	def __init__(
			self,
			template_dir,
			template_type,
			template_classes={},
			keybindings = {}
			):
		self.template_dir = template_dir
		self.template_type = template_type
		self.template_classes = {}.update(template_classes)
		self.keybindings = {}.update(keybindings)

	def begin()
		"""**`begin`** is the primary entry point for a Pinecurses application.

		When executed, `Pinecurses.begin` will take control and begin the application.

		Parameters: None

		Returns: an integer exit code
			0 - The program executed successfully
			1 - The program crashed due to an issue with Pinecurses
			2 - The program crashed due to an issue with custom code
		"""
		# Begin by collecting all templates:
		template_list = []
		for template_path in os.listdir(self.template_dir):
			template_dictionary = parse_file(template_path, self.template_type)
			template_list.append(template_dictionary)


