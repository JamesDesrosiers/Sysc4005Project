from Workstate import Workstate
from Inspector import Inspector
from Buffer import Buffer
from Component import Component
from Log import log

#Temp Import for Testing
from Event import event

class Scheduler:
    
    eventList = []
    time = -1

    productsMade = 0

    entities = []
    
    def __init__(self):
        self.eventList = []
        self.time = 0

    def addEvent(self, new):
        self.eventList.append(new)
        self.sortEvents()

    def getTime(self, e):
        return e.time

    def setTime(self, new):
        self.time = new

    def sortEvents(self):
        self.eventList.sort(key = self.getTime)

    def idleCheck(self):
        checks = 0
        active = 0
        for i in self.entities:
            checks += 1
            if i.state == Workstate.IDLE:
                i.activate()
                active += 1
        log("Time is at: " + str(self.time) + ", Checking Idle Entities")
        log("     " + str(checks) + " entites checked for idleness")
        log("     " + str(active) + " entites have been activated")
        return

    def popEvent(self):
        if len(self.eventList) == 0:
                log("There exists no Events to Process")
                return -1
        x = self.eventList.pop(0)
        return x

def main():
    #Create the Scheduler
    schedule = Scheduler()

    #Creating the Queues
    #Name Format: QC#W#
    #Explanation
    #   C# references the component the queue accepts
    #   W# references which workstation uses the queue
    QC1W1 = Buffer()
    QC1W2 = Buffer()
    QC1W3 = Buffer()

    QC2W2 = Buffer()

    QC3W3 = Buffer()
    
    #Create the Entities
    #   Creating the Inspectors
    I1 = Inspector([QC1W1,QC1W2, QC1W3],Component.C1, schedule)
    I2 = None

    #Add Inspectors to Scheduler
    schedule.entities.append(I1)
    #schedule.entities.append(inspector())
    #schedule.entities.append(workstation())
    #schedule.entities.append(workstation())
    #schedule.entities.append(workstation())

    #Add Initial events(Via the Idle Check)
    schedule.idleCheck()

    #TEMP CODE for testing
    temp = event(None, 2)
    temp.special = True
    schedule.addEvent(temp)

    #Simulation loop
    code = 1
    while code != -1:
        #Go to next event
        x = schedule.popEvent()
        #temp code to handle having no events
        if x == -1 and True:
            code = -1
        else:
            if x.special:
                log("Special event is being run")
            else:
                x.handle()
            schedule.setTime(x.time)
        #Checking if any of the idle entities can fire
        schedule.idleCheck()
        
    log("Simulation Ended")

if __name__ == "__main__":
    main()
