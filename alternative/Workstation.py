import sys
import threading
import time
from Buffer import Buffer
from ComponentType import ComponentType
from RandomGen import exp_rand_gen_range
from Component import Component
from ProductType import ProductType
from Product import Product

class Workstation(threading.Thread):

    def __init__(self, buffers, timing, ptype, running):
        threading.Thread.__init__(self)
        self.buffers = buffers
        self.timing = timing
        self.running = running
        self.products = []
        self.ptype = ptype
        self.time_blocked = 0

    def get_products(self):
        return self.products

    def get_product_type(self):
        return self.ptype

    def get_time_blocked(self):
        return self.time_blocked * 100

    def shutdown(self):
        print(f'Workstation for {self.ptype} shutting down\n')
        self.running['running'] = False

    def run(self):
        while self.running['running']:
            if len(self.timing) == 0:
                self.shutdown()
            else:
                if self.buffers_ready():
                    sleep_time = self.timing.pop()
                    time.sleep(sleep_time / 100)
                    components = []
                    # time_start = time.time()
                    for buffer in self.buffers:
                        component = self.get_component(buffer)
                        if not isinstance(component.get_component_type(), ComponentType):
                            time_start = time.time()
                            while not isinstance(component.get_component_type(), ComponentType):
                                component = self.get_component(buffer)
                            time_end = time.time()
                            self.time_blocked += time_end - time_start
                        components.append(component)
                    self.products.append(Product(self.ptype, components, time.time()))
        print('Workstation shutting down...\n')
        sys.exit()

    def buffers_ready(self):
        for buffer in self.buffers:
            if buffer.get_len() == 0:
                return False
        return True

    def get_component(self, buffer):
        component_type = buffer.get_component_type()
        if buffer.get_len() > 0:
            # print(f'Workstation for {self.ptype} is getting {component_type}\n')
            return buffer.get_component()
        else:
            # print(f'Workstation for {self.ptype} is blocked\n')
            return Component('', 0)

# if __name__ == "__main__":
#     # b11 = Buffer(ComponentType.C1)
#     # b11.add_component(Component(ComponentType.C1, 0))
#     # b11.add_component(Component(ComponentType.C1, 0))
#     # b22 = Buffer(ComponentType.C2)
#     # b22.add_component(Component(ComponentType.C2, 0))
#     # b22.add_component(Component(ComponentType.C2, 0))
#     # ws1_timing = exp_rand_gen_range(4.604417, 0.007, 29.375, 10).tolist()
#     # w1 = Workstation([b11, b22], ws1_timing, ProductType.P1)
#     # w1.start()
#     test = {
#         'test': True
#     }