import Workstate
import time
import Component


class Inspector:
    id = None
    state = None
    buffers = None

    def __init__(self, identifier, bf):
        self.id = identifier  # not sure if this is needed
        self.buffers = bf
        self.state = Workstate.IDLE

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

        smallest_buffer.add_component(Component.C1)

        self.state = Workstate.IDLE
