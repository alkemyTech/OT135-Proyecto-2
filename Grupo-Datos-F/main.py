from collections import Counter
from functools import reduce
import logging as log
from logging.config import fileConfig
import os
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

config = os.path.join(os.path.dirname(__file__), 'logging.cfg')
fileConfig(config)

# Devuelve un logger con el nombre especificado
logger = log.getLogger('log for data group F')

# Registra un mensaje con nivel INFO en este logger
logger.info('log by console')

DIR = os.path.abspath('posts.xml')

try:
    tree = ET.parse(DIR)
    logger.info('File uploaded successfully')
except Exception as err:
    logger.error(err)
    raise err

root = tree.getroot()

# Top 10 palabras mas nombradas en los posts.
def clean_text(data):
    soup = BeautifulSoup(data, 'lxml')
    text = soup.get_text()
    text = re.sub(r'[\n|.|,|?|¿|¡|!|(|)|-|/|\|:]', ' ', text).lower()
    return text
    
def count_words(data):
    text_split = data.split()
    return Counter(text_split)

def mapper(data):
    return data.attrib['Body']

def reducer(cnt1, cnt2):
    cnt1.update(cnt2)
    return cnt1

data = list(map(mapper, root))
data_clean = list(map(clean_text, data))
data_count = map(count_words, data_clean)
reduced = reduce(reducer, data_count)

print('Top 10 palabras mas nombradas en los post:')
print(reduced.most_common(10))