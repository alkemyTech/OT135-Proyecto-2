from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


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


def formatear_fecha_1(data):
    return data[0], data[1], datetime.strptime(data[2], '%Y-%m-%dT%H:%M:%S.%f')


def formatear_fecha_2(data):
    return data[0], datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%S.%f')


def reducer_1(data1, data2):
    data1 = data1 + data2
    return data1


def mapper_1(data):
    post_type_1 = list(map(id_score_dates, data))
    post_type_1 = list(filter(None, post_type_1))
    post_type_1 = list(map(formatear_fecha_1, post_type_1))
    return post_type_1


def mapper_2(data):
    post_type_2 = list(map(parentid_dates, data))
    post_type_2 = list(filter(None, post_type_2))
    post_type_2 = list(map(formatear_fecha_2, post_type_2))
    return post_type_2


tree = ET.parse(
    r"/home/lengulian/Escritorio/OT135-Proyecto-2/Grupo-Datos-G/posts.xml")
root = tree.getroot()
data_chunks = chunkify(root, 50)
mapped_1 = list(map(mapper_1, data_chunks))
type1_reduced = reduce(reducer_1, mapped_1)
type1_reduced = sorted(
    type1_reduced, key=lambda x: x[1], reverse=True)[200:300]
# print(len(type1_reduced))
# print(type1_reduced)
data_chunks = chunkify(root, 50)
mapped_2 = list(map(mapper_2, data_chunks))
# print(mapped_2)

times = []

def reducer2(data1, data2):
    for elem in type1_reduced:
        for i in data1:
            while elem[0] == i[0]:
                time = i[1] - elem[2]
                times.append(time)
                break
    data1 = data2
    return data1


reduced_type1_type2 = reduce(reducer2, mapped_2)

def time_reducer(time1, time2):
    time1 = time1 + time2
    return time1

prom_time_200_300 = reduce(time_reducer, times)/len(times)
print(f'El timepo promedio de respuesta en el top 200-300 de preguntas es: {prom_time_200_300}')
