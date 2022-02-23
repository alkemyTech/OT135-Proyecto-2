
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

mytree = ET.parse('Grupo-Datos-A/112010 Meta Stack Overflow/posts.xml')
myroot = mytree.getroot()

start = datetime.now()
print(f'The top 10 tags with most accepted responses are: {query1(myroot)}')
print((datetime.now()).total_seconds()-start)
start = datetime.now()
print(f'The average score per word is equal to: {query2(myroot)}')
print((datetime.now()).total_seconds()-start)
start = datetime.now()
print(f'The average delay in seconds is equal to: {query3(myroot)}')
print((datetime.now()).total_seconds()-start)