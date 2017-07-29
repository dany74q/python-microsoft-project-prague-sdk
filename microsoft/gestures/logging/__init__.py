import logging


LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def get_logger(name,
		level=logging.INFO,
		handler=logging.FileHandler('prague.txt'),
		formatter=logging.Formatter(LOGGING_FORMAT)):
	logger = logging.getLogger(name)
	logger.setLevel(level)
	handler.setLevel(level)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger
