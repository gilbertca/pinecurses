import json
import os

class Parser:
	
	def __init__(self, root_directory, *args, **kwargs):
		self.root_directory = root_directory

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
		return pycurses_objects_dict

	def parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file returns a dict object
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data

	def traverse_directories(self):
		"""
		Uses os.walk to traverse through the root directory
			and 
		"""
		for walk in os.walk(self.root_directory):
		current_dir_name = walk[0] # Name of current directory
		filenames_list = walk[2] # List of file names in the current directory
