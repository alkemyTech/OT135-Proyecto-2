import logging
import logging.config
import os
import time
import multiprocessing as mp

import xml.etree.cElementTree as ET  # Supuestamente es más rápido
from functools import reduce
from collections import Counter
from multiprocessing import Pool

DIR = os.path.dirname(__file__)

logging.config.fileConfig(f'{DIR}/logging.cfg')
logger = logging.getLogger('Logger_Grupo_B')
# logger.info('Test message')

FILE = f'{DIR}/posts.xml'
# FILE_LIGHT = f'{DIR}/posts_light.xml'
# FILE_LARGE = f'{DIR}/posts_large.xml'

# start_time = time.time()

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def add_ranking(key, increment, ranking):
    """
    Incrementa valores de un diccionario
    Inputs:
        key, valor de incremento y diccionario
    Output:
        Ninguna, es un procedimento
    """
    if key in ranking:
        ranking[key] = ranking[key] + increment
    else:
        ranking[key] = increment

def add_ranking_tuple(key, quantity, amount, ranking):
    """
    Incrementa valores de un diccionario de listas
    Inputs:
        key, valor de incremento uno, valor de incremento dos y diccionario
    Output:
        Ninguna, es un procedimento
    """
    if key in ranking:
        ranking[key][0] = ranking[key][0] + quantity
        ranking[key][1] = ranking[key][1] + amount
    else:
        ranking[key] = [quantity, amount]

def reducer(list1, list2):
    """
    Función de reducción
    Inputs:
        2 listas, cada lista contiene:
            lista [cantidad de visitas, cantidad de palabras]
            diccionario {'Lenguaje': número de preguntas}
            diccionario de listas {'número_de_favoritos': [cantidad_de_posts, puntaje acumulado]}
    Output:
        lista reducida
    """
    # Sumamos los valores de la lista qe contiene visitas y palabras
    value1 = [0, 0]
    value1[0] = value1[0] + list1[0][0] + list2[0][0]
    value1[1] = value1[1] + list1[0][1] + list2[0][1]

    # Combinamos ambos diccionarios de lenguajes
    counter1 = Counter(list1[1])
    counter2 = Counter(list2[1])
    add_dict = counter1 + counter2
    dict2 = dict(add_dict)

    # Combinamos los diccionarios de favoritos
    dict3 = list1[2]
    for element in list2[2]:
        if element in dict3:
            dict3[element][0] = dict3[element][0] + list2[2][element][0]
            dict3[element][1] = dict3[element][1] + list2[2][element][1]
        else:
            dict3[element] = list2[2][element]
    return [value1, dict2, dict3]

def chunk_mapper(chunk):
    mapped = map(mapper, chunk)
    reduced = reduce(reducer, mapped)
    return reduced

def mapper(data):
    """
    Función de mapeo
    Inputs:
        Conjunto de datos
    Output:
        Lista con los datos mapeados
            [cantidad de vsitas. cantidad de palabras]
            {'Lenguaje': número de preguntas}
            {'número_de_favoritos': [cantidad_de_posts, puntaje acumulado]}

    """
    list_words_value = list(map(get_word_value, data))  # Mapeamos la función a los datos
    list_words_value = [i for i in list_words_value if i != [0, 0]]  # Quitamos valores de posts mal formados
    words_value = [0, 0]
    # Sumamos las cantidades de los elementos de la lista
    for element in list_words_value:
        words_value[0] = words_value[0] + element[0]
        words_value[1] = words_value[1] + element[1]

    list_top_languages = list(map(get_top_languages, data))  # Mapeamos la función a los datos
    list_top_languages = [x for x in list_top_languages if x]  # Quitamos valores de posts mal formados

    ranking_languages = {}
    # Recorremos la "lista de listas de lenguajes" y vamos añadiéndolas al diccionario
    for list_language in list_top_languages:
        for language in list_language:
            add_ranking(language, 1, ranking_languages)

    list_favorite_questions = list(map(get_favorite_questions, data))  # Mapeamos la función a los datos
    list_favorite_questions = [i for i in list_favorite_questions if i != [0, 0]]  # Quitamos valores de posts mal formados
    # Recorremos la lista y vamos añadiéndolas al diccionario
    ranking_favorite_questions = {}
    for favorite_question in list_favorite_questions:
        add_ranking_tuple(favorite_question[0], 1, favorite_question[1], ranking_favorite_questions)
    # logger.info([words_value, ranking_languages, ranking_favorite_questions])
    return [words_value, ranking_languages, ranking_favorite_questions]

def get_top_languages(node):
    """
    Dado un nodo, devuelve una lista vacía o una lista de lenguajes
    Inputs:
        Nodo XML
    Output:
        Lista de strings de los lenguajes de la respuesta sin respuestas aceptadas ['A', 'B', 'C']
        Lista vacía en todos los otros casos []
    """
    is_answer = bool(node.attrib.get("ParentId"))
    if is_answer:
        # This is an answer
        return []
    else:
        # This is a question, get attributes
        has_accepted_answer = node.attrib.get("AcceptedAnswerId")
        languages = node.attrib.get("Tags")
        # Bye malformed elements
        if languages is None:
            return []
        # Ranking de lenguajes sin respuestas aceptadas
        languages = languages.replace('><', ';')
        languages = languages.replace('<', '')
        languages = languages.replace('>', '')
        languages = languages.split(';')
        if not(bool(has_accepted_answer)):
            # logger.info(languages)
            return languages
        else:
            return []

def get_word_value(node):
    """
    Dado un nodo, devuelve una lista con cantidad de visitas y cantidad de palabras
    Inputs:
        Nodo XML
    Output:
        Lista con cantidad de visitas y cantidad de palabras en nodos bien formados [X, Y]
        Lista [0, 0] en todos los otros casos
    """
    word_value = 0

    number_of_words = 0
    views_total = 0

    is_answer = bool(node.attrib.get("ParentId"))
    if is_answer:
        # This is an answer
        return [0, 0]
    else:
        # This is a question, get attributes
        full_text = node.attrib.get("Body")
        views = node.attrib.get("ViewCount")
        # Bye malformed elements
        if full_text is None or views is None:
            return [0, 0]
        # Relaciónh de palabas con visitas
        filter(str.isalnum, full_text)
        full_text = filter(lambda x: x.isalnum() or x.isspace(), full_text)
        full_text = "".join(full_text)

        number_of_words = number_of_words + len(full_text.strip().split(' '))
        views_total = views_total + int(views)
        # logger.info(str([views_total, number_of_words]))
        return [views_total, number_of_words]

def get_favorite_questions(node):
    """
    Dado un nodo, devuelve una lista con cantidad de favoritos y puntaje
    Inputs:
        Nodo XML
    Output:
        Lista con con cantidad de favoritos y puntaje en nodos bien formados [X, Y]
        Lista [0, 0] en todos los otros casos
    """
    is_answer = bool(node.attrib.get("ParentId"))
    if is_answer:
        # This is a answer
        return [0, 0]
    else:
        # This is a question, get attributes
        favorite_count = node.attrib.get("FavoriteCount")
        score = node.attrib.get("Score")
        # Bye malformed elements
        if score is None or favorite_count is None:
            return[0, 0]
        else:
            # logger.info(str([favorite_count, score]))
            return [favorite_count, int(score)]
if __name__ == '__main__':
    pool = Pool(processes=mp.cpu_count())
    try:
        tree = ET.parse(FILE)
    except IOError as e:
        logger.error(f'Error al leer el archivo xml, no se lo ha encontrado: {e}')
        raise Exception('No se encontró el archivo xml')
    root = tree.getroot()
    data_chunks = chunkify(root, 100)

    # mapped = list(pool.map(mapper, data_chunks))
    # reduced = reduce(reducer, mapped)
    reduced = reduce(reducer, list(pool.map(mapper, data_chunks)))
    # Convertimos y mostramos los datos
    reduced[0] = reduced[0][0] / reduced[0][1]
    reduced[1] = sorted(reduced[1].items(), key=lambda x: x[1], reverse=True)
    for element in reduced[2]:
        reduced[2][element] = reduced[2][element][1] / reduced[2][element][0]
    reduced[2] = sorted(reduced[2].items(), key=lambda x: x[1], reverse=True)
    print(f'Valor de cada palabra {reduced[0]}')
    print(f'Top 10 de lenguajes con más preguntas sin respuestas aceptadas {reduced[1][:10]}')
    print(f'Promedio de puntaje según cantidad de favoritos {reduced[2]}')
    # print("--- %s seconds ---" % (time.time() - start_time))
