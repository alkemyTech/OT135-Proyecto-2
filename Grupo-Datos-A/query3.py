from datetime import datetime
from itertools import chain
from statistics import mean

def chunkify(iterable, len_of_chunk):
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i:i + len_of_chunk]

def extract_CreationDate(root):
    return root.attrib['CreationDate']
    
def extract_LastEditDate(root):
    lastEditDate = None
    try:
        lastEditDate = root.attrib['LastEditDate']
    except:
        pass
    return lastEditDate
    
def toDatetime(string):
    date = datetime.strptime(string,'%Y-%m-%dT%H:%M:%S.%f')
    return date
    
def delay(CreationDates, LastEditDates):
    delayTimes = []
    for date in LastEditDates:
        delayTimes.append((date - CreationDates[LastEditDates.index(date)]).total_seconds())
    return delayTimes

def mapper(myroot):
    
    creationDates = list(map(extract_CreationDate, myroot))
    
    lastEditDates = list(map(extract_LastEditDate, myroot))

    filteredCreationDates = []
    
    filteredLastEditDates = []

    for date in creationDates:
        index = creationDates.index(date)
        if lastEditDates[index] is not None:
            filteredCreationDates.append(creationDates[index])
            filteredLastEditDates.append(lastEditDates[index])
        
    del creationDates
    del lastEditDates

    filteredCreationDates = list(map(toDatetime,filteredCreationDates))

    filteredLastEditDates = list(map(toDatetime,filteredLastEditDates))

    delayTime = delay(filteredCreationDates, filteredLastEditDates)
    
    return delayTime



def query3(myroot):
    '''
    Esta función recibe como parametro una root de un archivo xml parseado con ElementTree.
    Aplica técnicas de map-reduce y devuelve el tiempo promedio de respuesta en días.
    '''
    myroot = chunkify(myroot, 100)
    mapped = list(map(mapper, myroot))
    reduced = mean(list(chain(*mapped)))

    return ((reduced/60)/60)/24