import json
import os
from base_controller import BaseController
from base_view import BaseView
from base_item import BaseItem

def parse_json(file_name):
	"""
	Simple utility to read from a JSON file returns a dict object
	"""
	with open(file_name) as json_file:
		data = json.load(json_file)
	return data

def parse_json_folder(base_directory):
	"""
	Takes a directory within ./ named 'json'
		and programmatically parses the json files within
		each nested folder. 
	The structure for a basic pycurses program is as such:
		./json/ -
			controllers/ -
				controller.json
			views/ -
				view.json
			items/ -
				item.json
	This utility will traverse these directories
		and create corresponding PycursesObjects for
		each json file.
    Uses os.walk to traverse the file tree.
	"""
	def create_objects(base_directory, json_file_list, ClassReference):
		"""
		Takes a list of files, and a reference to a class definition.
		Returns a list containing instantiated instances of the
			ClassReference for each json file.
		"""
		return_object_list = []
		for json_file in json_file_list:
			kwargs = parse_json(f"{base_directory}/{json_file}")
			new_object = ClassReference(**kwargs)
			return_object_list.append(new_object)
		return return_object_list

	# The class_namespace links the name of the	different classes 
	#	with class references to which the attributes in the 
	#	json files are passed for object instantiation.
	class_namespace = {
		'controllers' : BaseController,
		'views' : BaseView,
		'items' : BaseItem,
	}
	# Begin iterating through file structure:
	return_objects_dict = {}
	for walk in os.walk(base_directory):
		current_dir_name = walk[0] # Name of current dir in the walk
		files_list = walk[2] # List of string file names in current dir
		# Iterate through the name:Class namespace
		for key in class_namespace:
			if key in current_dir_name:
				ClassReference = class_namespace.get(key)
				object_instance_list = create_objects(base_directory, files_list, ClassReference)
				return_objects_dict.update({key : object_instance_list})
	# Return dict structure: {classname : [ClassInstance1, ClassInstance2, ...],}
	return return_objects_dict
