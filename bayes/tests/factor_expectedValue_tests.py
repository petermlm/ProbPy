from bayes.prob.bn import *
from nose.tools import with_setup, nottest, assert_almost_equal

from bayes.tests.factor_base import FactorBase


class TestFactorExpectedValue(FactorBase):
    def expected_value_test_0(self):
        """
        E[X]
        """

        res = self.X_dist.expectedValue(self.x_ev)
        assert_almost_equal(res, 12.0)

    def expected_value_test_1(self):
        """
        E[X, Y]
        """

        res_xy = self.XY_dist.expectedValue(self.xy_ev)
        assert_almost_equal(res_xy, 38.0)

    def expected_value_test_2(self):
        """
        E[X | Y] == E[X]
        """

        local_XY_dist = self.X_dist.mult(self.Y_dist)
        local_X_k_Y_dist = local_XY_dist.div(self.Y_dist)

        res_x_k_y = local_X_k_Y_dist.expectedValue(self.x_ev)
        res_x = self.X_dist.expectedValue(self.x_ev)
        assert_almost_equal(res_x_k_y, 12.0)
        assert_almost_equal(res_x, 12.0)

    def expected_value_test_3(self):
        """
        E[X]c == E[Xc]
        """

        c = 10
        fun = self.x_ev.mult(c)

        res_x_c = self.X_dist.expectedValue(self.x_ev) * c
        res_xc  = self.X_dist.expectedValue(fun)
        assert_almost_equal(res_x_c, res_xc)

    def expected_value_test_4(self):
        """
        E[X] + c == E[X + c]
        """

        c = 10
        fun = self.x_ev.add(c)

        res_x_c = self.X_dist.expectedValue(self.x_ev) + c
        res_xc  = self.X_dist.expectedValue(fun)
        assert_almost_equal(res_x_c, res_xc)

    def expected_value_test_5(self):
        """
        E[X + Y] == E[X] + E[Y]
        """

        XY_local_dist = self.X_dist.mult(self.Y_dist)

        res_X = self.X_dist.expectedValue(self.x_ev)
        res_Y = self.Y_dist.expectedValue(self.y_ev)
        res_XY = XY_local_dist.expectedValue(self.xy_ev)
        assert_almost_equal(res_XY, res_X + res_Y)
