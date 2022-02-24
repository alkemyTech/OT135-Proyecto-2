import re
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Counter

# Top 10 palabras mas nombradas en los post por lenguaje

def chunkify(iterable, len_of_chunk):
    '''Divide un archivo grande en pedazos'''
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


def get_tags_words(data):
    '''Obtiene los tags(lenguajes) y los body. Limpia los body'''
    try:
        tags = data.attrib['Tags']
    except:
        return
    tags = re.findall('<(.+?)>', tags)
    body = data.attrib['Body']
    body = re.findall(
        '(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))', body)
    word_counter = Counter(body)
    return tags, word_counter


def separate_tags_words(data):
    return dict([[tag, data[1].copy()] for tag in data[0]])


def reduce_counter(data1, data2):
    '''Devuelve el contador de palabras por lenguaje'''
    for key, value in data2.items():
        if key in data1.keys():
            data1[key].update(data2[key])
        else:
            data1.update({key: value})
    return data1


def mapper(data):
    mapped_words = list(map(get_tags_words, data))
    mapped_words = list(filter(None, mapped_words))
    words_in_tag = list(
        map(separate_tags_words, mapped_words))
    try:
        reduced = reduce(reduce_counter, words_in_tag)
    except:
        return
    return reduced


def calculate_top_10(data):
    '''Devuelve el top 10 de palabras por lenguaje'''
    return data[0], data[1].most_common(10)


tree = ET.parse(r"posts.xml")
root = tree.getroot()


def task_2():
    '''Ejecuta una consulta que imprime el top 10 de palabras por lenguaje'''
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper, data_chunks))
    mapped = list(filter(None, mapped))
    reduced = reduce(reduce_counter, mapped)
    top_10 = dict(map(calculate_top_10, reduced.items()))
    print(top_10)
