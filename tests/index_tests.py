from nose.tools import with_setup, nottest, assert_almost_equal

from ProbPy import RandVar, Factor, MarkovNetwork

class TestIndex:
    def __init__(self):
        # Variables
        self.v1 = RandVar("V1", [0, 1])
        self.v2 = RandVar("V2", [0, 1])
        self.v3 = RandVar("V3", [0, 1])
        self.v4 = RandVar("V4", [0, 1])

        # Factors
        self.f_v1_v2 = Factor([self.v1, self.v2], list(range(1, 5)))
        self.f_v2_v3 = Factor([self.v2, self.v3], list(range(1, 5)))
        self.f_v1_v3 = Factor([self.v1, self.v3], list(range(1, 5)))

    def index_factor_test_0(self):
        res_value = range(1, 5)
        for i, val in enumerate(self.f_v1_v2):
            assert(res_value[i] == val)

    def index_factor_test_1(self):
        res = self.f_v1_v2 * self.f_v2_v3

        res_value = [1, 2, 6, 8, 3, 6, 12, 16]
        for i, val in enumerate(res):
            assert(res_value[i] == val)

    def index_mn_test_0(self):
        MN = MarkovNetwork(self.f_v1_v2)
        MN.BeliefPropagation(tree=True)

        assert(MN["V1"] == MN.var_nodes["V1"].marginal)
        assert(MN["V2"] == MN.var_nodes["V2"].marginal)

    def index_mn_test_1(self):
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3])
        MN.BeliefPropagation(tree=True)

        assert(MN["V1"] == MN.var_nodes["V1"].marginal)
        assert(MN["V2"] == MN.var_nodes["V2"].marginal)
        assert(MN["V3"] == MN.var_nodes["V3"].marginal)

    def index_mn_test_2(self):
        MN = MarkovNetwork([self.f_v1_v2, self.f_v1_v3])
        MN.BeliefPropagation()

        assert(MN["V1"] == MN.var_nodes["V1"].marginal)
        assert(MN["V2"] == MN.var_nodes["V2"].marginal)
        assert(MN["V3"] == MN.var_nodes["V3"].marginal)
