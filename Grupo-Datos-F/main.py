import logging as log
from logging.config import fileConfig
import os

config = os.path.join(os.path.dirname(__file__),
                        'logging.cfg')
fileConfig(config)
logger = log.getLogger('__name__')
    