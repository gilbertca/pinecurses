import json
import os

class Parser:
	
	def __init__(self, base_directory, *args, **kwargs):
		self.base_directory = base_directory

	def parse(self):
		raise Exception("This method must be overloaded by a child class.")


class JsonParser(Parser):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def parse(self):
		"""
		parse returns a dictionary containing name:PycursesObjects.
		JsonParser uses json.load(..) to read from .json files.
		"""
		pycurses_objects_dict = self.traverse()
		return pycurses_objects_dict

	def _create_objects_from_namespace(self, ClassReference, file_list, current_directory):
		"""
		Helper method which returns a list of objects created from a given ClassReference.
		The attributes for each created object are read from the file_list
			in the given current_directory.
		"""
		pass


	def parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file returns a dict object
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data
