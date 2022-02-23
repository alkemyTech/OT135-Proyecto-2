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

def query1(myroot):
    tags = list(map(extract_tags,myroot))
    tags = clean_tags(tags)

    answer_count = list(map(extract_answers,myroot))
    answer_count = filter_answers(answer_count)

    tags_answers = []
    for tag_list in tags:
        if (tag_list is not None):
            for tag in tag_list:
                tags_answers.append((tag, answer_count[tags.index(tag_list)]))

    results = {}
    for tag_answer in tags_answers:
        if tag_answer[0] in results:
            results[tag_answer[0]] += tag_answer[1]
        else:
            results[tag_answer[0]] = tag_answer[1]
        
    result = sorted(results, key=results.get, reverse=True)[:10]

    return result