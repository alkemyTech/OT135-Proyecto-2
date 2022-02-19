import logging
from logging import config
from os import path
from functools import reduce
import xml.etree.ElementTree as ET
from numpy import iterable

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

def obtener_id_views(data):
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])

def sort_best_10(posts):
    sorted_posts = sorted(posts, key=lambda item: item[1], reverse=True)[:10]
    return sorted_posts

def mapper(top_posts):
    posts = list(map(obtener_id_views, top_posts))
    posts = sort_best_10(posts)
    return posts

#def reducer(posts1, posts2):
    posts1 = posts1.extend(posts2)
    print(posts1)


data_chunks = chunkify(root, 50)
mapped = list(map(mapper, data_chunks))
#reduced = reduce(reducer, mapped)
print(mapped)