import os 
import pandas as pd 
import xml.etree.ElementTree as etree
from functools import reduce
from datetime import datetime


    # ['Id', 'PostTypeId', 'ParentId', 
    # 'AcceptedAnswerId', 'CreationDate', 'Score',
    # 'ViewCount', 'Body', 'OwnerUserId',
    # 'LastEditorUserId', 'LastEditorDisplayName',
    # 'LastEditDate', 'LastActivityDate', 'CommunityOwnedDate',
    # 'ClosedDate', 'Title', 'Tags',
    # 'AnswerCount', 'CommentCount', 'FavoriteCount'
    # ]

dir = os.path.dirname(__file__)
tree = etree.parse(r'./posts.xml')   

def chunkify(iterable, len_of_chunk):  
    for i in range(0, len(iterable), len_of_chunk): 
        yield iterable[i:i + len_of_chunk] 

def post_type_list(data): 
    score_list=[]
    post_list = []
    for element in data:
        answer = element.attrib.get('AcceptedAnswerId')
        post_type = element.attrib.get('PostType')
        score = element.attrib.get('Score')
        if answer is None and post_type is not None:
            post_list.append(post_type)
            score_list.append(score)
        
    return score_list

def reducer1(data):
    list_a = sorted(data, key=lambda x:x[1], reverse=True)
    list_a = [i[0] for i in list_a]
    return list_a[:10]

def creation_date_list(data):
    date_list = []
    for element in data:
        date1 = element.attrib.get('CreationDate')
        date2 = element.attrib.get('LastActivityDate')
        date_list.append((datetime.datetime.strptime(date2,'%Y-%m-%dT%H:%M:%S.%f')-(datetime.datetime.strptime(date1,'%Y-%m-%dT%H:%M:%S.%f'))))
    return sorted(date_list, reverse = True)

def reducer2(data):
    list_2 = data[:10]

def s_a_relation(data):
    list_3 =[]
    for element in data:
        score = element.attrib.get('Score')
        answercount = element.attrib.get('AnswerCount')
        list_3.append(answercount/score)
    return list_3

def reducer3(data):
    rel=sum(data)
    return rel

root = tree.getroot()
chunks = chunkify(root, 50)
mapped1 =list(map(post_type_list, chunks))
#reduced1 = reduce(reducer1, mapped1)