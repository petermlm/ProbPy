"""
TODO documentation
"""


class Event:
    def __init__(self, tlist=None, var=None, val=None):
        if tlist is not None and type(tlist) is list:
            self.event = tlist
        elif var is not None or val is not None:
            self.event = [(var, val)]
        else:
            self.event = []

    def varInEvent(self, var):
        for i in self.event:
            if i[0].name == var.name:
                return True
        return False

    def value(self, var):
        for i in self.event:
            if i[0].name == var.name:
                return i[1]
        return None

    def setValue(self, var, value):
        for i in range(len(self.event)):
            if self.event[i][0].name == var.name:
                self.event[i][1] = value
                return
        self.event.append((var, value))

    def __iter__(self):
        cindex = 0
        while cindex < len(self.event):
            yield self.event[cindex]
            cindex += 1
