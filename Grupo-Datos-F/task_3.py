import os
import xml.etree.ElementTree as ET
from datetime import datetime
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
        datetime: Tiempo promedio de respuesta.
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

    times_100_200 = reduce(time_reducer, times)
    avg_time_100_200 = times_100_200/len(times)
    return avg_time_100_200
