class AbstractBaseController:
	"""
	The highest abstraction of a Controller.
	Can not be instantiated by itself;
		instead use BaseController.
	"""
	def __init__(self, file_name=None, *args, **kwargs):
		if file_name: # If file name is given:
			self.ATR = parse_json(file_name)
		elif kwargs: # If dictionary is given as K/V pairs:
			self.ATR = kwargs
		else: # If no attributes are present:
			raise ValueError("Attributes are required to create a view.")
		# self.atr is shorthand to access self.ATR
		self.atr = lambda key : self.ATR.get(key)
