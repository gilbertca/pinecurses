from utils import parse_json_folder

class PycursesProgram():
	
	def __init__(self, json_directory, *args, **kwargs):
		self.class_namespace = {}

	def begin(self, class_namespace):
		"""
		Must be run by the child PycursesProgram class,
			due to self.class_namespace not being created during
			self.__init__(..).
		"""
		self.object_dict = 
