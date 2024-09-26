import json
import tomllib

def parse_json(file_name):
	with open(file_name) as file:
		return json.load(file)

def parse_toml(file_name):
	with open(file_name) as file:
		return toml.load(file)

def parse_file(file_name, file_type):
	"""**parse_file** returns structured data from a file for Pinecurses.

	**parse_file** will match **file_type** to a deserialization function.
	The file will be parsed by the function and the data will be returned
	with Python's data types.
	"""
	deserializing_functions = {
		'json': parse_json,
		'toml': parse_toml,
	}
	deserializer = deserializing_function.get(file_type)
	if deserializer is None: # Unsupported file format
		if file_type.startswith('.'):
			error_message = "Remove the '.' from file_type and try again."
		else:
			error_message = f"file_type {file_type} is not supported at this time."
		raise ValueError(error_message)
