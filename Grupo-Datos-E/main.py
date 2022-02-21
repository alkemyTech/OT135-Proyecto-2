import logging
from logging.config import fileConfig
import os
from map_functions import top_10_posts, answers_visits

LOGGING_CONF=os.path.join(os.path.dirname(__file__),
                          'logging.ini')
fileConfig(LOGGING_CONF)
logger = logging.getLogger('Grupo-E')

