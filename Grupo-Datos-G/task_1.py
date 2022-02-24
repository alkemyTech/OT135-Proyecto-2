from functools import reduce
import xml.etree.ElementTree as ET

file_path = 'posts.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Top 10 posts mas vistos

def chunkify(iterable, len_of_chunk):
    '''Divide un archivo grande en pedazos'''
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def get_id_views(data):
    '''Obtiene los id y viewcount'''
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])

def sort_best_10(posts):
    '''Ordena los post de mayor a menor por views'''
    sorted_posts = sorted(
        posts, key=lambda item: item[1], reverse=True)[:10]
    return sorted_posts

def mapper(top_posts):
    '''Itera los data_chunks para obtener los id y views, y los ordena de mayor a menor'''
    posts = list(map(get_id_views, top_posts))
    posts = sort_best_10(posts)
    return posts

def reducer(posts1, posts2):
    '''Retorna el top 10 de post más vistos'''
    posts1 = posts1 + posts2
    posts1 = sort_best_10(posts1)
    return posts1

def task_1():
    '''Ejecuta una consulta que devuelve los 10 post(id, viewcount) más vistos'''
    data_chunks = chunkify(root, 50)
    mapped = list(map(mapper, data_chunks))
    reduced = reduce(reducer, mapped)
    print(reduced)
