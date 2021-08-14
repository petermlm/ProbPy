from nose.tools import with_setup, nottest

from tests.test_base import TestBase
from ProbPy import Event


class TestEvent(TestBase):
    def eventConst_test_0(self):
        """
        Empty constructor
        """

        event = Event()
        assert event.event == {}

    def eventConst_test_1(self):
        """
        tlist test, one element
        """

        tlist = [(self.X, self.X.domain[0])]
        event = Event(tlist=tlist)

        assert len(event.event.keys()) == 1
        assert event.event[self.X] == self.X.domain[0]

    def eventConst_test_2(self):
        """
        tlist test, two element
        """

        tlist = []
        tlist.append((self.X, self.X.domain[0]))
        tlist.append((self.Y, self.Y.domain[0]))

        event = Event(tlist=tlist)

        assert len(event.event.keys()) == 2

        assert event.event[self.X] == self.X.domain[0]
        assert event.event[self.Y] == self.Y.domain[0]

    def eventConst_test_3(self):
        """
        var and val
        """

        event = Event(var=self.X, val=self.X.domain[0])

        assert len(event.event.keys()) == 1
        assert event.event[self.X] == self.X.domain[0]

    def eventVarInEvent_test_4(self):
        """
        Test varInEvent() method
        """

        event = Event(var=self.X, val=self.X.domain[0])

        assert event.varInEvent(self.X)
        assert not event.varInEvent(self.Y)

    def eventValue_test_5(self):
        """
        Test value() method
        """

        event = Event(var=self.X, val=self.X.domain[0])
        assert event.value(self.X) == self.X.domain[0]

    def eventSetValue_test_6(self):
        """
        Test setValue method
        """

        event = Event(var=self.X, val=self.X.domain[0])
        event.setValue(self.X, self.X.domain[1])
        event.setValue(self.Y, self.Y.domain[1])

        assert len(event.event.keys()) == 2
        assert event.value(self.X) == self.X.domain[1]
        assert event.value(self.Y) == self.Y.domain[1]

    def eventRemoveVar_test_7(self):
        """
        Test setValue method
        """

        event = Event(var=self.X, val=self.X.domain[0])
        event.removeVar(self.X)
        event.removeVar(self.Y)  # Already not in event
        assert not event.varInEvent(self.X)
        assert not event.varInEvent(self.Y)

    def eventIter_test_8(self):
        """
        Test iteration
        """

        tlist = [
            (self.X, self.X.domain[0]),
            (self.Y, self.Y.domain[0]),
            (self.Z, self.Z.domain[0]),
        ]
        event = Event(tlist=tlist)

        iter_res = [i for i in event]

        for i in range(len(tlist)):
            if (
                tlist[i][0].name != iter_res[i][0].name
                and tlist[i][1] != iter_res[i][1]
            ):
                assert False

        assert True

    def eventEqual_test_9(self):
        """
        Test if two equal event are actually equal
        """

        tlist1 = [(self.X, self.X.domain[0])]
        tlist2 = [(self.X, self.X.domain[0]), (self.Y, self.Y.domain[0])]
        tlist3 = [(self.Y, self.Y.domain[0]), (self.X, self.X.domain[0])]

        event1a = Event(tlist=tlist1)
        event1b = Event(tlist=tlist1)

        event2a = Event(tlist=tlist2)
        event2b = Event(tlist=tlist2)
        event2c = Event(tlist=tlist3)

        assert event1a == event1b
        assert event2a == event2b
        assert event2a == event2c

    def eventEqual_test_10(self):
        """
        Test when two event are different in their values, one variable
        """

        tlist1 = [(self.X, self.X.domain[0])]
        tlist2 = [(self.X, self.X.domain[1])]

        event1 = Event(tlist=tlist1)
        event2 = Event(tlist=tlist2)

        assert event1 != event2

    def eventNotEqual_test_11(self):
        """
        Test when two event are different in their values, two variables
        """

        tlist1 = [(self.X, self.X.domain[0]), (self.Y, self.Y.domain[0])]
        tlist2 = [(self.X, self.X.domain[1]), (self.Y, self.Y.domain[0])]
        tlist3 = [(self.Y, self.Y.domain[0]), (self.X, self.X.domain[1])]

        event1 = Event(tlist=tlist1)
        event2 = Event(tlist=tlist2)
        event3 = Event(tlist=tlist3)

        assert event1 != event2
        assert event1 != event3

    def eventNotEqual_test_12(self):
        """
        Test when variables in events are not the same, one variable
        """

        tlist1 = [(self.X, self.X.domain[0])]
        tlist2 = [(self.Y, self.Y.domain[0])]

        event1 = Event(tlist=tlist1)
        event2 = Event(tlist=tlist2)

        assert event1 != event2

    def eventNotEqual_test_13(self):
        """
        Test when variables in events are not the same, two variables
        """

        tlist1 = [(self.X, self.X.domain[0]), (self.Y, self.Y.domain[0])]
        tlist2 = [(self.X, self.X.domain[0]), (self.Z, self.Z.domain[0])]

        event1 = Event(tlist=tlist1)
        event2 = Event(tlist=tlist2)

        assert event1 != event2
