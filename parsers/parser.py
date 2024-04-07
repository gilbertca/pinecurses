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

