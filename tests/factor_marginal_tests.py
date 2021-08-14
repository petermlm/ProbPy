from nose.tools import with_setup, nottest

from tests.test_base import TestBase


class TestMarginalMult(TestBase):
    def marginal_test_0(self):
        """
        X, f(X)
        """

        res = self.X_factor.marginal(self.X)
        assert res.rand_vars == [self.X] and res.values == [1, 2]

    def marginal_test_1(self):
        """
        X, f(Y)
        """

        res = self.X_factor.marginal(self.X)
        assert res.rand_vars == [self.X] and res.values == [1, 2]

    def marginal_test_2(self):
        """
        X, f(X, Y)
        """

        res = self.XY_factor.marginal(self.X)
        assert res.rand_vars == [self.X] and res.values == [4, 6]

    def marginal_test_3(self):
        """
        Y, f(X, Y)
        """

        res = self.XY_factor.marginal(self.Y)
        assert res.rand_vars == [self.Y] and res.values == [3, 7]

    def marginal_test_4(self):
        """
        X, Y, f(X, Y)
        """

        res = self.XY_factor.marginal([self.X, self.Y])
        assert res.rand_vars == [self.X, self.Y] and res.values == [1, 2, 3, 4]

    def marginal_test_5(self):
        """
        Z, f(X, Y)
        """

        res = self.XY_factor.marginal([self.X, self.Y])
        assert res.rand_vars == [self.X, self.Y] and res.values == [1, 2, 3, 4]

    def marginal_test_6(self):
        """
        X, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.X)
        assert res.rand_vars == [self.X] and res.values == [16, 20]

    def marginal_test_7(self):
        """
        Y, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.Y)
        assert res.rand_vars == [self.Y] and res.values == [14, 22]

    def marginal_test_8(self):
        """
        Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.Z)
        assert res.rand_vars == [self.Z] and res.values == [10, 26]

    def marginal_test_9(self):
        """
        X, Y, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Y])
        assert res.rand_vars == [self.X, self.Y] and res.values == [6, 8, 10, 12]

    def marginal_test_10(self):
        """
        X, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Z])
        assert res.rand_vars == [self.X, self.Z] and res.values == [4, 6, 12, 14]

    def marginal_test_11(self):
        """
        Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.Y, self.Z])
        assert res.rand_vars == [self.Y, self.Z] and res.values == [3, 7, 11, 15]

    def marginal_test_12(self):
        """
        X, Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Y, self.Z])
        assert res.rand_vars == [self.X, self.Y, self.Z] and res.values == list(
            range(1, 9)
        )
