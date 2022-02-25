import logging as log
import os
from logging.config import fileConfig

from task_1 import dates_with_fewer_posts
from task_2 import top_ten_words_in_posts
from task_3 import avg_time_100_200

config = os.path.join(os.path.dirname(__file__), 'logging.cfg')
fileConfig(config)

# Devuelve un logger con el nombre especificado
logger = log.getLogger('log for data group F')

# Registra un mensaje con nivel INFO en este logger
logger.info('log by console')

if __name__ == '__main__':
    print('Top 10 fechas con menor cantidad de post creados:\n', dates_with_fewer_posts())
    print('Top 10 palabras mas nombradas en los posts:\n', top_ten_words_in_posts())
    print('Tiempo de respuesta promedio en top 100-200 score:\n', avg_time_100_200())

