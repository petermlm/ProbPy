from nose.tools import with_setup, nottest

from tests.par_test_base import ParTestBase


class TestParMarginalMult(ParTestBase):
    def marginal_test_0(self):
        """
        X, f(X)
        """

        res = self.X_factor.marginal(self.X)
        par_res = self.X_par_factor.marginal(self.X)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_1(self):
        """
        X, f(Y)
        """

        res = self.X_factor.marginal(self.X)
        par_res = self.X_par_factor.marginal(self.X)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_2(self):
        """
        X, f(X, Y)
        """

        res = self.XY_factor.marginal(self.X)
        par_res = self.XY_par_factor.marginal(self.X)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_3(self):
        """
        Y, f(X, Y)
        """

        res = self.XY_factor.marginal(self.Y)
        par_res = self.XY_par_factor.marginal(self.Y)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_4(self):
        """
        X, Y, f(X, Y)
        """

        res = self.XY_factor.marginal([self.X, self.Y])
        par_res = self.XY_par_factor.marginal([self.X, self.Y])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_5(self):
        """
        Z, f(X, Y)
        """

        res = self.XY_factor.marginal([self.X, self.Y])
        par_res = self.XY_par_factor.marginal([self.X, self.Y])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_6(self):
        """
        X, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.X)
        par_res = self.XYZ_par_factor.marginal(self.X)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_7(self):
        """
        Y, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.Y)
        par_res = self.XYZ_par_factor.marginal(self.Y)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_8(self):
        """
        Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal(self.Z)
        par_res = self.XYZ_par_factor.marginal(self.Z)
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_9(self):
        """
        X, Y, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Y])
        par_res = self.XYZ_par_factor.marginal([self.X, self.Y])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_10(self):
        """
        X, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Z])
        par_res = self.XYZ_par_factor.marginal([self.X, self.Z])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_11(self):
        """
        Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.Y, self.Z])
        par_res = self.XYZ_par_factor.marginal([self.Y, self.Z])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values

    def marginal_test_12(self):
        """
        X, Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor.marginal([self.X, self.Y, self.Z])
        par_res = self.XYZ_par_factor.marginal([self.X, self.Y, self.Z])
        assert res.rand_vars == par_res.rand_vars and res.values == par_res.values
