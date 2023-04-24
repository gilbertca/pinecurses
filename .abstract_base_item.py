class AbstractBaseItem:
	"""
	Highest abstraction of an item.
	Cannot be instantiated;
		use BaseItem instead.
	"""
	def __init__(self, view, file_name=None, *args, **kwargs):
		self.view = view
		if file_name: # If file name is given:
			self.ATR = parse_json(file_name)
		elif kwargs: # If dictionary is given as K/V pairs:
			self.ATR = kwargs
		else: # If no attributes are present:
			raise ValueError("Attributes are required to create a view.")
		# self.atr is shorthand to access self.ATR
		self.atr = lambda key : self.ATR.get(key)
