import xml.etree.cElementTree as ET
from xml.etree.cElementTree import iterparse

FILE = 'posts.xml'
FILE_BETA = 'posts_beta.xml'

#  tree = ET.parse(FILE)
#  root = tree.getroot()

ranking_languages = {}
ranking_favorite_answers = {}
number_of_words = 0
views_total = 0
items = 0

def add_ranking(key,increment,ranking):
    if key in ranking:
        ranking[key] = ranking[key] + increment
    else:
        ranking[key] = increment
def reducer_function():
    #  for _, node in iterparse(FILE, events=("end",)):
    for event, node in iterparse(FILE):
    #  for node in root:
        items = items + 1
        if items % 100000 == 0:
            print(f'Procesados {items} elementos')
        row_Id = node.attrib.get("Id")
        is_answer = bool(node.attrib.get("ParentId"))
        if is_answer:
            # This is a answer
            favorite_count = node.attrib.get("FavoriteCount")
            score = node.attrib.get("Score")
            #  if favorite_count>0:
            #      add_ranking(row_Id, int(score), ranking_favorite_answers)
            #  TODO: mover score al if
            #  print(f'Esto es una respuesta: puntaje {score} y favoritos {favorite_count}')
        else:
            # This is a question
            has_accepted_answer = bool(node.attrib.get("AcceptedAnswerId"))
            languages = node.attrib.get("Tags")
            if languages is None:
                continue
            languages = languages.replace('><',';')
            languages = languages.replace('<','')
            languages = languages.replace('>','')
            languages = languages.split(';')
            if not(has_accepted_answer):
                for language in languages:
                    add_ranking(language,1,ranking_languages)
            full_text = node.attrib.get("Body")
            number_of_words = number_of_words + len(full_text.strip().split(' '))
            views = node.attrib.get("ViewCount")
            views_total = views_total + int(views)
            #  print(f'Esto es una pregunta: Respuesta aceptada {has_accepted_answer}, lenguajes {languages} y visitas {views}')
        node.clear()
reducer_function()
# Ranking de lenguajes sin respuestas
sorted_ranking_languages = sorted(ranking_languages.items(), key=lambda x: x[1], reverse=True)
print(sorted_ranking_languages[:20])
#  Relación de visitas y palabras
#  print(f'Cantidad de palabnas: {number_of_words} y visitas: {views_total}')
# Ranking de respuestas con más favoritos
#  sorted_ranking_favorite_answers = sorted(ranking_favorite_answers.items(), key=lambda x: x[1], reverse=True)
#  print(sorted_ranking_favorite_answers)
