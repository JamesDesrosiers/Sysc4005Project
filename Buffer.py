import queue


class Buffer:
    queue = None

    def __init__(self):
        self.queue = queue.Queue()

    def get_length(self):
        return len(self.queue)

    def add_component(self, component):
        self.queue.append(component)

    def get_component(self):
        if self.queue.empty():
            return None

        return self.queue.pop()
