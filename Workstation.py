import Workstate
import time


class Workstation:
    buffer = None
    state = None
    products = None
    product = None

    def __init__(self, bf, ptype):
        self.buffer = bf
        self.state = Workstate.IDLE
        self.product = ptype
        self.products = []

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def get_product(self):
        return self.product

    def get_products(self):
        return self.products

    def handle(self, event):
        self.state = Workstate.BUSY

        # After sleep, send component to workstation
        has_empty = False
        for buffer in self.buffers:
            if buffer.get_length() == 0:
                has_empty = True
                break

        if not has_empty:  # If there are enough components, take components and make a product
            time.sleep(event.time)
            for buffer in self.buffers:
                buffer.get_component()
            self.products.append(self.product)

        self.state = Workstate.IDLE
