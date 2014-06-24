from bayes.prob.bn import *
from nose.tools import with_setup, nottest

from bayes.tests.factor_base import FactorBase


class TestFactorExpectedValue(FactorBase):
    def expected_value_test_0(self):
        """
        E[X]
        """

        res = self.X_factor.expectedValue(self.X, self.x_ev)
        assert(res == 30)

    def expected_value_test_1(self):
        """
        E[X, Y]
        """

        res_xy = self.XY_factor.expectedValue([self.X, self.Y], self.xy_ev)
        assert(res_xy == 300)

    def expected_value_test_2(self):
        """
        E[X | Y] == E[X]
        """

        res_x = self.X_factor.expectedValue(self.X, self.x_ev)
        res_x_k_y = self.XY_factor.expectedValue(self.X, self.x_ev)
        assert(res_x == res_x_k_y == 30)

    def expected_value_test_3(self):
        """
        E[X]c == E[Xc]
        """

        c = 10
        fun = [i*c for i in self.x_ev]

        res_x_c = self.X_factor.expectedValue(self.X, self.x_ev) * c
        res_xc  = self.X_factor.expectedValue(self.X, fun)
        assert(res_x_c == res_xc)

    def expected_value_test_4(self):
        """
        E[X] + c == E[X + c]
        """

        c = 10
        fun = [i+c for i in self.x_ev]

        res_x_c = self.X_factor.expectedValue(self.X, self.x_ev) + c
        res_xc  = self.X_factor.expectedValue(self.X, fun)
        assert(res_x_c == res_xc)

    def expected_value_test_5(self):
        """
        E[X + Y] == E[X] + E[Y]
        """

        XY_local_factor = self.X_factor.mult(self.Y_factor)

        res_X = self.X_factor.expectedValue(self.X, self.x_ev)
        res_Y = self.Y_factor.expectedValue(self.Y, self.y_ev)
        res_XY = XY_local_factor.expectedValue([self.X, self.Y], self.xy_ev)
        assert(res_XY == res_X == res_Y)
