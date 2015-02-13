from nose.tools import with_setup, nottest

from tests.par_test_base import ParTestBase
from ProbPy import RandVar, Factor, ParFactor


class TestFactorMult(ParTestBase):
    def __init__(self):
        super().__init__()

    def par_test_0(self):
        """
        f(X), scalar
        """

        for i in range(4):
            self.X_par_factor.setMaxDepth(i)

            res = [self.X_factor.mult(self.scalar),
                   self.X_factor.mult(self.scalarf),
                   self.scalarf.mult(self.X_factor)]

            par_res = [self.X_par_factor.mult(self.scalar),
                       self.X_par_factor.mult(self.par_scalarf),
                       self.par_scalarf.mult(self.X_par_factor)]

            for i, ele in enumerate(res):
                assert(ele.rand_vars == par_res[i].rand_vars and
                       ele.values == par_res[i].values)

    def par_test_1(self):
        """
        f(X, Y), scalar
        """

        for i in range(4):
            self.XY_par_factor.setMaxDepth(i)
            self.XY_par_factor.setMaxDepth(i)

            res = [self.XY_factor.mult(self.scalar),
                   self.XY_factor.mult(self.scalarf),
                   self.scalarf.mult(self.XY_factor)]

            par_res = [self.XY_par_factor.mult(self.scalar),
                       self.XY_par_factor.mult(self.par_scalarf),
                       self.par_scalarf.mult(self.XY_par_factor)]

            for i, ele in enumerate(res):
                assert(ele.rand_vars == par_res[i].rand_vars and
                       ele.values == par_res[i].values)

    def par_test_2(self):
        """
        f(X, Y, Z), scalar
        """

        for i in range(4):
            self.XYZ_par_factor.setMaxDepth(i)
            self.XYZ_par_factor.setMaxDepth(i)

            res = [self.XYZ_factor.mult(self.scalar),
                   self.XYZ_factor.mult(self.scalarf),
                   self.scalarf.mult(self.XYZ_factor)]

            par_res = [self.XYZ_par_factor.mult(self.scalar),
                       self.XYZ_par_factor.mult(self.par_scalarf),
                       self.par_scalarf.mult(self.XYZ_par_factor)]

            for i, ele in enumerate(res):
                assert(ele.rand_vars == par_res[i].rand_vars and
                       ele.values == par_res[i].values)

    def par_test_3(self):
        """
        f(X), f(X)
        """

        for i in range(4):
            self.X_par_factor.setMaxDepth(i)

            res = self.X_factor.mult(self.X_factor)
            par_res = self.X_par_factor.mult(self.X_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_4(self):
        """
        f(X), f(Y)
        """

        for i in range(4):
            self.X_par_factor.setMaxDepth(i)
            self.Y_par_factor.setMaxDepth(i)

            res = self.X_factor.mult(self.Y_factor)
            par_res = self.X_par_factor.mult(self.Y_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_5(self):
        """
        f(X, Y) f(X)
        """

        for i in range(4):
            self.X_par_factor.setMaxDepth(i)
            self.XY_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.X_factor)
            par_res = self.XY_par_factor.mult(self.X_par_factor)
            print(i)
            print(res)
            print(par_res)
            print("----")
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_6(self):
        """
        f(X, Y) f(Y)
        """

        for i in range(4):
            self.Y_par_factor.setMaxDepth(i)
            self.XY_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.Y_factor)
            par_res = self.XY_par_factor.mult(self.Y_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_7(self):
        """
        f(X, Y) f(Z)
        """

        for i in range(4):
            self.Z_par_factor.setMaxDepth(i)
            self.XY_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.Z_factor)
            par_res = self.XY_par_factor.mult(self.Z_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_8(self):
        """
        f(X, Y) f(X, Y)
        """

        for i in range(4):
            self.XY_par_factor.setMaxDepth(i)
            self.XY_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.XY_factor)
            par_res = self.XY_par_factor.mult(self.XY_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_9(self):
        """
        f(X, Y) F(X, Z)
        """

        for i in range(4):
            self.XY_par_factor.setMaxDepth(i)
            self.XZ_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.XZ_factor)
            par_res = self.XY_par_factor.mult(self.XZ_par_factor)
            print(i)
            print(res)
            print(par_res)
            print("----")
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_10(self):
        """
        f(X, Y) f(Z, W)
        """

        for i in range(4):
            self.XY_par_factor.setMaxDepth(i)
            self.ZW_par_factor.setMaxDepth(i)

            res = self.XY_factor.mult(self.ZW_factor)
            par_res = self.XY_par_factor.mult(self.ZW_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_11(self):
        """
        f(X, Y, Z) f(X, Y, Z)
        """

        for i in range(4):
            self.XYZ_par_factor.setMaxDepth(i)
            self.XYZ_par_factor.setMaxDepth(i)

            res = self.XYZ_factor.mult(self.XYZ_factor)
            par_res = self.XYZ_par_factor.mult(self.XYZ_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_12(self):
        """
        f(X, Y, Z) f(X, Y, W)
        """

        for i in range(4):
            self.XYZ_par_factor.setMaxDepth(i)
            self.XYW_par_factor.setMaxDepth(i)

            res = self.XYZ_factor.mult(self.XYW_factor)
            par_res = self.XYZ_par_factor.mult(self.XYW_par_factor)
            print(i)
            print(res)
            print(par_res)
            print("----")
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_13(self):
        """
        f(X, Y, Z) f(X, K, W)
        """

        for i in range(4):
            self.XYZ_par_factor.setMaxDepth(i)
            self.XKW_par_factor.setMaxDepth(i)

            res = self.XYZ_factor.mult(self.XKW_factor)
            par_res = self.XYZ_par_factor.mult(self.XKW_par_factor)
            print(i)
            print(res)
            print(par_res)
            print("----")
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)

    def par_test_14(self):
        """
        f(X, Y, Z) f(T, K, W)
        """

        for i in range(4):
            self.XYZ_par_factor.setMaxDepth(i)
            self.TKW_par_factor.setMaxDepth(i)

            res = self.XYZ_factor.mult(self.TKW_factor)
            par_res = self.XYZ_par_factor.mult(self.TKW_par_factor)
            assert(res.rand_vars == par_res.rand_vars and
                   res.values == par_res.values)
