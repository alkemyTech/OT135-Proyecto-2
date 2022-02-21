import xml.etree.ElementTree as ET
from collections import Counter
from functools import reduce

'''
Script que realiza 3 funciones:
- Top 10 fechas con mayor cantidad de post creados 
- Relación entre cantidad de respuestas y sus visitas - Answer -> ViewCount
- Tiempo de respuesta promedio en top 0-100 post con mayor puntaje 
'''

# Devuelve un objeto con los datos cargados
def routing():
  route_file = 'posts.xml'
  tree = ET.parse(route_file)
  root = tree.getroot()
  return root

'''
Itera desde el rango hasta el total del tamaño del chunk
iterable -> arbol completo(root)
len_chunk -> cantidad de veces a dividir
Devuelve la cantidad de elementos del chunk
'''
def chukinfy(iterable, len_chunk):
  for i in range(0, len(iterable), len_chunk):
      yield iterable[i:i + len_chunk]

# Recibe un elemento y devuelve la fecha de un post
def search_fecha(data):
  return data.attrib['CreationDate'][:10]

# Devuelve una lista con las cantidades de post por fecha
def mapper_top(fechas):
  mapp_fechas = list(map(search_fecha, fechas))
  return Counter(mapp_fechas)

# Aplica la funcion a 2 elementos y actualiza el resultado
def reducer_top(cnt1, cnt2):
  cnt1.update(cnt2)
  return cnt1

'''
Devuelve el top 10 fechas con mayor cantidad de post creados
'''
def top_10_posts():
  # Ruta del archivo .xml
  root = routing()
  data_chunks = chukinfy(root, 50)
  mapped_top = list(map(mapper_top, data_chunks))
  reduced_top = reduce(reducer_top, mapped_top)
  return reduced_top.most_common(10)

'''
Recibe un elemento y devuelve el id y la cantidad de visitas
Si es PostTypeId = 1 es question, devuelve None
'''
def id_views(data):
  if data.attrib['PostTypeId'] == '2':
    return int(data.attrib['Id']), int(data.attrib['ViewCount'])
  else:
    pass

def order_top(asnwers):
  ordered = sorted(asnwers, key=lambda item: item[1])
  return ordered

def reducer_answers(cp1, cp2):
    cp1 = cp1 + cp2
    cp2 = order_top(cp1)
    return cp1

def mapper_answers(top_posts):
  mapp_answers = list(map(id_views, top_posts))
  # Filtra las question (None)
  mapp_answers = list(filter(None, mapp_answers))
  return mapp_answers

'''
Devuelve la relación entre cantidad de respuestas y sus visitas
(por cada respuesta cuantas visitas)
'''
def answers_visits():
  root = routing()
  data_chunks = chukinfy(root, 50)
  mapped = list(map(mapper_answers, data_chunks))
  reduced = reduce(reducer_answers, mapped)
  return reduced
