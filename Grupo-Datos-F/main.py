import logging as log
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from functools import reduce
from logging.config import fileConfig

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
def clean_data(data):
    body = data.attrib['Body']
    body = re.findall('(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))', body) 
    return Counter(body)

def mapper_words(data):
    mapped_words = list(map(clean_data, data))
    reduced_words = reduce(reducer, mapped_words)
    return reduced_words

def top_ten_words_in_posts():
    """Realiza un map-reduce de las palabras nombradas en los posts.

    Returns:
       list: Devuelve una lista de tuplas con las 10 palabras más nombradas en los posts..
    """
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper_words, data_chunks))
    reduced = reduce(reducer, mapped)
    return reduced.most_common(10)

# Tiempo de respuesta promedio en top 100-200 score
def id_score_dates(data):
    post_id = data.attrib['PostTypeId']
    score = int(data.attrib['Score'])
    id = data.attrib['Id']
    creation_date = data.attrib['CreationDate']
    if post_id == '1':
        return id, score, creation_date
    else:
        pass

def parentid_dates(data):
    post_id = data.attrib['PostTypeId']
    creation_date = data.attrib['CreationDate']
    #parent_id = data.attrib['ParentId']
    if post_id == '2':
        parent_id = data.attrib['ParentId']
        return parent_id, creation_date
    else:
        pass

def format_date_1(data):
    return data[0], data[1], datetime.strptime(data[2], '%Y-%m-%dT%H:%M:%S.%f')

def format_date_2(data):
    return data[0], datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%S.%f')

def reducer_1(data1, data2):
    data1 = data1 + data2
    return data1

def mapper_1(data):
    post_type_1 = list(map(id_score_dates, data))
    post_type_1 = list(filter(None, post_type_1))
    post_type_1 = list(map(format_date_1, post_type_1))
    return post_type_1

def mapper_2(data):
    post_type_2 = list(map(parentid_dates, data))
    post_type_2 = list(filter(None, post_type_2))
    post_type_2 = list(map(format_date_2, post_type_2))
    return post_type_2

def reducer2(data1, data2):
    """
    Obtiene los tiempos de respuesta comparando los id de las preguntas 
    con el parent id de las respuestas.
    """
    for elem in type1_reduced:
        for i in data1:
            while elem[0] == i[0]:
                time = i[1] - elem[2]
                times.append(time)
                break
    data1 = data2
    return data1

def time_reducer(time1, time2):
    """Suma todos los tiempos de respuesta en uno

    Args:
        time1 (datetime): Fecha
        time2 (datetime): Fecha

    Returns:
        datetime: Fecha
    """
    time1 = time1 + time2
    return time1

def avg_time_100_200():
    """
    Realiza un map-reduce para calcular el tiempo promedio de respuesta 
    en el top 100-200 score.

    Returns:
        str: Tiempo promedio de respuesta.
    """
    global type1_reduced, times
    data_chunks = chunkify(root, 50)
    mapped_1 = list(map(mapper_1, data_chunks))
    type1_reduced = reduce(reducer_1, mapped_1)
    type1_reduced = sorted(type1_reduced, key=lambda x: x[1], reverse=True)[100:200]

    data_chunks = chunkify(root, 50)
    mapped_2 = list(map(mapper_2, data_chunks))

    times = []
    reduce(reducer2, mapped_2)

    avg_time_100_200 = reduce(time_reducer, times)/len(times)
    return avg_time_100_200


if __name__ == '__main__':
    print('Top 10 fechas con menor cantidad de post creados:\n', dates_with_fewer_posts())
    print('Top 10 palabras mas nombradas en los posts:\n', top_ten_words_in_posts())
    print('Tiempo de respuesta promedio en top 100-200 score:\n', avg_time_100_200())

