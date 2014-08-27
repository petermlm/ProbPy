from nose.tools import with_setup, nottest, assert_almost_equal

from tests.test_base import TestBase
from ProbPy import RandVar, Factor, entropy, kullbackLeiblerDistance
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

        self.P1 = Factor([self.X], [0.5, 0.5])
        self.Q1 = Factor([self.X], [0.9, 0.1])

        self.P2 = Factor([self.X, self.Y], [0.25, 0.25, 0.25, 0.25])
        self.Q2 = Factor([self.X, self.Y], [0.8, 0.05, 0.05, 0.8])

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

    def inf_theory_test_2(self):
        """
        KLD(P1 | Q1)
        """

        res = [kullbackLeiblerDistance(self.P1, self.Q1),
               kullbackLeiblerDistance(self.P1, self.Q1, 10),
               kullbackLeiblerDistance(self.P1, self.Q1, math.e)]

        assert_almost_equal(res[0], 0.73697, places=4)
        assert_almost_equal(res[1], 0.22185, places=4)
        assert_almost_equal(res[2], 0.51083, places=4)

    def inf_theory_test_3(self):
        """
        KLD(P2 | Q2)
        """

        res = [kullbackLeiblerDistance(self.P2, self.Q2),
               kullbackLeiblerDistance(self.P2, self.Q2, 10),
               kullbackLeiblerDistance(self.P2, self.Q2, math.e)]

        assert_almost_equal(res[0], 0.32193, places=4)
        assert_almost_equal(res[1], 0.09691, places=4)
        assert_almost_equal(res[2], 0.22314, places=4)

    def inf_theory_test_4(self):
        """
        KLD(Q1 | P1)
        """

        res = [kullbackLeiblerDistance(self.Q1, self.P1),
               kullbackLeiblerDistance(self.Q1, self.P1, 10),
               kullbackLeiblerDistance(self.Q1, self.P1, math.e)]

        assert_almost_equal(res[0], 0.53100, places=5)
        assert_almost_equal(res[1], 0.15985, places=5)
        assert_almost_equal(res[2], 0.36806, places=5)

    def inf_theory_test_5(self):
        """
        KLD(Q2 | P2)
        """

        res = [kullbackLeiblerDistance(self.Q2, self.P2),
               kullbackLeiblerDistance(self.Q2, self.P2, 10),
               kullbackLeiblerDistance(self.Q2, self.P2, math.e)]

        assert_almost_equal(res[0], 2.4527, places=4)
        assert_almost_equal(res[1], 0.73834, places=5)
        assert_almost_equal(res[2], 1.7001, places=4)
