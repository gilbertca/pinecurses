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

	def parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file returns a dict object
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data
