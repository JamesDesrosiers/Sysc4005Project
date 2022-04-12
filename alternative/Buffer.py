import threading


class Buffer:
    def __init__(self, component_type):
        self.storage = []
        self.component_type = component_type
        self.lock = threading.Lock()

    def add_component(self, component):
        self.lock.acquire()
        if len(self.storage) < 4 and self.component_type == component.get_component_type():
            self.storage.append(component)
        else:
            print(f'Storage for {self.component_type} is full\n')
        self.lock.release()

    def get_component(self):
        component = ""
        self.lock.acquire()
        if len(self.storage) > 0:
            component = self.storage.pop()
        else:
            print(f'Storage for {self.component_type} is empty\n')
        self.lock.release()
        return component

    def get_len(self):
        return len(self.storage)

    def get_component_type(self):
        return self.component_type
