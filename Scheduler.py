from Workstate import Workstate
from Inspector import Inspector
from Buffer import Buffer
from Component import Component
from Log import log
from Workstation import Workstation
from Product import Product

#Temp Import for Testing
from Event import event

# Author: James
SIMULATIONTIME = 100


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
        log("Time is at: " + str(self.time) + ", Checking Idle Entities")
        active = 0
        for i in self.entities:
            checks += 1
            if i.state == Workstate.IDLE:
                i.activate()
                active += 1
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
    I2 = Inspector([QC2W2, QC3W3], [Component.C2, Component.C3], schedule)

    #   Creating the Workstations
    W1 = Workstation([QC1W1], Product.P1, schedule)
    W2 = Workstation([QC1W2, QC2W2], Product.P2, schedule)
    W3 = Workstation([QC1W3, QC3W3], Product.P3, schedule)

    #Add Inspectors to Scheduler
    schedule.entities.append(I1)
    schedule.entities.append(I2)
    schedule.entities.append(W1)
    schedule.entities.append(W2)
    schedule.entities.append(W3)

    #Add Initial events(Via the Idle Check)
    schedule.idleCheck()

    #Simulation loop
    code = 1
    while code != -1:
        #Go to next event
        x = schedule.popEvent()
        #temp code to handle having no events
        if x == -1 or schedule.time > SIMULATIONTIME:
            code = -1
        else:
            schedule.setTime(x.time)
            x.handle()
        #Checking if any of the idle entities can fire
        schedule.idleCheck()

    log("Simulation Ended at Time: " + str(schedule.time))
    log("REPORT:")
    log("   Workstation W1 Produced: " + str(W1.products) + " units P1")
    log("   Workstation W2 Produced: " + str(W2.products) + " units P2")
    log("   Workstation W3 Produced: " + str(W3.products) + " units P3")

if __name__ == "__main__":
    main()
