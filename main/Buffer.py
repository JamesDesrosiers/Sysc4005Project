import queue


class Buffer:
    queue = None

    def __init__(self):
        self.queue = queue.Queue(2)

    def get_length(self):
        return self.queue.qsize()

    def add_component(self, component):
        self.queue.put(component)

    def get_component(self):
        if self.queue.empty():
            return None

        return self.queue.get()

    def isFull(self):
        return self.queue.full()
