from nose.tools import with_setup, nottest

from tests.test_base import TestBase


class TestFactorMult(TestBase):
    def div_test_0(self):
        """
        f(X), scalar
        """

        res = [self.X_factor.div(self.scalar),
               self.X_factor.div(self.scalarf)]

        for i in res:
            assert(i.rand_vars == [self.X] and
                   i.values == [0.1, 0.2])

        res = self.scalarf.div(self.X_factor)
        assert(res.rand_vars == [self.X] and
               res.values == [10/1, 10/2])

    def div_test_1(self):
        """
        f(X, Y), scalar
        """

        res = [self.XY_factor.div(self.scalar),
               self.XY_factor.div(self.scalarf)]

        for i in res:
            assert(i.rand_vars == [self.X, self.Y] and
                   i.values == [0.1, 0.2, 0.3, 0.4])

        res = self.scalarf.div(self.XY_factor)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [10/1, 10/2, 10/3, 10/4])

    def div_test_2(self):
        """
        f(X, Y, Z), scalar
        """

        res = [self.XYZ_factor.div(self.scalar),
               self.XYZ_factor.div(self.scalarf)]

        for i in res:
            assert(i.rand_vars == [self.X, self.Y, self.Z] and
                   i.values == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])

        res = self.scalarf.div(self.XYZ_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [10/1, 10/2, 10/3, 10/4, 10/5, 10/6, 10/7, 10/8])

    def div_test_3(self):
        """
        f(X), f(X)
        """

        res = self.X_factor.div(self.X_factor)
        assert(res.rand_vars == [self.X] and
               res.values == [1, 1])

    def div_test_4(self):
        """
        f(X), f(Y)
        """

        res = self.X_factor.div(self.Y_factor)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/3, 2/3, 1/4, 2/4])

    def div_test_5(self):
        """
        f(X, Y) f(X)
        """

        res = self.XY_factor.div(self.X_factor)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/1, 2/2, 3/1, 4/2])

    def div_test_6(self):
        """
        f(X, Y) f(Y)
        """

        res = self.XY_factor.div(self.Y_factor)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1/3, 2/3, 3/4, 4/4])

    def div_test_7(self):
        """
        f(X, Y) f(Z)
        """

        res = self.XY_factor.div(self.Z_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/5, 2/5, 3/5, 4/5,
                              1/6, 2/6, 3/6, 4/6])

    def div_test_8(self):
        """
        f(X, Y) f(X, Y)
        """

        res = self.XY_factor.div(self.XY_factor)
        assert(res.rand_vars == [self.X, self.Y] and
               res.values == [1, 1, 1, 1])

    def div_test_9(self):
        """
        f(X, Y) F(X, Z)
        """

        res = self.XY_factor.div(self.XZ_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1/5, 2/6, 3/5, 4/6,
                              1/7, 2/8, 3/7, 4/8])

    def div_test_10(self):
        """
        f(X, Y) f(Z, W)
        """

        res = self.XY_factor.div(self.ZW_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.W] and
               res.values == [1/9, 2/9, 3/9, 4/9,
                              1/10, 2/10, 3/10, 4/10,
                              1/11, 2/11, 3/11, 4/11,
                              1/12, 2/12, 3/12, 4/12])

    def div_test_11(self):
        """
        f(X, Y, Z) f(X, Y, Z)
        """

        res = self.XYZ_factor.div(self.XYZ_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and
               res.values == [1, 1, 1, 1,
                              1, 1, 1, 1])

    def div_test_12(self):
        """
        f(X, Y, Z) f(X, Y, W)
        """

        res = self.XYZ_factor.div(self.XYW_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.W] and
               res.values == [1/9, 2/10, 3/11, 4/12,
                              5/9, 6/10, 7/11, 8/12,
                              1/13, 2/14, 3/15, 4/16,
                              5/13, 6/14, 7/15, 8/16])

    def div_test_13(self):
        """
        f(X, Y, Z) f(X, K, W)
        """

        res = self.XYZ_factor.div(self.XKW_factor)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.K, self.W] and
               res.values == [1/17, 2/18, 3/17, 4/18,
                              5/17, 6/18, 7/17, 8/18,
                              1/19, 2/20, 3/19, 4/20,
                              5/19, 6/20, 7/19, 8/20,

                              1/21, 2/22, 3/21, 4/22,
                              5/21, 6/22, 7/21, 8/22,
                              1/23, 2/24, 3/23, 4/24,
                              5/23, 6/24, 7/23, 8/24])

    def div_test_14(self):
        """
        f(X, Y, Z) f(T, K, W)
        """

        res = self.XYZ_factor.div(self.TKW_factor)
        assert(res.rand_vars == [
            self.X, self.Y, self.Z,
            self.T, self.K, self.W] and
            res.values == [1/25, 2/25, 3/25, 4/25,
                           5/25, 6/25, 7/25, 8/25,
                           1/26, 2/26, 3/26, 4/26,
                           5/26, 6/26, 7/26, 8/26,

                           1/27, 2/27, 3/27, 4/27,
                           5/27, 6/27, 7/27, 8/27,
                           1/28, 2/28, 3/28, 4/28,
                           5/28, 6/28, 7/28, 8/28,

                           1/29, 2/29, 3/29, 4/29,
                           5/29, 6/29, 7/29, 8/29,
                           1/30, 2/30, 3/30, 4/30,
                           5/30, 6/30, 7/30, 8/30,

                           1/31, 2/31, 3/31, 4/31,
                           5/31, 6/31, 7/31, 8/31,
                           1/32, 2/32, 3/32, 4/32,
                           5/32, 6/32, 7/32, 8/32])
