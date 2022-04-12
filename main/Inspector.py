import numpy as np

from Workstate import Workstate
from Event import event
from ComponentType import ComponentType
from Log import log
from random import randint
from Component import Component


class Inspector:
    # Variables for State
    state = None
    buffers = None
    component_type = None
    stuckBuffer = None
    scheduler = None
    cIndex = 0

    lastActive = 0
    timeBlocked = 0
    # TEMP Variables for working
    # TODO find duration based on data
    randDurations = None

    def __init__(self, bf, ctype, sch, randdur):
        self.buffers = bf
        self.state = Workstate.IDLE
        self.component_type = ctype
        self.scheduler = sch
        self.randDurations = randdur

    def get_state(self):
        return self.state

    # TODO Finish code for Inpector 2's handle
    def handle(self, event):
        if self.component_type == ComponentType.C1:
            # Code that Finds the smallest buffer
            smallest_buffer = self.buffers[0]
            for buffer in self.buffers:
                if buffer.get_length() < smallest_buffer.get_length():
                    smallest_buffer = buffer

            # Checking if the buffer can have something pushed
            if smallest_buffer.isFull():
                self.stuckBuffer = smallest_buffer
                self.lastActive = event.time
                self.state = Workstate.IDLE
            else:
                smallest_buffer.add_component(Component(self.component_type, self.scheduler.time))
                self.beginWork()
        elif isinstance(self.component_type, list):
            # Only I2 Should arrive here
            if self.buffers[self.cIndex].isFull():
                self.stuckBuffer = self.buffers[self.cIndex]
                self.lastActive = event.time
                self.state = Workstate.IDLE
            else:
                self.buffers[self.cIndex].add_component(Component(self.component_type[self.cIndex], self.scheduler.time))
                self.beginWork()

    # Function that adds a finish event to be handled
    def beginWork(self):
        # Generate useful event ID
        if self.component_type == ComponentType.C1:
            id = "Inspection of C1 Complete"
        else:
            self.cIndex = randint(0, 1)
            if self.cIndex == 0:
                id = "Inspection of C2 Comlete"
            else:
                id = "Inspection of C3 Complete"

        temp = None
        if isinstance(self.component_type, list):
            if len(self.randDurations[self.cIndex]) > 0:
                temp = event(self, self.randDurations[self.cIndex][0] + self.scheduler.time, id)
                self.randDurations[self.cIndex] = np.delete(self.randDurations[self.cIndex], [0])
            else:
                temp = event(self, -1, id)
        else:
            if len(self.randDurations) > 0:
                temp = event(self, self.randDurations[0] + self.scheduler.time, id)
                self.randDurations = np.delete(self.randDurations, [0])
            else:
                temp = event(self, -1, id)
        self.scheduler.addEvent(temp)
        self.state = Workstate.BUSY

    # There exists 2 reasons for an inspector to be idle
    #   1- The inspector has yet to become busy for the first time
    #   2- The inspector is stuck on pushing out a component
    def activate(self):
        if self.stuckBuffer is not None:
            if self.stuckBuffer.isFull():
                # The Inspector is still stuck
                return
            else:
                if isinstance(self.component_type, list):
                    self.stuckBuffer.add_component(Component(self.component_type[self.cIndex], self.scheduler.time))
                else:
                    self.stuckBuffer.add_component(Component(self.component_type, self.scheduler.time))
                self.timeBlocked += self.scheduler.time - self.lastActive
                self.beginWork()
        else:
            self.beginWork()
