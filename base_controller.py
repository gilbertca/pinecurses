from abstract_base_controller import AbstractBaseController

class BaseController(AbstractBaseController):
	"""
	The simplest controller which can be instantiated.
	It inherits it's attributes from AbstractBaseController.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		pass
