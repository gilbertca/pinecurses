import logging
from logger import log
from utils import parse_json_folder

class PycursesProgram():
	
	def __init__(self, json_directory, *args, **kwargs):
		self.class_namespace = {}
		self.json_directory = json_directory

	@log
	def load_objects(self):
		"""
		Reads through
		"""
		self.object_dict = parse_json_folder(self.class_namespace, self.json_directory)

	@log
	def begin(self):
		"""
		The main method of a PycursesProgram, which must be called as:
		return *Program.begin()
		This will read all JSON files and create the corresponding PycursesObjects,
		Initialize the proper relationships between classes,
		Pass control to a Controller and return its interact method.
		"""
		# Read all json, and load into a key-name dictionary:
		pycurses_object_dict = self.load_objects()
		# Once all objects are created, they must be initialized,
		# 	e.g. screen position calculations are run after __init__.
		
		#return controller.begin(self.object_dict)
