
class Product:

    def __init__(self, ptype, components, create_time):
        self.ptype = ptype
        self.components = components
        self.create_time = create_time

    def get_ptype(self):
        return self.ptype

    def get_components(self):
        return self.components

    def get_create_time(self):
        return self.create_time

    def get_finish_time(self):
        smallest_time = self.components[0].get_create_time()
        for component in self.components:
            create_time = component.get_create_time()
            if create_time < smallest_time:
                smallest_time = create_time
        return (self.create_time - smallest_time) * 100
