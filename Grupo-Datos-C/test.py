import os
import sys
import time
from functools import reduce
from xml.etree.cElementTree import iterparse

from multiprocessing import Pool

from lxml import etree as ET
import lxml.etree

import pandas as pd

start_time = time.time()

DIR = os.path.dirname(__file__)
FILE = f'{DIR}/files/posts.xml'
FILE_LIGHT = f'{DIR}/files/posts_beta.xml'

def add_ranking(key, increment, ranking):
    if key in ranking:
        ranking[key] = ranking[key] + increment
    else:
        ranking[key] = increment
def add_ranking_tuple(key, quantity, amount, ranking):
    if key in ranking:
        ranking[key][0] = ranking[key][0] + quantity
        ranking[key][1] = ranking[key][1] + amount
    else:
        ranking[key] = [quantity, amount]
def reducer(dict1, dict2):
    for element in dict2:
        if element[0] in dict1:
            dict1[element[0]] = dict1[element[0]] + element[1]
        else:
            dict1[element[0]] = element[1]
    return dict1

def chunk_mapper(chunk):
    mapped = map(mapper, chunk)
    reduced = reduce(reducer, mapped)
    return reduced

def mapper(data):
    #  for _, node in iterparse(FILE, events=("end",)):
    ranking_languages = {}
    ranking_favorite_questions = {}
    number_of_words = 0
    views_total = 0
    items = 0
    malformed_elements = 0
    for event, node in data:
        items = items + 1
        if items % 100000 == 0:
            print(f'Procesados {items} elementos')
        row_Id = node.attrib.get("Id")
        is_answer = bool(node.attrib.get("ParentId"))
        if is_answer:
            # This is a answer
            continue
        else:
            # This is a question, get attributes
            has_accepted_answer = node.attrib.get("AcceptedAnswerId")
            languages = node.attrib.get("Tags")
            favorite_count = node.attrib.get("FavoriteCount")
            full_text = node.attrib.get("Body")
            views = node.attrib.get("ViewCount")
            score = node.attrib.get("Score")
            # Bye malformed elements
            if languages is None or favorite_count is None:
                malformed_elements = malformed_elements + 1
                continue
            # Ranking de lenguajes sinn respuestas aceptadas
            languages = languages.replace('><', ';')
            languages = languages.replace('<', '')
            languages = languages.replace('>', '')
            languages = languages.split(';')
            if not(bool(has_accepted_answer)):
                for language in languages:
                    add_ranking(language, 1, ranking_languages)
            # Relaciónh de palabas con visitas
            number_of_words = number_of_words + len(full_text.strip().split(' '))
            views_total = views_total + int(views)
            #  print(f'Pregunta: Respuesta aceptada {has_accepted_answer}, lenguajes {languages} y visitas {views}')
            # Preguntas con favoritos y puntaje
            add_ranking_tuple(int(favorite_count), 1, int(score), ranking_favorite_questions)
            #  print(f'Esto es una respuesta: puntaje {score} y favoritos {favorite_count}')
        node.clear()
    # Ranking de lenguajes sin respuestas
    sorted_ranking_languages = sorted(ranking_languages.items(), key=lambda x: x[1], reverse=True)
    print(sorted_ranking_languages[:20])
    # Relación de visitas y palabras
    print(f'Cantidad de palabras: {number_of_words} y visitas: {views_total}')
    print(f'Su relación es {views_total/number_of_words}')
    # Ranking de respuestas con más favoritos
    # TODO: simplificar la función
    sorted_ranking_favorite_questions = sorted(ranking_favorite_questions.items(), key=lambda x: x[0], reverse=True)
    print(sorted_ranking_favorite_questions[:50])
    # TODO: return something
#  mapper(iterparse(FILE_LIGHT))
# print(f'{time.time() - start_time}')

tree = lxml.etree.parse(FILE_LIGHT)
root = tree.getroot()
if __name__ == '__main__':
    pool = Pool(processes=8)
    pool.map(mapper, root)
