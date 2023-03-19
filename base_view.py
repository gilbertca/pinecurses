from abstract_base_view import AbstractBaseView

class BaseView(AbstractBaseView):
	"""
	The simplest View which may be instantiated.
	Inherits it's attributes from AbstractBaseView.
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
