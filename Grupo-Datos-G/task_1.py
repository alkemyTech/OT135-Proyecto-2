from functools import reduce
import xml.etree.ElementTree as ET

file_path = '/home/lengulian/Escritorio/OT135-Proyecto-2/Grupo-Datos-G/posts.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Top 10 posts mas vistos

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def get_id_views(data):
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])

def sort_best_10(posts):
    sorted_posts = sorted(
        posts, key=lambda item: item[1], reverse=True)[:10]
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
