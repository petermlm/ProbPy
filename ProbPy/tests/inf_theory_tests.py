from nose.tools import with_setup, nottest, assert_almost_equal

from ProbPy.tests.test_base import TestBase

from ProbPy import RandVar, Factor, entropy

import math


class TestInfTheoryValue(TestBase):
    def __init__(self):
        TestBase.__init__(self)

        # factors for information theory testing
        self.fX1 = Factor(self.X, [0.5, 0.5])
        self.fX2 = Factor(self.X, [0.0, 1.0])
        self.fX3 = Factor(self.X, [1.0, 0.0])

        self.fXY1 = Factor([self.X, self.Y], [0.25, 0.25, 0.25, 0.25])
        self.fXY2 = Factor([self.X, self.Y], [0.1, 0.2, 0.3, 0.4])
        self.fXY3 = Factor([self.X, self.Y], [0.4, 0.3, 0.2, 0.1])

    def inf_theory_test_0(self):
        """
        H(X)
        """

        assert_almost_equal(entropy(self.fX1), 1.0, places=1)
        assert_almost_equal(entropy(self.fX1, 10), 0.30103, places=5)
        assert_almost_equal(entropy(self.fX1, math.e), 0.69315, places=5)

        assert_almost_equal(entropy(self.fX2), 0.0, places=1)
        assert_almost_equal(entropy(self.fX2, 10), 0.0, places=1)
        assert_almost_equal(entropy(self.fX2, math.e), 0.0, places=1)

        assert_almost_equal(entropy(self.fX3), 0.0, places=1)
        assert_almost_equal(entropy(self.fX3, 10), 0.0, places=1)
        assert_almost_equal(entropy(self.fX3, math.e), 0.0, places=1)

    def inf_theory_test_1(self):
        """
        H(X, Y)
        """

        assert_almost_equal(entropy(self.fXY1), 2.0, places=1)
        assert_almost_equal(entropy(self.fXY1, 10), 0.60206, places=5)
        assert_almost_equal(entropy(self.fXY1, math.e), 1.3863, places=4)

        assert_almost_equal(entropy(self.fXY2), 1.8464, places=4)
        assert_almost_equal(entropy(self.fXY2, 10), 0.55583, places=5)
        assert_almost_equal(entropy(self.fXY2, math.e), 1.2799, places=4)

        assert_almost_equal(entropy(self.fXY3), 1.8464, places=4)
        assert_almost_equal(entropy(self.fXY3, 10), 0.55583, places=5)
        assert_almost_equal(entropy(self.fXY3, math.e), 1.2799, places=4)
