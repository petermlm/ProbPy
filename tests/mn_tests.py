from nose.tools import with_setup, nottest, assert_almost_equal

from ProbPy import RandVar, Factor, MarkovNetwork


class TestMarkovNetwork:
    """
    The ep values are used for the different tests. ep_tree_res is used to
    compare the results from inference in tree networks. The results should be
    similar up to the last few digits because, in trees, inference not an
    approximation.

    For loops, ep_loop_calc is used during calculation, but comparing the
    values to its brute force version will always carry a bigger error. To
    compare the values ep_loop_res is used.
    """

    def __init__(self):
        self.ep_tree_res = 0.0000001
        self.ep_loop_res = 0.01
        self.ep_loop_calc = 0.00001

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
        self.f_v2 = Factor(self.v2, list(range(1, 3)))
        self.f_v3 = Factor(self.v3, list(range(1, 3)))
        self.f_v4 = Factor(self.v4, list(range(1, 3)))
        self.f_v5 = Factor(self.v5, list(range(1, 3)))
        self.f_v6 = Factor(self.v6, list(range(1, 3)))
        self.f_v7 = Factor(self.v7, list(range(1, 3)))
        self.f_v8 = Factor(self.v8, list(range(1, 3)))

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

    def compare_results(self, tree, bf, MN):
        for i in bf.rand_vars:
            bf_res = bf.marginal(i).normalize()
            mn_res = MN.var_nodes[i.name].marginal
            dist = bf_res.euclideanDist(mn_res)
            print(bf_res, mn_res, dist)
            if tree:
                assert(dist < self.ep_tree_res)
            else:
                assert(dist < self.ep_loop_res)

    def compare_networks(self, tree, net1, net2):
        for i in net1.var_nodes:
            f1 = net1.var_nodes[i].marginal
            f2 = net2.var_nodes[i].marginal
            dist = f1.euclideanDist(f2)
            print(f1, f2, dist)
            if tree:
                assert(dist < self.ep_tree_res)
            else:
                assert(dist < self.ep_loop_res)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v1_v3

        # Compare results
        self.compare_results(False, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4

        # Compare results
        self.compare_results(False, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v2_v3 * self.f_v1_v4 * self.f_v2_v5 * \
            self.f_v3_v6 * self.f_v4_v5 * self.f_v5_v6

        # Compare results
        self.compare_results(False, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2_v3 * self.f_v1_v2_v3_v4 * self.f_v4_v5_v6

        # Compare results
        self.compare_results(False, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f2_v1_v2 * self.f3_v1_v2

        # Compare results
        self.compare_results(False, bf, MN)

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
        self.compare_results(True, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4

        # Compare results
        self.compare_results(False, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v4 * \
            self.f_v1_v2_v3_v4

        # Compare results
        self.compare_results(False, bf, MN)

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
        MN.BeliefPropagation(ep=self.ep_loop_calc)

        # Make brute force
        bf = self.f_v1_v2 * self.f_v1_v3 * self.f_v2_v4 * self.f_v3_v5 * \
            self.f_v4_v5

        # Compare results
        self.compare_results(False, bf, MN)

    """
    Update belief
    """

    def mn_update_belief_test_0(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        f(v1) -- v1 -- f(v1, v2) -- v2
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v1])
        MN_update = MarkovNetwork(self.f_v1_v2)

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f_v1, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_1(self):
        """
        v1 -- f(v1, v2) -- v2

        ||
        \/

        f2(v1) ---
                 |
        f(v1) -- v1 -- f(v1, v2) -- v2
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v1, self.f2_v1])
        MN_update = MarkovNetwork(self.f_v1_v2)

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f_v1, tree=True)
        MN_update.updateBelief(self.f2_v1, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_2(self):
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
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v1, self.f2_v1,
                                self.f3_v1])
        MN_update = MarkovNetwork(self.f_v1_v2)

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f_v1, tree=True)
        MN_update.updateBelief(self.f2_v1, tree=True)
        MN_update.updateBelief(self.f3_v1, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_2(self):
        """
        f(v1) -- v1 -- f(v1, v2) -- v2

        ||
        \/

        f2(v1) ---
                 |
        f(v1) -- v1 -- f(v1, v2) -- v2
                 |
        f3(v1) ---
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v1, self.f2_v1,
                                self.f3_v1])
        MN_update = MarkovNetwork([self.f_v1_v2, self.f_v1])

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f2_v1, tree=True)
        MN_update.updateBelief(self.f3_v1, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_3(self):
        """
        f(v1) -- v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3

        ||
        \/

        f(v1) -- v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3 -- f(v3)
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1, self.f_v1_v2, self.f_v2_v3,
                                self.f_v3])
        MN_update = MarkovNetwork([self.f_v1, self.f_v1_v2, self.f_v2_v3])

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f_v3, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_4(self):
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

        ||
        \/

        f(v1)               f(v2)
        |                       |
        v1 -- f(v1, v2, v3) -- v2
                     |
                     |
                     v3
        f(v4)        |          f(v5)
        |            |              |
        v4 -- f(v3, v4, v5, v6) -- v5
                     |
                     |
                     v6
        f(v7)        |      f(v8)
        |            |          |
        v7 -- f(v6, v7, v8) -- v8
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2_v3, self.f_v3_v4_v5_v6,
                                self.f_v6_v7_v8,
                                self.f_v1, self.f_v2, self.f_v3, self.f_v4,
                                self.f_v5, self.f_v6, self.f_v7, self.f_v8])
        MN_update = MarkovNetwork([self.f_v1_v2_v3, self.f_v3_v4_v5_v6,
                                   self.f_v6_v7_v8])

        MN_all.BeliefPropagation(tree=True)
        MN_update.BeliefPropagation(tree=True)
        MN_update.updateBelief(self.f_v1, tree=True)
        MN_update.updateBelief(self.f_v2, tree=True)
        MN_update.updateBelief(self.f_v3, tree=True)
        MN_update.updateBelief(self.f_v4, tree=True)
        MN_update.updateBelief(self.f_v5, tree=True)
        MN_update.updateBelief(self.f_v6, tree=True)
        MN_update.updateBelief(self.f_v7, tree=True)
        MN_update.updateBelief(self.f_v8, tree=True)

        # Compare results
        self.compare_networks(True, MN_all, MN_update)

    def mn_update_belief_test_5(self):
        """
        |-- f2(v1, v2) --|
        |                |
        v1              v2
        |                |
        |-- f3(v1, v2) --|

        ||
        \/

                 |-- f2(v1, v2) --|
                 |                |
        f(v1) -- v1              v2
                 |                |
                 |-- f3(v1, v2) --|
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f2_v1_v2, self.f3_v1_v2,
                                self.f_v1])
        MN_update = MarkovNetwork([self.f2_v1_v2, self.f3_v1_v2])

        MN_all.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v1, ep=self.ep_loop_calc)

        # Compare results
        self.compare_networks(False, MN_all, MN_update)

    def mn_update_belief_test_6(self):
        """
        |-- f2(v1, v2) --|
        |                |
        v1              v2
        |                |
        |-- f3(v1, v2) --|

        ||
        \/

                 |-- f2(v1, v2) --|
                 |                |
        f(v1) -- v1              v2 -- f(v2)
                 |                |
                 |-- f3(v1, v2) --|
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f2_v1_v2, self.f3_v1_v2,
                                self.f_v1, self.f_v2])
        MN_update = MarkovNetwork([self.f2_v1_v2, self.f3_v1_v2])

        MN_all.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v1, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v2, ep=self.ep_loop_calc)

        # Compare results
        self.compare_networks(False, MN_all, MN_update)

    def mn_update_belief_test_7(self):
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

        f(v1)           f(v2)
        |                   |
        v1 -- f(v1, v2) -- v2
        |                   |
        |                   |
        f(v1, v3)   f(v2, v4)
        |                   |
        |                   |
        v3 -- f(v3, v4) -- v4
        |                   |
        f(v3)           f(v4)
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v1_v3,
                                self.f_v2_v4, self.f_v3_v4,
                                self.f_v1, self.f_v2, self.f_v3, self.f_v4])
        MN_update = MarkovNetwork([self.f_v1_v2, self.f_v1_v3,
                                   self.f_v2_v4, self.f_v3_v4])

        MN_all.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v1, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v2, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v3, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v4, ep=self.ep_loop_calc)

        # Compare results
        self.compare_networks(False, MN_all, MN_update)

    def mn_update_belief_test_8(self):
        """
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
        |                  |                   |
        |                  |                   |
        f(v1, v4)      f(v2, v5)       f(v3, v6)
        |                  |                   |
        |                  |                   |
        v4 -- f(v4, v5) -- v5 -- f(v5, v6) -- v6

        ||
        \/

        f(v1)             f(v2)            f(v3)
        |                  |                   |
        v1 -- f(v1, v2) -- v2 -- f(v2, v3) -- v3
        |                  |                   |
        |                  |                   |
        f(v1, v4)      f(v2, v5)       f(v3, v6)
        |                  |                   |
        |                  |                   |
        v4 -- f(v4, v5) -- v5 -- f(v5, v6) -- v6
        |                  |                   |
        f(v4)             f(v5)            f(v6)
        """

        # Make belief propagation
        MN_all = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v1_v4,
                                self.f_v2_v5, self.f_v3_v6, self.f_v4_v5,
                                self.f_v5_v6,
                                self.f_v1, self.f_v2, self.f_v3,
                                self.f_v4, self.f_v5, self.f_v6])
        MN_update = MarkovNetwork([self.f_v1_v2, self.f_v2_v3, self.f_v1_v4,
                                   self.f_v2_v5, self.f_v3_v6, self.f_v4_v5,
                                   self.f_v5_v6])

        MN_all.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.BeliefPropagation(ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v1, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v2, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v3, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v4, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v5, ep=self.ep_loop_calc)
        MN_update.updateBelief(self.f_v6, ep=self.ep_loop_calc)

        # Compare results
        self.compare_networks(False, MN_all, MN_update)
