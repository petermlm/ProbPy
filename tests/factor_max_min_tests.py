from nose.tools import with_setup, nottest

from tests.test_base import TestBase
from ProbPy import Factor, Event


class TestFactorMaxMin(TestBase):
    def max_test_0(self):
        """
        Maximum with one variable
        """

        for i, domain in enumerate(self.X.domain):
            fac = Factor(self.X, [1, 2])
            fac.values[i] = 10

            assert fac.max() == 10

    def max_test_1(self):
        """
        Maximum with two variables
        """

        for i, domainx in enumerate(self.X.domain):
            for j, domainy in enumerate(self.Y.domain):
                fac = Factor([self.X, self.Y], [1, 2, 3, 4])
                fac.values[i + j * 2] = 10

                assert fac.max() == 10

    def min_test_2(self):
        """
        Minimum with one variable
        """

        for i, domain in enumerate(self.X.domain):
            fac = Factor(self.X, [1, 2])
            fac.values[i] = -10

            assert fac.min() == -10

    def min_test_3(self):
        """
        Minimum with two variables
        """

        for i, domainx in enumerate(self.X.domain):
            for j, domainy in enumerate(self.Y.domain):
                fac = Factor([self.X, self.Y], [1, 2, 3, 4])
                fac.values[i + j * 2] = -10

                assert fac.min() == -10

    def argmax_test_4(self):
        """
        Maximum argument with one variable
        """

        for i, domain in enumerate(self.X.domain):
            fac = Factor(self.X, [1, 2])
            fac.values[i] = 10

            event = Event([(self.X, domain)])
            assert fac.argmax() == event

    def argmax_test_5(self):
        """
        Maximum argument with two variables
        """

        for i, domainx in enumerate(self.X.domain):
            for j, domainy in enumerate(self.Y.domain):
                fac = Factor([self.X, self.Y], [1, 2, 3, 4])
                fac.values[i + j * 2] = 10

                event = Event([(self.X, domainx), (self.Y, domainy)])
                assert fac.argmax() == event

    def argmin_test_6(self):
        """
        Minimum argument with one variable
        """

        for i, domain in enumerate(self.X.domain):
            fac = Factor(self.X, [1, 2])
            fac.values[i] = -10

            event = Event([(self.X, domain)])
            assert fac.argmin() == event

    def argmin_test_7(self):
        """
        Minimum argument with two variables
        """

        for i, domainx in enumerate(self.X.domain):
            for j, domainy in enumerate(self.Y.domain):
                fac = Factor([self.X, self.Y], [1, 2, 3, 4])
                fac.values[i + j * 2] = -10

                event = Event([(self.X, domainx), (self.Y, domainy)])
                assert fac.argmin() == event
