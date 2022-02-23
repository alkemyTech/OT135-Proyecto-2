from datetime import datetime

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
    
def daleay(CreationDates, LastEditDates):
    delayTime = 0
    for date in LastEditDates:
        delay = (date - CreationDates[LastEditDates.index(date)]).total_seconds()
        delayTime = (delayTime+delay)/2
    return delayTime

def query3(myroot):
    creationDates = list(map(extract_CreationDate, myroot))

    lastEditDates = list(map(extract_LastEditDate, myroot))

    for i in range(10):
        for date in creationDates:
            index = creationDates.index(date)
            if lastEditDates[index] is None:
                del lastEditDates[index]
                del creationDates[index]

    creationDates = list(map(toDatetime,creationDates))

    lastEditDates = list(map(toDatetime,lastEditDates))

    delayTime = daleay(creationDates, lastEditDates)

    return delayTime