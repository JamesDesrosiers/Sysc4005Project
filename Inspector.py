import Workstate
import time

class Inspector:
    state = None
    buffers = None
    component = None

    def __init__(self, bf, ctype):
        self.buffers = bf
        self.state = Workstate.IDLE
        self.component = ctype

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def handle(self, event):
        self.state = Workstate.BUSY
        time.sleep(event.time)

        # After sleep, send component to workstation
        smallest_buffer = self.buffers[0]
        for buffer in self.buffers:
            if buffer.get_length() < smallest_buffer.get_length():
                smallest_buffer = buffer

        smallest_buffer.add_component(self.component)

        self.state = Workstate.IDLE
