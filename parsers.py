import json
import os

class Parser:
	
	def __init__(self, base_directory, *args, **kwargs):
		self.base_directory = base_directory

	def parse(self, class_namespace):
		"""
		parse returns a dictionary containing name:PycursesObjects.
		"""
		pycurses_objects_dict = {}
		directory_list = os.listdir(self.base_directory)
		# NOTE: Directory name must match the name associated
		#	with the corresponding class!
		for current_directory_name in directory_list:
			class_reference = class_namespace.get(current_directory_name)
			filenames_list = os.listdir(f"{self.base_directory}/{current_directory_name}")
			pycurses_objects_list = self._create_objects_from_namespace(
				ClassReference, filenames_list, current_directory_name
			)
			pycurses_objects_dict.update({current_directory_name:pycurses_objects_list})
		return pycurses_objects_dict

	def _create_objects_from_namespace(self, ClassReference, filenames_list, current_directory_name):
		"""
		Helper method which returns a list of objects created from a given ClassReference.
		The attributes for each created object are read from the file_list
			in the given current_directory_name.
		"""
		pycurses_objects_list = []
		for filename in filenames_list:
			class_attributes = parse_file(f"{self.base_directory}/{current_directory_name}/{filename}")
			PycursesClass = ClassReference(**class_attributes)
			pycurses_objects_list.append(PycursesClass)
		return pycurses_objects_list

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
		return parse_json(file_name)

	def parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file, returns a dict object.
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data
