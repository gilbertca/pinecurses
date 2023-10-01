import json
import os

class Parser:
	
	def __init__(self, base_directory, *args, **kwargs):
		self.base_directory = base_directory

	def parse(self, class_namespace):
		"""
		parse returns a dictionary containing name:PycursesObjects.
		"""
		pinecurses_objects_dict = {}
		directory_list = os.listdir(self.base_directory)
		# NOTE: Directory name must match the name associated in Pinecurses.class_namespace
		for current_directory_name in directory_list:
			ClassReference = class_namespace.get(current_directory_name)
			filenames_list = os.listdir(f"{self.base_directory}/{current_directory_name}")
			pinecurses_objects_list = self._create_objects_from_namespace(
				ClassReference, filenames_list, current_directory_name
			)
			pinecurses_objects_dict.update({current_directory_name:pinecurses_objects_list})
		return pinecurses_objects_dict

	def _create_objects_from_namespace(self, ClassReference, filenames_list, current_directory_name):
		"""
		Helper method which returns a list of objects created from a given ClassReference.
		The attributes for each created object are read from the file_list
			in the given current_directory_name.
		"""
		pinecurses_objects_list = []
		for filename in filenames_list:
			class_attributes = self.parse_file(f"{self.base_directory}/{current_directory_name}/{filename}")
			PycursesClass = ClassReference(**class_attributes)
			pinecurses_objects_list.append(PycursesClass)
		return pinecurses_objects_list

	def parse_file(self, *args, **kwargs):
		"""
		This function is to be overloaded by a child class,
			and is to return the contents of a file in the form
			of a dictionary containing name:attribute pairs.
		"""
		raise Exception("This method must be overloaded by a child class.")

