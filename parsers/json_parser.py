from parsers.parser import Parser

class JsonParser(Parser):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def parse_file(self, file_name):
		"""
		Overloaded method which returns the value from parse_json.
		"""
		return self.parse_json(file_name)

	def parse_json(self, file_name):
		"""
		Simple utility to read from a JSON file, returns a dict object.
		"""
		with open(file_name) as json_file:
			data = json.load(json_file)
		return data
