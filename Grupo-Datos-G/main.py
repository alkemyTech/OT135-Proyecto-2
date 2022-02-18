import logging
from logging import config
from os import path

from functools import reduce
import xml.etree.ElementTree as ET

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

file_path = '/home/lengulian/Escritorio/Prueba_python/Stack Overflow 11-2010/112010 Meta Stack Overflow/posts.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Top 10 posts mas vistos
top_posts = []


def mapper():
    for i in root:
        ids = [int(i.attrib['Id']), int(i.attrib['ViewCount'])]
        top_posts.append(ids)


def reducer():
    # mapper()
    top_ten_posts = tuple(
        sorted(top_posts, key=lambda item: item[1], reverse=True))[:10]
    print(top_ten_posts)

# Top 10 posts mas vistos
def mapper(data):
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])

def reducer(top_post):
    return tuple(sorted(top_post, key=lambda item: item[1], reverse=True))


mapped = list(map(mapper, root))[:20]
#reduced = reduce(reducer, mapped)
print(mapped)
