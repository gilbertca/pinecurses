from abstract_base_controller import AbstractBaseController
from mixins import FunctionsMixin

class BaseController(AbstractBaseController, FunctionsMixin):
	"""
	The simplest controller which can be instantiated.
	It inherits it's attributes from AbstractBaseController.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		pass
