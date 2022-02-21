import logging
from logging import config
from os import path
from functools import reduce
from itertools import chain
import xml.etree.ElementTree as ET
from numpy import iterable
from collections import Counter
import re
from bs4 import BeautifulSoup


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

file_path = '/home/lengulian/OT135-Proyecto-2/Grupo-Datos-G/posts.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Top 10 posts mas vistos


def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]


def get_id_views(data):
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])


def sort_best_10(posts):
    sorted_posts = sorted(posts, key=lambda item: item[1], reverse=True)[:10]
    return sorted_posts


def mapper(top_posts):
    posts = list(map(get_id_views, top_posts))
    posts = sort_best_10(posts)
    return posts


def reducer(posts1, posts2):
    posts1 = posts1 + posts2
    posts1 = sort_best_10(posts1)
    return posts1


def task_1():
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper, data_chunks))
    reduced = reduce(reducer, mapped)
    print(reduced)

# Top 10 palabras mas nombradas en los post por lenguaje


def get_bodies(data):
    return data.attrib['Body']


def body_cleaner(body):
    soup = BeautifulSoup(body, 'lxml').get_text()
    soup = re.sub(r'[\n|.|,|?|¿|¡|!|(|)|-|/|\|:|\'|\"|,]', ' ', soup).lower()
    return soup.split()


def mapper2(bodies):
    body_list = list(map(get_bodies, bodies))
    body_list = list(map(body_cleaner, body_list))
    body_list = chain(*body_list)
    return Counter(body_list)


def reducer2(cnt1, cnt2):
    cnt1.update(cnt2)
    return cnt1


def task_2():
    data_chunks = chunkify(root, 50)
    mapped2 = list(map(mapper2, data_chunks))
    reduced2 = reduce(reducer2, mapped2)
    print(reduced2.most_common(10))

#Get tags
def get_tags(data):
    if data.attrib['PostTypeId'] == "1":
        return data.attrib['Tags']


def tag_cleaner(tags):
    clean_tags = re.sub(r'[<|><|>]', ' ', tags).lower()
    clean_tags = clean_tags.strip()
    return clean_tags


def tag_mapper(chunks):
    tags = list(map(get_tags, chunks))
    tags = list(filter(None, tags))  # Quito los None
    tags = list(map(tag_cleaner, tags))
    tags = list(set(tags))  # Quito los tags duplicados
    tags = "".join(tags)
    tags = tags.split()
    return tags


def tag_reducer(tags, tag2):
    tags.extend(tag2)
    return tags


data_chunks = chunkify(root, 50)
mapped_tags = list(map(tag_mapper, data_chunks))
#reduced_tags = list(map(tag_reducer, mapped_tags))
#print(reduced_tags)
print(mapped_tags)