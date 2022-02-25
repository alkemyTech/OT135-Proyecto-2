from bs4 import BeautifulSoup
import re
from itertools import chain
from statistics import mean

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def extract_bodies(data):
    yield data.attrib['Body']

def extract_scores(data):
    return int(data.attrib['Score'])

def extract_LastEditDate(root):
    lastEditDate = None
    try:
        lastEditDate = root.attrib['LastEditDate']
    except:
        pass
    return lastEditDate

def count_words(string):
    soup = BeautifulSoup(next(string), 'lxml')
    text = soup.get_text()
    text = re.sub(r'[\n|.|,|?|¿|¡|!|(|)|-|/|\|:|"]', ' ', text).lower()
    return len(text.split())

def mapper(myroot):
    texts = list(map(extract_bodies, myroot))
    words = list(map(count_words,texts))
    return words

def mapper2(myroot):
    score = list(map(extract_scores,myroot))
    return score

def reducer(words, score):
    relations = []
    for word in words:
        if word > 0:
            relations.append(score[words.index(word)]/word)
        else:
            pass
    return mean(relations)


def query2(myroot):
    '''
    Esta función recibe como parametro una root de un archivo xml parseado con ElementTree.
    Aplica técnicas de map-reduce y devuelve el valor promedio por palabra.
    '''
    root = chunkify(myroot, 100)
    words = list(map(mapper, root))
    root = chunkify(myroot, 100)
    scores = list(map(mapper2, root))

    reduced = reducer(list(chain(*words)), list(chain(*scores)))

    return reduced