import logging
from datetime import datetime

# Create a logger for this module
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.DEBUG)

def log(function):
	"""
	Decorator to log info about internal functions and handle errors.
	"""
	def log(*args, **kwargs):
		# Log the function name, arguments, and file
		logger.debug(f"{datetime.now()}\
				\nFunction: {function.__name__}\
				\nArgs: {args}\
				\nKwargs: {kwargs}\
				\nFile: {function.__globals__.get('__file__')}\n")
		try:
			return function(*args, **kwargs)
		except Exception as e:
			# Log the exception
			logger.critical(f"Critical error in function {function.__name__} due to {e}", exc_info=True)
			raise

	return log	  
