
import logging
from logging.config import fileConfig
import os
import xml.etree.ElementTree as ET
from functools import reduce
from bs4 import BeautifulSoup
import re

LOGGING_CONF=os.path.join(os.path.dirname(__file__), 'logging.cfg')
fileConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)

mytree = ET.parse('Grupo-Datos-A/112010 Meta Stack Overflow/posts.xml')
myroot = mytree.getroot()

# Valor promedio de puntaje por palabra

def extract_bodies(data):
    yield data.attrib['Body']

def extract_scores(data):
    yield int(data.attrib['Score'])

def count_words(string):
    soup = BeautifulSoup(next(string), 'lxml')
    text = soup.get_text()
    text = re.sub(r'[\n|.|,|?|¿|¡|!|(|)|-|/|\|:|"]', ' ', text).lower()
    yield len(text.split())

def score_per_word(words, score):
    average = 0
    for word in words:
        w = next(word)
        s = next(score[words.index(word)])
        if w != 0:
            average = (average+(s/w))/2
        else:
            pass
    return average

# map: extraigo todos los bodies
texts = list(map(extract_bodies,myroot))
#reduce: reduzco cada body a la cantidad de palabras por body
words = list(map(count_words,texts))
#map: extraigo todos los scores
score = list(map(extract_scores,myroot))
#reduce: hago el promedio total comparando los scores con sus respectivos bodies
average_score = score_per_word(words, score)

print(f'Average score per word is equal to: {average_score}')
