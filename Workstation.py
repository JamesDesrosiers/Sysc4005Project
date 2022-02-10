from Workstate import Workstate
from Event import event
from Log import log


class Workstation:
    buffer = None
    state = None
    products = None
    product = None
    schedule = None

    #TEMP Values for testing
    duration = 3

    def __init__(self, bf, ptype, sch):
        self.buffer = bf
        self.state = Workstate.IDLE
        self.product = ptype
        self.products = 0
        self.schedule = sch
        

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def get_product(self):
        return self.product

    def get_products(self):
        return self.products

    def handle(self, event):
        self.products += 1
        self.state = Workstate.IDLE

    def activate(self):
        #Check if components exist to do work
        has_empty = False
        for buffer in self.buffer:
            if buffer.get_length() == 0:
                has_empty = True
                break
        # If there are enough components, take components and add completion event
        if not has_empty:  
            for buffer in self.buffer:
                buffer.get_component()
            temp = event(self, self.schedule.time + self.duration,
                         "Workstation Complete")
            self.schedule.addEvent(temp)
            self.state = Workstate.BUSY
            return
            
