from collections import Counter
from functools import reduce
from itertools import chain
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

DIR = os.path.dirname(__file__)

try:
    tree = ET.parse(f'{DIR}/posts.xml')
    logger.info('File uploaded successfully')
except Exception as err:
    logger.error(err)
    raise err

root = tree.getroot()

def chunkify(iter, len_chunk):
    """Itera desde un cierto rango hasta el total del tamaño del chunk

    Args:
        iter (xml): Árbol de elemento raíz del archivo xml.
        len_chunk (int): Longitud del chunk

    Yields:
        xml: Devuelve un chunk de una determinada longitud
    """
    for i in range(0, len(iter), len_chunk):
        yield iter[i:i + len_chunk]

def reducer(cnt1, cnt2):
    """Compara elementos de una secuencia.

    Args:
        cnt1 (tuple): Primer elemento a comparar
        cnt2 (tuple: Segundo elemento a comparar

    Returns:
        tuple: Elemento actualizado.
    """
    cnt1.update(cnt2)
    return cnt1

# Top 10 fechas con menor cantidad de post creados.
def get_dates(data):
    return data.attrib['CreationDate'][:10]

def mapper_dates(dates):
    mapped_dates = list(map(get_dates, dates))
    return Counter(mapped_dates)

def dates_with_fewer_posts():
    """Realiza un map-reduce de los posts creados en cada fecha.

    Returns:
        list: Devuelve una lista de tuplas con las 10 fechas con menos posts creados.
    """
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper_dates, data_chunks))
    reduced = reduce(reducer, mapped)
    return reduced.most_common()[-11:-1:]

# Top 10 palabras mas nombradas en los posts.
def clean_text(data):
    soup = BeautifulSoup(data, 'lxml')
    text = soup.get_text()
    text = re.sub(r'[\n|.|,|?|¿|¡|!|(|)|-|/|\|:]', ' ', text).lower()
    return text.split()

def get_words(data):
    return data.attrib['Body']

def mapper_words(data):
    mapped_words = list(map(get_words, data))
    data_clean = list(map(clean_text, mapped_words))
    flatten_data = chain(*data_clean)
    return Counter(flatten_data)

def top_ten_words_in_posts():
    """Realiza un map-reduce de las palabras nombradas en los posts.

    Returns:
       list: Devuelve una lista de tuplas con las 10 palabras más nombradas en los posts..
    """
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper_words, data_chunks))
    reduced = reduce(reducer, mapped)
    return reduced.most_common(10)

if __name__ == '__main__':
    print('Top 10 fechas con menor cantidad de post creados:\n', dates_with_fewer_posts())
    print('Top 10 palabras mas nombradas en los posts:\n', top_ten_words_in_posts())

