import xml.etree.ElementTree as ET
from functools import reduce
from datetime import datetime

'''
Script que devuelve:
- Tiempo de respuesta promedio en top 0-100 post con mayor puntaje 
'''

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def id_score_dates(data):
    '''
    Me quedo con los id de los post donde PostTypeId = 1 (preguntas)
    El score para calcular el top 0-100
    La fecha de creacion
    '''    
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

def formatear_fecha_1(data):
    '''
    Transformo la fecha de creacion de string a tipo fecha
    '''
    return data[0], data[1], datetime.strptime(data[2], '%Y-%m-%dT%H:%M:%S.%f')

def formatear_fecha_2(data):
    '''
    Transformo la fecha de creacion de string a tipo fecha
    '''    
    return data[0], datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%S.%f')

def reducer_1(data1, data2):
    data1 = data1 + data2
    return data1

def mapper_1(data):
    '''
    Obtengo la información de los post pregunta y
    convierto a formato fecha
    '''
    post_type_1 = list(map(id_score_dates, data))
    post_type_1 = list(filter(None, post_type_1))
    post_type_1 = list(map(formatear_fecha_1, post_type_1))
    return post_type_1

def mapper_2(data):
    '''
    Obtengo la información de los post respuesta y
    convierto a formato fecha
    '''
    post_type_2 = list(map(parentid_dates, data))
    post_type_2 = list(filter(None, post_type_2))
    post_type_2 = list(map(formatear_fecha_2, post_type_2))
    return post_type_2

def reducer2(data1, data2):
    '''
    Obtiene los tiempos de respuesta comparando 
    los id de las preguntas con el parent id de las respuestas
    '''
    for elem in type1_reduced:
        for i in data1:
            while elem[0] == i[0]:
                time = i[1] - elem[2]
                times.append(time)
                break
    data1 = data2
    return data1

def time_reducer(time1, time2):
    '''
    Suma todos los tiempos de respuesta en uno
    '''
    time1 = time1 + time2
    return time1

def average_response():
    '''
    Ejecuta la tarea 3:
    Devuelve el tiempo promedio de respuesta en el top 200-300 de preguntas
    '''
    tree = ET.parse(r"posts.xml")
    root = tree.getroot()
    data_chunks = chunkify(root, 50)

    global type1_reduced, times
    #Preguntas: Top 0-100 ordenadas por score    
    mapped_1 = list(map(mapper_1, data_chunks))
    type1_reduced = reduce(reducer_1, mapped_1)
    type1_reduced = sorted(type1_reduced, key=lambda x: x[1], reverse=True)[:100]

    #Respuestas
    data_chunks = chunkify(root, 50)
    mapped_2 = list(map(mapper_2, data_chunks))
    times = []
    reduce(reducer2, mapped_2)
    times_0_100 = reduce(time_reducer, times)
    prom_time_0_100 = times_0_100/len(times)
    return prom_time_0_100