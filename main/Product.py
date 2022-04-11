
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