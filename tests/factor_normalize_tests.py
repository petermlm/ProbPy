from nose.tools import with_setup, nottest

from tests.test_base import TestBase


class TestFactorNormalize(TestBase):
    def normalize_test_0(self):
        """
        X, f(X)
        """

        res = self.X_factor_n.normalize(self.X)
        assert(res.rand_vars == [self.X] and
               res.values == [1/3, 2/3])

        res = self.X_factor_n.normalize()
        assert(res.rand_vars == [self.X] and
               res.values == [1/3, 2/3])

    def normalize_test_1(self):
        """
        X, f(X, Y)
        """

        res = self.XY_factor_n.normalize(self.X)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/2, 1/2, 2/4, 2/4])

    def normalize_test_2(self):
        """
        Y, f(X, Y)
        """

        res = self.XY_factor_n.normalize(self.Y)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/3, 1/3, 2/3, 2/3])

    def normalize_test_3(self):
        """
        X, Y, f(X, Y)
        """

        res = self.XY_factor_n.normalize([self.X, self.Y])
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/6, 1/6, 2/6, 2/6])

        res = self.XY_factor_n.normalize()
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/6, 1/6, 2/6, 2/6])

    def normalize_test_4(self):
        """
        X, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize(self.X)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/2, 1/2, 2/4, 2/4, 3/6, 3/6, 4/8, 4/8])

    def normalize_test_5(self):
        """
        Y, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize(self.Y)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/3, 1/3, 2/3, 2/3, 3/7, 3/7, 4/7, 4/7])

    def normalize_test_6(self):
        """
        Z, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize(self.Z)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/4, 1/4, 2/6, 2/6, 3/4, 3/4, 4/6, 4/6])

    def normalize_test_6(self):
        """
        X, Y, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize([self.X, self.Y])
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/6, 1/6, 2/6, 2/6, 3/20, 3/20, 4/20, 4/20])

    def normalize_test_6(self):
        """
        X, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize([self.X, self.Z])
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/8, 1/12, 2/8, 2/12, 3/8, 3/12, 4/8, 4/12])

    def normalize_test_6(self):
        """
        Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize([self.Y, self.Z])
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/10, 1/10, 2/10, 2/10, 3/10, 3/10, 4/10, 4/10])

    def normalize_test_7(self):
        """
        X, Y, Z, f(X, Y, Z)
        """

        res = self.XYZ_factor_n.normalize([self.X, self.Y, self.Z])
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/20, 1/20, 2/20, 2/20, 3/20, 3/20, 4/20, 4/20])

        res = self.XYZ_factor_n.normalize()
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/20, 1/20, 2/20, 2/20, 3/20, 3/20, 4/20, 4/20])
