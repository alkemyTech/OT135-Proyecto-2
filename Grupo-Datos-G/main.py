import logging
from logging import config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)

logger = logging.getLogger('__name__')


logger.info('This is info')
logger.warning('This is warning')
logger.error('This is error')