from bs4 import BeautifulSoup
import re

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

def query2(myroot):
    # map: extraigo todos los bodies
    texts = list(map(extract_bodies,myroot))
    #reduce: reduzco cada body a la cantidad de palabras por body
    words = list(map(count_words,texts))
    #map: extraigo todos los scores
    score = list(map(extract_scores,myroot))
    #reduce: hago el promedio total comparando los scores con sus respectivos bodies
    average_score = score_per_word(words, score)

    return average_score