
import logging
from logging.config import fileConfig
import os

LOGGING_CONF=os.path.join(os.path.dirname(__file__), 'logging.cfg')
fileConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)
#logger.info('hello world')
