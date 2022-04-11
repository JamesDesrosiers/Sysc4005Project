from Workstate import Workstate
from Event import event
from Log import log
import numpy as np
from Product import Product


class Workstation:
    buffer = None
    state = None
    products = None
    product_type = None
    schedule = None

    lastActive = 0
    timeBlocked = 0

    #TEMP Values for testing
    randDurations = None
    temp_prod_comps = {}

    def __init__(self, bf, ptype, sch, randdur):
        self.buffer = bf
        self.state = Workstate.IDLE
        self.product_type = ptype
        self.products = []
        self.schedule = sch
        self.randDurations = randdur
        

    def get_state(self):
        return self.state

    def get_product(self):
        return self.product_type

    def get_products(self):
        return self.products

    def handle(self, event):
        new_prod = Product(self.product_type, self.temp_prod_comps, event.time)
        self.products.append(new_prod)
        self.temp_prod_comps = []
        self.lastActive = event.time
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
            temp_prod_comps = []
            for buffer in self.buffer:
                temp_prod_comps.append(buffer.get_component())
            self.temp_prod_comps = temp_prod_comps
            temp = event(self, self.schedule.time + self.randDurations[0],
                         "Workstation Complete")
            self.randDurations = np.delete(self.randDurations, [0])
            self.schedule.addEvent(temp)
            self.timeBlocked = self.schedule.time - self.lastActive
            self.state = Workstate.BUSY
            return
            
