import logging
import logging.config
import os
import xml.etree.ElementTree as ET
from functools import reduce

# DIR = os.path.dirname(__file__)

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('logger_grupo_C')
logger.info('Test message')


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


def top_reducer(ls1, ls2):
    ls1 += ls2
    return sorted(ls1, reverse=True)[:10]

# Top 10 tipo de post con mayor respuestas aceptadas


def top_10_answered(data):
    list_top_10 = []
    for child in data:
        answer = child.attrib.get('AcceptedAnswerId')
        if answer is not None:
            list_top_10.append(int(answer))
    return sorted(list_top_10, reverse=True)[:10]

# Top 10 de usuarios con mayor porcentaje de respuestas favoritas


def top_10_favourite(data):
    list_top_10 = []
    for child in data:
        favourite = child.attrib.get('FavoriteCount')
        if favourite is not None:
            list_top_10.append(int(favourite))
    return sorted(list_top_10, reverse=True)[:10]

# Relación entre cantidad de palabras en un post y su cantidad de respuestas


def word_count(data):
    list_words = []
    for child in data:
        words = child.attrib.get('Body')
        answer = child.attrib.get('AnswerCount')
        if (words is not None) and (answer is not None):
            len_words = len(words)
            list_words.append(int(answer)/len_words*100)
    return list_words


def reducer_3(ls1, ls2):
    ls1 += ls2
    return ls1


def main():
    try:
        # Passing the path of the xml document to enable the parsing process
        tree = ET.parse('posts.xml')
        logger.info('File uploaded successfully')
    except Exception as exc:
        logger.error(exc)
        raise exc
    
    # getting the parent tag of the xml document
    root = tree.getroot()

    data_chunks1 = chunkify(root, 50)
    mapped_1 = list(map(top_10_answered, data_chunks1))
    reduced_1 = reduce(top_reducer, mapped_1)
    logger.info('top_10_answered completed successfully')

    data_chunks2 = chunkify(root, 50)
    mapped_2 = list(map(top_10_favourite, data_chunks2))
    reduced_2 = reduce(top_reducer, mapped_2)
    logger.info('top_10_favourite completed successfully')

    data_chunks3 = chunkify(root, 50)
    mapped_3 = list(map(word_count, data_chunks3))
    reduced_3 = reduce(reducer_3, mapped_3)
    logger.info('word_count completed successfully')


if __name__ == "__main__":
    logger.info('Process Initialized')
    main()
