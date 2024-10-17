import os
import curses
from utils.parser import parse_file

class Pinecurses:
	"""**`Pinecurses`** is the object representation of the entire application.

	An instance of **`Pinecurses`** will contain all `curses` related logic.
	This allows other components to be `curses` agnostic,
	and allows the developer to focus on their application's presentation.

	Initialization:
		**template_dir** - The name of the directory containing your templates.
		**template_type** - The name of your serialization language.
		**template_classes** - A dictionary namespace to link templates to custom classes.
		**keybindings** - A dictionary namespace to link keypresses to functions.
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

	def begin(self):
		"""**`begin`** is the primary entry point for a Pinecurses program.

		When executed, **`Pinecurses.begin`** will take control and begin the application.
		**`begin`** wraps `_begin` with `curses.wrapper`
		because we don't want the user making *any* calls to `curses` themselves.

		Remember that we are unable to process dimensions until we are *inside* curses
		because we do not have information about our terminal until then.

		All `curses.window` objects are instantiated before the main loop begins.
		All `window` instances live simultaneously for the duration of the program.
		It is the responsibility of Pinecurses to adaptively hide and display all windows.

		Parameters: None

		Returns: an integer exit code
			0 - The program executed successfully
			1 - The program crashed due to an issue with Pinecurses
			2 - The program crashed due to an issue with custom code
		"""
		curses.wrapper(self._begin)	
	
	def _begin(self, stdscr):
		"""**`_begin`** is to be wrapped by `Pinecurses.begin` with `curses.wrapper`.

		Note: window_list contains Pinecurses objects, not curses.window objects.
		See `Pinecurses.begin` for details and documentation.
		"""
		# Collect all templates:
		template_list = []
		for template_path in os.listdir(self.template_dir):
			template_dictionary = parse_file(template_path, self.template_type)
			template_list.append(template_dictionary)

		# Create Pinecurses objects for all templates.
		# window objects are created by their initialziers.
		template_instance_list = []
		for template in template_list:
			template_class = template.get("class_name")
			template_instance = template_class(**template)
			template_instance_list.append(template_instance)

		# Stuff all of the windows into a panel.
		# Pinecurses can switch between windows by using Panel methods.
		# Data can be selected in a panel with Panel.set_userptr.
		panel_list = []
        for template_instance in template_instance_list:
			new_panel = curses.panel.new_panel(template_instance.window)
			# PC instances must reference their own panel so they can adjust userptr
			pc_instance.new_panel(new_panel)
			panel_list.append(new_panel)
		
		# Main loop:
		while True:
			# The window is drawn and *undrawn* at this point
			for window in window_list:
				if window.is_drawn:
					window.draw()
				if not window.is_drawn:
					window.clear()
			# Windows should call noutrefresh on themselves... always.
			curses.doupdate()

			# COLLECT INPUT
			# PROCESS INPUT
			# REPEAT
			break

