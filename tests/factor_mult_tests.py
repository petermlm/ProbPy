from nose.tools import with_setup, nottest

from tests.test_base import TestBase


class TestFactorMult(TestBase):
    def mult_test_0(self):
        """
        f(X), scalar
        """

        res = [
            self.X_factor.mult(self.scalar),
            self.X_factor.mult(self.scalarf),
            self.scalarf.mult(self.X_factor),
        ]

        for i in res:
            assert i.rand_vars == [self.X] and i.values == [10, 20]

    def mult_test_1(self):
        """
        f(X, Y), scalar
        """

        res = [
            self.XY_factor.mult(self.scalar),
            self.XY_factor.mult(self.scalarf),
            self.scalarf.mult(self.XY_factor),
        ]

        for i in res:
            assert i.rand_vars == [self.X, self.Y] and i.values == [10, 20, 30, 40]

    def mult_test_2(self):
        """
        f(X, Y, Z), scalar
        """

        res = [
            self.XYZ_factor.mult(self.scalar),
            self.XYZ_factor.mult(self.scalarf),
            self.scalarf.mult(self.XYZ_factor),
        ]

        for i in res:
            assert i.rand_vars == [self.X, self.Y, self.Z] and i.values == [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
            ]

    def mult_test_3(self):
        """
        f(X), f(X)
        """

        res = self.X_factor.mult(self.X_factor)
        assert res.rand_vars == [self.X] and res.values == [1, 4]

    def mult_test_4(self):
        """
        f(X), f(Y)
        """

        res = self.X_factor.mult(self.Y_factor)
        assert res.rand_vars == [self.X, self.Y] and res.values == [3, 6, 4, 8]

    def mult_test_5(self):
        """
        f(X, Y) f(X)
        """

        res = self.XY_factor.mult(self.X_factor)
        assert res.rand_vars == [self.X, self.Y] and res.values == [1, 4, 3, 8]

    def mult_test_6(self):
        """
        f(X, Y) f(Y)
        """

        res = self.XY_factor.mult(self.Y_factor)
        assert res.rand_vars == [self.X, self.Y] and res.values == [3, 6, 12, 16]

    def mult_test_7(self):
        """
        f(X, Y) f(Z)
        """

        res = self.XY_factor.mult(self.Z_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z] and res.values == [
            5,
            10,
            15,
            20,
            6,
            12,
            18,
            24,
        ]

    def mult_test_8(self):
        """
        f(X, Y) f(X, Y)
        """

        res = self.XY_factor.mult(self.XY_factor)
        assert res.rand_vars == [self.X, self.Y] and res.values == [1, 4, 9, 16]

    def mult_test_9(self):
        """
        f(X, Y) F(X, Z)
        """

        res = self.XY_factor.mult(self.XZ_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z] and res.values == [
            5,
            12,
            15,
            24,
            7,
            16,
            21,
            32,
        ]

    def mult_test_10(self):
        """
        f(X, Y) f(Z, W)
        """

        res = self.XY_factor.mult(self.ZW_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z, self.W]

        # fmt: off
        assert res.values == [9, 18, 27, 36,
                              10, 20, 30, 40,
                              11, 22, 33, 44,
                              12, 24, 36, 48]
        # fmt: on

    def mult_test_11(self):
        """
        f(X, Y, Z) f(X, Y, Z)
        """

        res = self.XYZ_factor.mult(self.XYZ_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z]

        # fmt: off
        assert res.values == [1, 4, 9, 16,
                              25, 36, 49, 64]
        # fmt: on

    def mult_test_12(self):
        """
        f(X, Y, Z) f(X, Y, W)
        """

        res = self.XYZ_factor.mult(self.XYW_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z, self.W]

        # fmt: off
        assert res.values == [9, 20, 33, 48,
                              45, 60, 77, 96,
                              13, 28, 45, 64,
                              65, 84, 105, 128]
        # fmt: on

    def mult_test_13(self):
        """
        f(X, Y, Z) f(X, K, W)
        """

        res = self.XYZ_factor.mult(self.XKW_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z, self.K, self.W]

        # fmt: off
        assert res.values == [17, 36, 51, 72,
                              85, 108, 119, 144,
                              19, 40, 57, 80,
                              95, 120, 133, 160,

                              21, 44, 63, 88,
                              105, 132, 147, 176,
                              23, 48, 69, 96,
                              115, 144, 161, 192]
        # fmt: on

    def mult_test_14(self):
        """
        f(X, Y, Z) f(T, K, W)
        """

        res = self.XYZ_factor.mult(self.TKW_factor)
        assert res.rand_vars == [self.X, self.Y, self.Z, self.T, self.K, self.W]

        # fmt: off
        assert res.values == [25, 50, 75, 100,
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
                              160, 192, 224, 256]
        # fmt: on
