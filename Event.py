from Log import log
class event:
    time = 0
    handler = None
    special = True

    def __init__(self, creator, finish):
        self.time = finish
        self.handler = creator

    def handle(self):
        log("**Event is asking Creator to handle")
        log("**It is time: " + str(self.time))
        self.handler.handle(self)
