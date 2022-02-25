from itertools import chain

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def extract_tags(data):
    yield data.attrib['Tags']

def extract_answers(data):
    yield data.attrib['AnswerCount']

def clean_tags(tags):
    tags_list = []
    for tag in tags:
        try:
            tag = next(tag)
            tag = tag.replace('<','')
            tag = tag.replace('>',' ')
            tag = tag.split()
            tags_list.append(tag)
        except:
            tags_list.append(None)
    return tags_list

def filter_answers(answer_count):
    answers_filtered = []
    for answer in answer_count:
        try:
            answer = int(next(answer))
            answers_filtered.append(answer)
        except:
            answers_filtered.append(0)
    return answers_filtered

def mapper(myroot):

    # Mapeo una lista de tags y una lista con la cantidad de respuestas

    tags = list(map(extract_tags,myroot))
    tags = clean_tags(tags)

    answer_count = list(map(extract_answers,myroot))
    answer_count = filter_answers(answer_count)

    # Armo una lista de tuplas donde cada una tiene el siguiente formato: (tag, cantidad de respuestas)

    tags_answers = []
    for tag_list in tags:
        if (tag_list is not None):
            for tag in tag_list:
                tags_answers.append((tag, answer_count[tags.index(tag_list)]))

    # Borro las listas que ya no necesito

    del tags
    del answer_count

    return tags_answers

def reducer(tags_answers):

    # Armo un diccionario donde cada key es una tag y cada value la acumulación de respuestas

    results = {}
    for tag_answer in tags_answers:
        if tag_answer[0] in results:
            results[tag_answer[0]] += tag_answer[1]
        else:
            results[tag_answer[0]] = tag_answer[1]
        
    result = sorted(results, key=results.get, reverse=True)[:10]

    return result

def query1(myroot):
    '''
    Esta función recibe como parametro una root de un archivo xml parseado con ElementTree.
    Aplica técnicas de map-reduce y devuelve una lista con los 10 tags que más respustas aceptadas tienen.
    '''

    chunks = chunkify(myroot, 1000)
    mapped = list(map(mapper, chunks))
    reduced = reducer(list(chain(*mapped)))

    return reduced