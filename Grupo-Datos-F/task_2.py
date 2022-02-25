import os
import re
import xml.etree.ElementTree as ET
from collections import Counter
from functools import reduce

DIR = os.path.dirname(__file__)
tree = ET.parse(f'{DIR}/posts.xml')
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

def clean_data(data):
    body = data.attrib['Body']
    body = re.findall('(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))', body) 
    return Counter(body)

def mapper_words(data):
    mapped_words = list(map(clean_data, data))
    reduced_words = reduce(reducer, mapped_words)
    return reduced_words

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

def top_ten_words_in_posts():
    """Realiza un map-reduce de las palabras nombradas en los posts.

    Returns:
       list: Devuelve una lista de tuplas con las 10 palabras más nombradas en los posts..
    """
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper_words, data_chunks))
    reduced = reduce(reducer, mapped)
    return reduced.most_common(10)
