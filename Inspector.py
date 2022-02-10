from Workstate import Workstate
from Event import event
from Component import Component
from Log import log
from random import randint

class Inspector:
    #Variables for State
    state = None
    buffers = None
    component = None
    stuckBuffer = None
    scheduler = None
    cIndex = 0

    lastActive = 0
    timeBlocked = 0
    #TEMP Variables for working
    #TODO find duration based on data
    duration = 2

    def __init__(self, bf, ctype, sch):
        self.buffers = bf
        self.state = Workstate.IDLE
        self.component = ctype
        self.scheduler = sch

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    #TODO Finish code for Inpector 2's handle
    def handle(self, event):
        if self.component == Component.C1:
            # Code that Finds the smallest buffer
            smallest_buffer = self.buffers[0]
            for buffer in self.buffers:
                if buffer.get_length() < smallest_buffer.get_length():
                    smallest_buffer = buffer
            
            #Checking if the buffer can have something pushed
            if smallest_buffer.isFull():
                self.stuckBuffer = smallest_buffer
                self.lastActive = event.time
                self.state = Workstate.IDLE
            else:
                smallest_buffer.add_component(self.component)
                self.beginWork()
        elif isinstance(self.component, list):
            #Only I2 Should arrive here
            if self.buffers[self.cIndex].isFull():
                self.stuckBuffer = self.buffers[self.cIndex]
                self.lastActive = event.time
                self.state = Workstate.IDLE
            else:
                self.buffers[self.cIndex].add_component(self.component[self.cIndex])
                self.beginWork()
            

    #Fuction that adds a finish event to be handled
    def beginWork(self):
        #GEnerate useful event ID
        if self.component == Component.C1:
            id = "Ispection of C1 Complete"
        else:
            self.cIndex = randint(0,1)
            if self.cIndex == 0:
                id = "Inspection of C2 Comlete"
            else:
                id = "Inspection of C3 Complete"
        temp = event(self, self.duration + self.scheduler.time, id)
        self.scheduler.addEvent(temp)
        self.state = Workstate.BUSY

    #There exists 2 reasons for an inspector to be idle
    #   1- The inspector has yet to become busy for the first time
    #   2- The inspector is stuck on pushing out a component
    def activate(self):
        if self.stuckBuffer is not None:
            if self.stuckBuffer.isFull():
                #The Inspector is still stuck
                return
            else:
                self.stuckBuffer.add_component(self.component)
                self.timeBlocked += self.scheduler.time - self.lastActive
                self.beginWork()
        else:
            self.beginWork()
        
