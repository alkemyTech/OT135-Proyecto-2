import xml.etree.ElementTree as ET
from collections import Counter
from functools import reduce

'''
Script que devuelve: 
- Top 10 fechas con mayor cantidad de post creados 
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
