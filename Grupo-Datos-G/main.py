import logging
from logging import config
from os import path
import xml.etree.ElementTree as ET
import task_1

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


# Top 10 posts mas vistos
print('Top 10 posts mas vistos: (ID, VISTAS)')
task_1.task_1()

# Top 10 palabras mas nombradas en los post por lenguaje

