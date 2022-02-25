
import logging
from datetime import datetime
import os
import xml.etree.ElementTree as ET
from logging.config import fileConfig
from query1 import query1
from query2 import query2
from query3 import query3

LOGGING_CONF=os.path.join(os.path.dirname(__file__), 'logging.cfg')
fileConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)

try:
    mytree = ET.parse('Grupo-Datos-A/112010 Meta Stack Overflow/posts.xml')
    myroot = mytree.getroot()
except:
    logger.error('Hubo un error parseando el archivo xml')
    raise Exception

start = datetime.now()
print(f'The top 10 tags with most accepted responses are: {query1(myroot)}')
logger.info(f'Consulta 1 finalizada en: {(datetime.now()-start).total_seconds()} segundos')

start = datetime.now()
print(f'The average score per word is equal to: {query2(myroot)}')
logger.info(f'Consulta 2 finalizada en: {(datetime.now()-start).total_seconds()} segundos')

start = datetime.now()
print(f'The average delay in seconds is equal to: {query3(myroot)} hours')
logger.info(f'Consulta 3 finalizada en: {(datetime.now()-start).total_seconds()} segundos')