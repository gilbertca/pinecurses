import logging
from datetime import datetime

# Create a logger for this module
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.DEBUG)

def log(function):
	"""**log** is a decorator which provides detailed information about the application at runtime.

	It is intended to decorate all methods for all classes involved in the application. 
	Successful usage of the log decorator will provide the developer with a detailed breakdown 
	of all function calls which occurred during the program's life, and a detailed stackstrace
	in the event of errors.

	**log** is not responsible for *handling* any errors. All exceptions should be logged and re-raised.

	Authors:
		@gilbertca
		@amin1029384756
	"""
	def log(*args, **kwargs):
		# Log function name, args and kwargs, and originating functions filename. 
		logger.debug(f"{datetime.now()}\
				\nFunction: {function.__name__}\
				\nArgs: {args}\
				\nKwargs: {kwargs}\
				\nFile: {function.__globals__.get('__file__')}\n")
		try:
			return function(*args, **kwargs)
		except Exception as e:
			# Log the exception and re-raise. We do not need exc_info, since our trace is detailed enough.
			logger.critical(f"Critical error in function {function.__name__} due to {e}", exc_info=False)
			raise

	return log	  
