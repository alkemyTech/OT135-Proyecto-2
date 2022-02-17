import logging
from logging.config import fileConfig
import os

fileConfig(os.path.join(os.path.dirname(__file__), 'logging.cfg'))
logger = logging.getLogger(__name__)