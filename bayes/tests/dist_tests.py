from bayes.bayes.dist import *
from bayes.bayes.bn import *
from nose.tools import with_setup, nottest

class TestDist:
    def setUp(self):
        # Scalar
        self.scalar = dist.Dist([], [10])

        # Binary variables
        self.X = dist.RandVar("X", ["T", "F"])
        self.Y = dist.RandVar("Y", ["T", "F"])
        self.Z = dist.RandVar("Z", ["T", "F"])
        self.W = dist.RandVar("W", ["T", "F"])
        self.K = dist.RandVar("K", ["T", "F"])
        self.T = dist.RandVar("T", ["T", "F"])

        # Distributions
        self.X_dist = dist.Dist([self.X], range(1, 3))
        self.Y_dist = dist.Dist([self.Y], range(3, 5))
        self.Z_dist = dist.Dist([self.Z], range(5, 7))

        self.XY_dist = dist.Dist([self.X, self.Y], range(1, 5))
        self.XZ_dist = dist.Dist([self.X, self.Z], range(5, 9))
        self.ZW_dist = dist.Dist([self.Z, self.W], range(9, 13))

        self.XYZ_dist = dist.Dist([self.X, self.Y, self.Z], range(1, 9))
        self.XYW_dist = dist.Dist([self.X, self.Y, self.W], range(9, 17))
        self.XKW_dist = dist.Dist([self.X, self.K, self.W], range(17, 25))
        self.TKW_dist = dist.Dist([self.T, self.K, self.W], range(25, 33))

    def tearDown(self):
        pass

    def mult_test_0(self):
        """
        f(X), scalar
        """

        res = self.scalar.mult(self.X_dist)
        assert(res.rand_vars == [self.X] and \
                res.values == [10, 20])

    def mult_test_1(self):
        """
        f(X, Y), scalar
        """

        res = self.scalar.mult(self.XY_dist)
        assert(res.rand_vars == [self.X, self.Y] and \
                res.values == [10, 20, 30, 40])

    def mult_test_2(self):
        """
        f(X, Y, Z), scalar
        """

        res = self.scalar.mult(self.XYZ_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and \
                res.values == [
                    10, 20, 30, 40,
                    50, 60, 70, 80])

    def mult_test_3(self):
        """
        f(X), f(X)
        """

        res = self.X_dist.mult(self.X_dist)
        assert(res.rand_vars == [self.X] and \
                res.values == [1, 4])

    def mult_test_4(self):
        """
        f(X), f(Y)
        """

        res = self.X_dist.mult(self.Y_dist)
        assert(res.rand_vars == [self.X, self.Y] and \
                res.values == [3, 6, 4, 8])

    def mult_test_5(self):
        """
        f(X, Y) f(X)
        """

        res = self.XY_dist.mult(self.X_dist)
        assert(res.rand_vars == [self.X, self.Y] and \
                res.values == [1, 4, 3, 8])

    def mult_test_6(self):
        """
        f(X, Y) f(Y)
        """

        res = self.XY_dist.mult(self.Y_dist)
        assert(res.rand_vars == [self.X, self.Y] and \
                res.values == [3, 6, 12, 16])

    def mult_test_7(self):
        """
        f(X, Y) f(Z)
        """

        res = self.XY_dist.mult(self.Z_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and \
                res.values == [
                    5, 10, 15, 20,
                    6, 12, 18, 24])

    def mult_test_8(self):
        """
        f(X, Y) f(X, Y)
        """

        res = self.XY_dist.mult(self.XY_dist)
        assert(res.rand_vars == [self.X, self.Y] and \
                res.values == [1, 4, 9, 16])

    def mult_test_9(self):
        """
        f(X, Y) F(X, Z)
        """

        res = self.XY_dist.mult(self.XZ_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and \
                res.values == [
                    5, 12, 15, 24,
                    7, 16, 21, 32])

    def mult_test_10(self):
        """
        f(X, Y) f(Z, W)
        """

        res = self.XY_dist.mult(self.ZW_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.W] and \
                res.values == [
                    9, 18, 27, 36,
                    10, 20, 30, 40,
                    11, 22, 33, 44,
                    12, 24, 36, 48])

    def mult_test_11(self):
        """
        f(X, Y, Z) f(X, Y, Z)
        """

        res = self.XYZ_dist.mult(self.XYZ_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z] and \
                res.values == [
                    1, 4, 9, 16,
                    25, 36, 49, 64])

    def mult_test_12(self):
        """
        f(X, Y, Z) f(X, Y, W)
        """

        res = self.XYZ_dist.mult(self.XYW_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.W] and \
                res.values == [
                    9, 20, 33, 48,
                    45, 60, 77, 96,
                    13, 28, 45, 64,
                    65, 84, 105, 128])

    def mult_test_13(self):
        """
        f(X, Y, Z) f(X, K, W)
        """

        res = self.XYZ_dist.mult(self.XKW_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.K, self.W] and \
                res.values == [
                    17, 36, 51, 72,
                    85, 108, 119, 144,
                    19, 40, 57, 80,
                    95, 120, 133, 160,

                    21, 44, 63, 88,
                    105, 132, 147, 176,
                    23, 48, 69, 96,
                    115, 144, 161, 192])

    def mult_test_14(self):
        """
        f(X, Y, Z) f(T, K, W)
        """

        res = self.XYZ_dist.mult(self.TKW_dist)
        assert(res.rand_vars == [self.X, self.Y, self.Z, self.T, self.K, self.W] and \
                res.values == [
                    25, 50, 75, 100,
                    125, 150, 175, 200,
                    26, 52, 78, 104,
                    130, 156, 182, 208,

                    27, 54, 81, 108,
                    135, 162, 189, 216,
                    28, 56, 84, 112,
                    140, 168, 196, 224,

                    29, 58, 87, 116,
                    145, 174, 203, 232,
                    30, 60, 90, 120,
                    150, 180, 210, 240,

                    31, 62, 93, 124,
                    155, 186, 217, 248,
                    32, 64, 96, 128,
                    160, 192, 224, 256])

