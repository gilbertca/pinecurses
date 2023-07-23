from pycurses_object import PycursesObject
from logger import log, log_t


class BaseItem(PycursesObject):
	"""
	The base Item which determines how strings / buttons / etc. should be displayed.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.is_drawn = False
		self.height = 0
		self.width = 0
		self.display_dictionary = {}
	def OnClick(self):
		log_t('Clicked')
	def get_display_string_iterable(self):
		"""
		Returns and formats self.attributes('display_string'),
			i.e. the text which is displayed by any view.
		Formatting is based on:
			1. Writable width
			2. Controller specific tests
		This code currently just returns a string within the width of the View's window.
		"""
		writable_width = self.parent.get_writable_width()
		display_string = self.attributes('display_string')
		display_string_iter = display_string.split('\n')
		truncation_character = self.attributes('truncation_character')
		return_iterable = []
		for iter_string in display_string_iter:
			# If whole string fits on a line:
			if len(iter_string) <= writable_width:
				return_iterable.append(iter_string)
			# Otherwise, if string is longer than width,
			#	And a truncation character is present:
			elif truncation_character:
				return_iterable.append((iter_string[:writable_width-1] + truncation_character))
			# Otherwise just return the string at length.
			else:
				return_iterable.append(iter_string[:writable_width])
		# And return the list of strings:
		return return_iterable

	def initialize(self, parent_view_instance):
		"""
		Sets attributes for the ItemInstance once all
			objects have been created.
		"""
		self.parent = parent_view_instance
