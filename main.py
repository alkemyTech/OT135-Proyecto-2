import logging
from logging import config

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('__name__')


logger.info('This is info')
logger.warning('This is warning')
logger.error('This is error')