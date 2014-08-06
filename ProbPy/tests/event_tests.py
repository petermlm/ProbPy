from nose.tools import with_setup, nottest

from ProbPy.tests.test_base import TestBase

from ProbPy import Event


class TestEvent(TestBase):
    def eventConst_test_0(self):
        """
        Empty constructor
        """

        event = Event()
        assert(len(event.event) == 0)
        assert(event.event == [])

    def eventConst_test_1(self):
        """
        tlist test, one element
        """

        tlist = [(self.X, self.X.domain[0])]
        event = Event(tlist=tlist)

        assert(len(event.event) == 1)
        assert(event.event[0].var.name == self.X.name)
        assert(event.event[0].val == self.X.domain[0])

    def eventConst_test_2(self):
        """
        tlist test, two element
        """

        tlist = []
        tlist.append((self.X, self.X.domain[0]))
        tlist.append((self.Y, self.Y.domain[0]))

        event = Event(tlist=tlist)

        assert(len(event.event) == 2)
        assert(event.event[0].var.name == self.X.name)
        assert(event.event[0].val == self.X.domain[0])
        assert(event.event[1].var.name == self.Y.name)
        assert(event.event[1].val == self.Y.domain[0])

    def eventConst_test_3(self):
        """
        var and val
        """

        event = Event(var=self.X, val=self.X.domain[0])

        assert(len(event.event) == 1)
        assert(event.event[0].var.name == self.X.name)
        assert(event.event[0].val == self.X.domain[0])

    def eventVarInEvent_test_4(self):
        event = Event(var=self.X, val=self.X.domain[0])

        assert(event.varInEvent(self.X))
        assert(not event.varInEvent(self.Y))

    def eventValue_test_5(self):
        event = Event(var=self.X, val=self.X.domain[0])

        assert(event.value(self.X) == self.X.domain[0])

    def eventSetValue_test_6(self):
        event = Event(var=self.X, val=self.X.domain[0])
        event.setValue(self.X, self.X.domain[1])
        event.setValue(self.Y, self.Y.domain[1])

        assert(len(event.event) == 2)
        assert(event.value(self.X) == self.X.domain[1])
        assert(event.value(self.Y) == self.Y.domain[1])

    def eventIter_test_7(self):
        tlist = [(self.X, self.X.domain[0]),
                 (self.Y, self.Y.domain[0]),
                 (self.Z, self.Z.domain[0])]
        event = Event(tlist=tlist)

        iter_res = [i for i in event]

        for i in range(len(tlist)):
            if tlist[i][0].name != iter_res[i][0].name and \
               tlist[i][1] != iter_res[i][1]:
                assert(False)

        assert(True)
