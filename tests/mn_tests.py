from nose.tools import with_setup, nottest, assert_almost_equal

from ProbPy import RandVar, Factor, MarkovNetwork


class TestMarkovNetwork:
    def __init__(self):
        self.ep = 0.1

        # Variables
        self.v1 = RandVar("V1", [0, 1])
        self.v2 = RandVar("V2", [0, 1])
        self.v3 = RandVar("V3", [0, 1])
        self.v4 = RandVar("V4", [0, 1])
        self.v5 = RandVar("V5", [0, 1])
        self.v6 = RandVar("V6", [0, 1])
        self.v7 = RandVar("V7", [0, 1])
        self.v8 = RandVar("V8", [0, 1])

        # Factors
        self.f_v1 = Factor(self.v1, list(range(1, 3)))
        self.f2_v1 = Factor(self.v1, list(range(1, 3)))
        self.f3_v1 = Factor(self.v1, list(range(1, 3)))
        self.f_v1_v2 = Factor([self.v1, self.v2], list(range(1, 5)))
        self.f2_v1_v2 = Factor([self.v1, self.v2], list(range(1, 5)))
        self.f3_v1_v2 = Factor([self.v1, self.v2], list(range(1, 5)))
        self.f_v1_v3 = Factor([self.v1, self.v3], list(range(1, 5)))
        self.f_v1_v4 = Factor([self.v1, self.v4], list(range(1, 5)))
        self.f_v2_v3 = Factor([self.v2, self.v3], list(range(1, 5)))
        self.f_v2_v4 = Factor([self.v2, self.v4], list(range(1, 5)))
        self.f_v2_v5 = Factor([self.v2, self.v5], list(range(1, 5)))
        self.f_v3_v4 = Factor([self.v3, self.v4], list(range(1, 5)))
        self.f_v3_v5 = Factor([self.v3, self.v5], list(range(1, 5)))
        self.f_v3_v6 = Factor([self.v3, self.v6], list(range(1, 5)))
        self.f_v4_v5 = Factor([self.v4, self.v5], list(range(1, 5)))
        self.f_v5_v6 = Factor([self.v5, self.v6], list(range(1, 5)))

        self.f_v1_v2_v3 = Factor([self.v1, self.v2, self.v3],
                                 list(range(1, 9)))
        self.f_v3_v4_v5 = Factor([self.v3, self.v4, self.v5],
                                 list(range(1, 9)))
        self.f_v4_v5_v6 = Factor([self.v3, self.v4, self.v5],
                                 list(range(1, 9)))
        self.f_v6_v7_v8 = Factor([self.v6, self.v7, self.v8],
                                 list(range(1, 9)))

        self.f_v1_v2_v3_v4 = Factor([self.v1, self.v2, self.v3, self.v4],
                                    list(range(1, 17)))
        self.f_v3_v4_v5_v6 = Factor([self.v3, self.v4, self.v5, self.v6],
                                    list(range(1, 17)))

    def compare_results(self, bf, MN):
        for i in bf.rand_vars:
            bf_res = bf.marginal(i).normalize()
            mn_res = MN.var_nodes[i.name].marginal
            print(bf_res, mn_res, bf_res.euclideanDist(mn_res))
            assert(bf_res.euclideanDist(mn_res) < self.ep)

    """
    Tree networks
    """

    def mn_tree_test_0(self):
        """
        v1 -- f(v1, v2) -- v2
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2)
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_1(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_2(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3 -- f(v3, v4) -- v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v3_v4])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v3_v4

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_3(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
                           |
                           |
                       f(v2, v4)
                           |
                           |
                           v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v2_v4])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v2_v4

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_4(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3 -- f(v3, v4) -- v4
                           |
                           |
                       f(v2, v5)
                           |
                           |
                           v5
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3,
                            self.f_v3_v4, self.f_v2_v5])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v3_v4 * self.f_v2_v5

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_5(self):
        """
        v1 -- f(v1, v2, v3) -- v2
                    |
                    |
                    v3
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2_v3)
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2_v3

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_6(self):
        """
        v1 -- f(v1, v2, v3) -- v2
                    |
                    |
                    v3
                    |
                    |
        v4 -- f(v3, v4, v5) -- v5
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2_v3, self.f_v3_v4_v5])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2_v3 * self.f_v3_v4_v5

        # Compare results
        self.compare_results(bf, MN)

    def mn_tree_test_7(self):
        """
        v1 -- f(v1, v2, v3) -- v2
                     |
                     |
                     v3
                     |
                     |
        v4 -- f(v3, v4, v5, v6) -- v5
                     |
                     |
                     v6
                     |
                     |
        v7 -- f(v6, v7, v8) -- v8
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2_v3, self.f_v3_v4_v5_v6,
                            self.f_v6_v7_v8])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2_v3 * self.f_v3_v4_v5_v6 * self.f_v6_v7_v8

        # Compare results
        self.compare_results(bf, MN)

    """
    Loop networks
    """

    def mn_loop_test_0(self):
        """
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v3)
        |                   |
        | ------ v3 ------- |
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v1_v3])
        MN.BeliefPropagation(ep=self.ep)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v1_v3

        # Compare results
        self.compare_results(bf, MN)

    def mn_loop_test_1(self):
        """
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3 -- f(v3, v4) -- v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v1_v3, self.f_v2_v4,
                            self.f_v3_v4])
        MN.BeliefPropagation(ep=self.ep)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4

        # Compare results
        self.compare_results(bf, MN)

    def mn_loop_test_2(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
        |                  |                   |
        |                  |                   |
        f(v1, v4)      f(v2, v5)       f(v3, v6)
        |                  |                   |
        |                  |                   |
        v4 -- f(v4, v5) -- v5 -- f(v5, v6) -- v6
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v1_v4,
                            self.f_v2_v5, self.f_v3_v6, self.f_v4_v5,
                            self.f_v5_v6])
        MN.BeliefPropagation(ep=self.ep)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v1_v4 * self.f_v2_v5 * \
            self.f_v3_v6 * self.f_v4_v5 * self.f_v5_v6

        # Compare results
        self.compare_results(bf, MN)

    def mn_loop_test_3(self):
        """
                        ------ v1                         v5
                      /        |                          |
        f(v1, v2, v3) -- V2 -- f(v1, v2, v3, v4) -- v4 -- f(v4, v5, v6)
                      \        |                          |
                        ------ v3                         v6
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2_v3, self.f_v1_v2_v3_v4,
                            self.f_v4_v5_v6])
        MN.BeliefPropagation(ep=self.ep)

        # Make brute force
        bf = self.f_v1_v2_v3 * self.f_v1_v2_v3_v4 * self.f_v4_v5_v6

        # Compare results
        self.compare_results(bf, MN)

    """
    Add new factor
    """

    def mn_add_new_factor_test_0(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        f(v1) -- v1 -- f(v1, v2) -- v2
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2)
        MN.addFactors(self.f_v1)
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1 * self.f_v1_v2

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_1(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        f2(v1) ---
                 |
        f(v1) -- v1 -- f(v1, v2) -- v2
                 |
        f3(v1) ---
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2)
        MN.addFactors([self.f_v1, self.f2_v1, self.f3_v1])
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1 * self.f2_v1 * self.f3_v1 * self.f_v1_v2

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_2(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        ----- f2(v1, v2) ----
        |                   |
        v1 -- f(v1, v2) -- v2
        |                   |
        ----- f3(v1, v2) ----
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2)
        MN.addFactors([self.f2_v1_v2, self.f3_v1_v2])
        MN.BeliefPropagation()

        # Make brute force
        bf = self.f_v1_v2 * self.f2_v1_v2 * self.f3_v1_v2

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_3(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
        """

        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        f(v1) -- v1 -- f(v1, v2) -- v2
        """

        # Make belief propagation
        MN = MarkovNetwork(self.f_v1_v2)
        MN.addFactors(self.f_v2_v3)
        MN.BeliefPropagation(tree=True)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_4(self):
        """
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3                 v4

        ||
        \/

        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3 -- f(v3, v4) -- v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v1_v3, self.f_v2_v4])
        MN.addFactors(self.f_v3_v4)
        MN.BeliefPropagation()

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_5(self):
        """
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3 -- f(v3, v4) -- v4

        ||
        \/

        v1 ------------ f(v1, v2) ------------ v2
        | \                                   / |
        |  ---------                 ---------  |
        |           \               /           |
        f(v1, v3)   f(v1, v2, v3, v4)   f(v2, v4)
        |           /               \           |
        |  ---------                 ---------  |
        | /                                   \ |
        v3 ------------ f(v3, v4) ------------ v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v1_v3,
                            self.f_v2_v4, self.f_v3_v4])
        MN.addFactors(self.f_v1_v2_v3_v4)
        MN.BeliefPropagation()

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4 * \
            self.f_v1_v2_v3_v4

        # Compare results
        self.compare_results(bf, MN)

    def mn_add_new_factor_test_6(self):
        """
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3                 v4

        ||
        \/

        v1 ----------- f(v1, v2) ------------ v2
        |                                      |
        |                                      |
        f(v1, v3)                      f(v2, v4)
        |                                      |
        |                                      |
        v3 -- f(v3, v5) -- v5 -- f(v4, v5) -- v4
        """

        # Make belief propagation
        MN = MarkovNetwork([self.f_v1_v2, self.f_v1_v3, self.f_v2_v4])
        MN.addFactors([self.f_v3_v5, self.f_v4_v5])
        MN.BeliefPropagation()

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v5 * \
            self.f_v4_v5

        # Compare results
        self.compare_results(bf, MN)
