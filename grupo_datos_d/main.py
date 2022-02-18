import logging as log
from logging.config import fileConfig

fileConfig('logging.cfg')
logger = log.getLogger('grupo_d')
 