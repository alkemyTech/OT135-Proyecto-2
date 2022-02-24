import logging
from logging.config import fileConfig
import os
from task_1 import top_10_posts
from task_2 import answers_visits
from task_3 import average_response

LOGGING_CONF=os.path.join(os.path.dirname(__file__),
                           'logging.ini')
fileConfig(LOGGING_CONF)
logger = logging.getLogger('Grupo-E')


top_10 = 'Top 10 fechas con mayor cantidad de post creados:\n', top_10_posts()
answer_views = 'Relación entre cantidad de respuestas y sus visitas:\n', answers_visits()
avg_answer_0_100 = 'Tiempo de respuesta promedio en top 0-100 post con mayor puntaje:\n', average_response()
