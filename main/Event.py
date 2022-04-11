from Log import log
class event:
    time = 0
    handler = None
    special = True
    des = ""
    
    def __init__(self, creator, finish, id = ""):
        self.time = finish
        self.handler = creator
        self.des = id

    def handle(self):
        log(" **Event " + self.des + " is asking Creator to handle")
        log(" **It is time: " + str(self.time))
        self.handler.handle(self)
