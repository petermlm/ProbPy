"""
TODO documentation
"""


from ProbPy import RandVar


class EventEle:
    def __init__(self, var, val):
        if type(var) is not RandVar:
            raise EventEleEx("var")
        elif val is None:
            raise EventEleEx("val")

        self.var = var
        self.val = val


class Event:
    def __init__(self, tlist=None, var=None, val=None):
        if tlist is not None and type(tlist) is list:
            self.event = [EventEle(i[0], i[1]) for i in tlist]
        elif var is not None or val is not None:
            self.event = [EventEle(var, val)]
        else:
            self.event = []

    def varInEvent(self, var):
        for i in self.event:
            if i.var.name == var.name:
                return True

        return False

    def value(self, var):
        for i in self.event:
            if i.var.name == var.name:
                return i.val

        return None

    def setValue(self, var, val):
        for i in range(len(self.event)):
            if self.event[i].var.name == var.name:
                self.event[i].val = val
                return

        self.event.append(EventEle(var, val))

    def __iter__(self):
        cindex = 0
        while cindex < len(self.event):
            ele = self.event[cindex]
            yield (ele.var, ele.val)
            cindex += 1


class EventEleEx(Exception):
    def __init__(self, op):
        if op is "var":
            self.txt = "Bad value for var argument of Event element."
        elif op is "val":
            self.txt = "Bad value for val argument of Event element."

    def __str__(self):
        return self.txt
