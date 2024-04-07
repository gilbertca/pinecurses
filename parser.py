import json
import os

class Parser:
	
	def __init__(self, base_directory, *args, **kwargs):
		self.base_directory = base_directory

	def parse_file(self, *args, **kwargs):
		"""
		This function is to be overloaded by a child class,
			and is to return the contents of a file in the form
			of a dictionary containing name:attribute pairs.
		"""
		raise Exception("This method must be overloaded by a child class.")


class JsonParser(Parser):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def parse_file(self, file_name):
		"""
		Overloaded method which returns the value from parse_json.
		"""
		return self._parse_json(file_name)

	def _parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file, returns a dict object.
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data

