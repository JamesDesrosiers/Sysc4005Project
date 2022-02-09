


class scheduler:
    
    eventList = None
    time = 0

    productsMade = 0

    entities = []
    
    def __init__():
        eventList = []

    def addEvent(self.new):
        self.eventList.append(new)
        self.sortEvents()

    def getTime(e):
        return e.time

    def sortEvents(self):
        eventList.sort(key = getTime)

    def logEvent(e):
        pass

    def __main__():
        pass

class event:
    time = 0
    handler = None

    def __init__(creator, finish):
        time = finish
        handler = creator

    def handle(self):
        creator.handle(self)
