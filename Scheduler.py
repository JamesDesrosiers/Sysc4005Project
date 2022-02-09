


class scheduler:
    
    eventList = None
    time = 0
    
    def __init__():
        eventList = []

    def addEvent(new):
        eventList.append(new)
        sortEvents()

    def getTime(e):
        return e.time

    def sortEvents():
        eventList.sort(key = getTime)
5
