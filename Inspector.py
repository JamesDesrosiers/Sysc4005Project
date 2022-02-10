import Workstate
import time
from Event import event
import Component

class Inspector:
    #Variables for State
    state = None
    buffers = None
    component = None
    stuckBuffer = None
    scheduler = None

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
        if component == Component.C1:
            # Code that Finds the smallest buffer
            smallest_buffer = self.buffers[0]
            for buffer in self.buffers:
                if buffer.get_length() < smallest_buffer.get_length():
                    smallest_buffer = buffer
            
            #Checking if the buffer can have something pushed
            if smallest_buffer.isFull():
                self.stuckBuffer = smallest_Buffer
                self.state = Workstate.IDLE
            else:
                self.smallest_buffer.add_component(self.component)
                self.beginWork()
        elif isinstance(component, list):
            #Add Code for doing inspector 2 here
            pass
            

    #Fuction that adds a finish event to be handled
    def beginWork(self):
        temp = event(self, duration + scheduler.time)
        scheduler.addEvent(temp)
        self.state = Workstate.busy

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
                self.beginWork()
        else:
            self.beginWork()
        
