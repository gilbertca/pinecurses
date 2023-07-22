import logging
from datetime import datetime

# Create a logger for this module
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.DEBUG)
def log_t(message):
    with open('LOG.pycurse', 'a') as log_file:
        log_file.write(message + '\n')
def log(function):
    """
    Decorator to log info about internal functions and handle errors.
    """
    def log(*args, **kwargs):
        # Log the function name, arguments, and file
        logger.debug(f"{datetime.now()} Function: {function.__name__} Args: {args} Kwargs: {kwargs} File: {function.__globals__.get('__file__')}")
        try:
            return function(*args, **kwargs)
        except Exception as e:
            # Log the exception
            logger.critical(f"Critical error in function {function.__name__} due to {e}", exc_info=True)
            raise

    return log
