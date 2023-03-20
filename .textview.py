from baseview import AbstractBaseView

class TextView(AbstractBaseView):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def draw_window(self, *args, **kwargs):
		pass
