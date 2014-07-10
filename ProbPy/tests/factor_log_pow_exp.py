from nose.tools import with_setup, nottest

from ProbPy.tests.test_base import TestBase
import math


class TestFactorLPE(TestBase):
    def lpe_test_log_0(self):
        """
        log(f(X), 2)
        log(f(X), 10)
        log(f(X), e)
        """

        res_2 = self.X_factor.log(2)
        res_10 = self.X_factor.log(10)
        res_e = self.X_factor.log(math.e)

        s = len(self.X_factor.values)

        assert(res_2.values == list(map(math.log, self.X_domain, [2]*s)) and
               res_2.rand_vars == [self.X])

        assert(res_10.values == list(map(math.log, self.X_domain, [10]*s)) and
               res_10.rand_vars == [self.X])

        assert(res_e.values == list(map(math.log, self.X_domain, [math.e]*s))
               and res_e.rand_vars == [self.X])

    def lpe_test_log_1(self):
        """
        log(f(X, Y), 2)
        log(f(X, Y), 10)
        log(f(X, Y), e)
        """

        res_2 = self.XY_factor.log(2)
        res_10 = self.XY_factor.log(10)
        res_e = self.XY_factor.log(math.e)

        s = len(self.XY_factor.values)

        assert(res_2.values == list(map(math.log, self.XY_domain, [2]*s)) and
               res_2.rand_vars == [self.X, self.Y])

        assert(res_10.values == list(map(math.log, self.XY_domain, [10]*s)) and
               res_10.rand_vars == [self.X, self.Y])

        assert(res_e.values == list(map(math.log, self.XY_domain, [math.e]*s))
               and res_e.rand_vars == [self.X, self.Y])

    def lpe_test_log_2(self):
        """
        log(f(X, Y, Z), 2)
        log(f(X, Y, Z), 10)
        log(f(X, Y, Z), e)
        """

        res_2 = self.XYZ_factor.log(2)
        res_10 = self.XYZ_factor.log(10)
        res_e = self.XYZ_factor.log(math.e)

        s = len(self.XYZ_factor.values)

        assert(res_2.values == list(map(math.log, self.XYZ_domain, [2]*s)) and
               res_2.rand_vars == [self.X, self.Y, self.Z])

        assert(res_10.values == list(map(math.log, self.XYZ_domain, [10]*s))
               and res_10.rand_vars == [self.X, self.Y, self.Z])

        assert(res_e.values == list(map(math.log, self.XYZ_domain, [math.e]*s))
               and res_e.rand_vars == [self.X, self.Y, self.Z])

    def lpe_test_pow_0(self):
        """
        pow(f(X), 2)
        pow(f(X), 10)
        pow(f(X), e)
        """

        res_2 = self.X_factor.pow(2)
        res_10 = self.X_factor.pow(10)
        res_e = self.X_factor.pow(math.e)

        s = len(self.X_factor.values)

        assert(res_2.values == list(map(math.pow, self.X_domain, [2]*s)) and
               res_2.rand_vars == [self.X])

        assert(res_10.values == list(map(math.pow, self.X_domain, [10]*s)) and
               res_10.rand_vars == [self.X])

        assert(res_e.values == list(map(math.pow, self.X_domain, [math.e]*s))
               and res_e.rand_vars == [self.X])

    def lpe_test_pow_1(self):
        """
        pow(f(X, Y), 2)
        pow(f(X, Y), 10)
        pow(f(X, Y), e)
        """

        res_2 = self.XY_factor.pow(2)
        res_10 = self.XY_factor.pow(10)
        res_e = self.XY_factor.pow(math.e)

        s = len(self.XY_factor.values)

        assert(res_2.values == list(map(math.pow, self.XY_domain, [2]*s)) and
               res_2.rand_vars == [self.X, self.Y])

        assert(res_10.values == list(map(math.pow, self.XY_domain, [10]*s)) and
               res_10.rand_vars == [self.X, self.Y])

        assert(res_e.values == list(map(math.pow, self.XY_domain, [math.e]*s))
               and res_e.rand_vars == [self.X, self.Y])

    def lpe_test_pow_2(self):
        """
        pow(f(X, Y, Z), 2)
        pow(f(X, Y, Z), 10)
        pow(f(X, Y, Z), e)
        """

        res_2 = self.XYZ_factor.pow(2)
        res_10 = self.XYZ_factor.pow(10)
        res_e = self.XYZ_factor.pow(math.e)

        s = len(self.XYZ_factor.values)

        assert(res_2.values == list(map(math.pow, self.XYZ_domain, [2]*s)) and
               res_2.rand_vars == [self.X, self.Y, self.Z])

        assert(res_10.values == list(map(math.pow, self.XYZ_domain, [10]*s))
               and res_10.rand_vars == [self.X, self.Y, self.Z])

        assert(res_e.values == list(map(math.pow, self.XYZ_domain, [math.e]*s))
               and res_e.rand_vars == [self.X, self.Y, self.Z])

    def lpe_test_exp_0(self):
        """
        exp(f(X))
        """

        res = self.X_factor.exp()
        assert(res.values == list(map(math.exp, self.X_domain)) and
               res.rand_vars == [self.X])

    def lpe_test_exp_1(self):
        """
        exp(f(X, Y))
        """

        res = self.XY_factor.exp()
        assert(res.values == list(map(math.exp, self.XY_domain)) and
               res.rand_vars == [self.X, self.Y])

    def lpe_test_exp_2(self):
        """
        exp(f(X, Y, Z))
        """

        res = self.XYZ_factor.exp()
        assert(res.values == list(map(math.exp, self.XYZ_domain)) and
               res.rand_vars == [self.X, self.Y, self.Z])
