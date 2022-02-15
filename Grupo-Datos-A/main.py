import logging
from logging.config import fileConfig
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO,
                    format=f"%(asctime)s_[%(levelname)s]_%(name)s_%(message)s",
                    datefmt='%d-%m-%Y')


def get_file_handler():
    file_handler = TimedRotatingFileHandler(filename="weekly_rotating.log",
                                            when="W0"
                                            )
    file_handler.setLevel(logging.INFO)
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger


logger = get_logger(__name__)
logger.info('Ejemplo')
