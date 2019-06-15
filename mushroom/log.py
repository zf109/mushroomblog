import logging
from .config import Config as conf

def setuplogger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(conf.LOG_LEVEL)
    logger.addHandler(handler)
    return logger
