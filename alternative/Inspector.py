import sys
import threading
import time
import Buffer
from ComponentType import ComponentType
from Component import Component
from RandomGen import exp_rand_gen_range


class Inspector(threading.Thread):

    def __init__(self, buffers, timings, running):
        threading.Thread.__init__(self)
        self.running = running
        self.buffers = buffers
        self.timings = timings
        self.time_blocked = 0

    def shutdown(self):
        print(f'Inspector shutting down\n')
        self.running['running'] = False

    def check_timings(self):
        for timing in self.timings:
            if len(timing) == 0:
                return False

        return True

    def get_time_blocked(self):
        return self.time_blocked * 100

    def run(self):
        while self.running['running']:
            if not self.check_timings():
                self.shutdown()
            else:
                smallest_index = self.get_smallest_buffer_index()
                sleep_time = self.timings[smallest_index].pop()
                time.sleep(sleep_time/100)
                run = True
                time_start = time.time()
                while run:
                    run = not self.put_component(smallest_index)
                time_end = time.time()
                self.time_blocked += (time_end - time_start)/100
        print('Inspector shutting down...\n')
        sys.exit()

    def get_smallest_buffer_index(self):
        get_len = lambda buffer: buffer.get_len()
        buffer_lengths = list(map(get_len, self.buffers))
        smallest_index = buffer_lengths.index(min(buffer_lengths))
        return smallest_index

    def put_component(self, index):
        buffer = self.buffers[index]
        component_type = buffer.get_component_type()
        if buffer.get_len() < 2:
            print(f'Inspector for {component_type} is adding to the buffer\n')
            buffer.add_component(Component(component_type, time.time()))
            return True
        else:
            # print(f'Inspector for {component_type} is blocked\n')
            return False
