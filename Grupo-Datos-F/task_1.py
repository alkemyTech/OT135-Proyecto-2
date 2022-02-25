import os
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

def get_dates(data):
    return data.attrib['CreationDate'][:10]

def mapper_dates(dates):
    mapped_dates = list(map(get_dates, dates))
    return Counter(mapped_dates)

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

def dates_with_fewer_posts():
    """Realiza un map-reduce de los posts creados en cada fecha.

    Returns:
        list: Devuelve una lista de tuplas con las 10 fechas con menos posts creados.
    """
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper_dates, data_chunks))
    reduced = reduce(reducer, mapped)
    return reduced.most_common()[-11:-1:]