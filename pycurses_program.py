import curses

class PycursesProgram():
	
	def __init__(self, json_directory, *args, **kwargs):
		self.class_namespace = {}
		self.json_directory = json_directory

	def load_objects(self, json_directory):
		"""
		Creates a PycursesParser instance and requests a dictionary
			of name:PycursesObjectInstance pairs created by the
			PycursesParser from the provided json_directory.
		"""
		self.object_dict = parse_json_folder(self.class_namespace, self.json_directory)

	def begin(self):
		"""
		The main method of a PycursesProgram, which must be called as:
		return *Program.begin()
		This will read all JSON files and create the corresponding PycursesObjects,
		Initialize the proper relationships between classes,
		Pass control to a Controller and return its interact method.
		"""
		curses.wrapper(self._begin)

	def _begin(self, stdscr):
		"""
		_begin is the primary callback used by PycursesProgram.begin(..).
		The 'begin' function only wraps the '_begin' function with
			'curses.wrapper'.
		"""
		self.stdscr = stdscr
