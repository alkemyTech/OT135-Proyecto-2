import logging
import logging.config
import os

DIR = os.path.dirname(__file__)


logging.config.fileConfig(f'{DIR}/logging.cfg')
logger = logging.getLogger('logger_grupo_C')
logger.info('HELLO')