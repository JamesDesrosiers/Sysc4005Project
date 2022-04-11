
class Component:

    def __init__(self, ctype, create_time):
        self.ctype = ctype
        self.create_time = create_time

    def get_create_time(self):
        return self.create_time

    def get_component_type(self):
        return self.ctype
