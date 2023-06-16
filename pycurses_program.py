from utils import parse_json_folder

class PycursesProgram():
	
	def __init__(self, *args, **kwargs):
		self.class_namespace = {}

	def initialize(self, json_directory):
		"""
		Must be run by the child PycursesProgram class,
			due to self.class_namespace not containing anything during
			self.__init__(..).
		"""
		self.object_dict = parse_json_folder(self.class_namespace, json_directory)

	def begin(self):
		"""
		Passes control of the program to the Controller.
		"""
		controller = self.object_dict.get('controller')[0]
		return controller.begin(self.object_dict)
