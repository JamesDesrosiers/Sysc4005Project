


class Scheduler:
    
    eventList = None
    time = 0

    productsMade = 0

    entities = []
    
    def __init__(self):
        self.eventList = []

    def addEvent(self, new):
        self.eventList.append(new)
        self.sortEvents()

    def getTime(e):
        return e.time

    def sortEvents(self):
        self.eventList.sort(key = getTime)

    def idleCheck(self):
        checks = 0
        active = 0
        for i in self.entities:
            checks += 1
            if i.state == IDLE:
                i.activate(self, self.time)
                active += 1
        logEvent(str(checks) + " entites checked for idleness")
        logEvent(str(active) + " entites have been activated")
        return

    def popEvent(self):
        if len(self.eventList) == 0:
                logEvent("There exists no Events to Process")
                return -1
        x = self.eventList.pop(0)
        return x



class event:
    time = 0
    handler = None

    def __init__(self, creator, finish):
        self.time = finish
        self.handler = creator

    def handle(self):
        self.handler.handle(self)

def logEvent(l):
    print(l)
    
def main():
    #Create the Scheduler
    schedule = Scheduler()

    #Create the Entities
    #schedule.entities.append(inspector())

    #Add Initial events(Via the Idle Check)
    schedule.idleCheck()

    #Simulation loop
    code = -1
    while code != -1:
        #Go to next event
        x = schedule.popEvent()
    print("Simulation Ended")

if __name__ == "__main__":
    main()
