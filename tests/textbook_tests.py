from nose.tools import with_setup, nottest, assert_almost_equal

from ProbPy import RandVar, Factor, bn


class TestTextBook:
    def sprinkler_test_0(self):
        '''
        Simple network from "An introduction to graphical models" by Kevin P.
        Murphy
        C -> S
        C -> R
        S -> W
        R -> W
        '''
        C = RandVar("Cloudy", ["F", "T"])
        S = RandVar("Sprinkler", ["F", "T"])
        R = RandVar("Rain", ["F", "T"])
        W = RandVar("WetGrass", ["F", "T"])

        Cf = Factor([C], [0.5, 0.5])
        Sf = Factor([S, C], [0.5, 0.5,
                             0.9, 0.1])
        Rf = Factor([R, C], [0.8, 0.2,
                             0.2, 0.5])
        Wf = Factor([W, S, R], [1.0, 0.0,
                                0.1, 0.9,
                                0.1, 0.9,
                                0.01, 0.99])

        SprinklerNW = bn.BayesianNetwork([(C, Cf, []),
                                          (S, Sf, [C]),
                                          (R, Rf, [C]),
                                          (W, Wf, [S, R])])

        cases = [(W, 1, [(S, "T"), (R, "F")], 0.9)]

        for (qvar, qvalue, evidence, expect) in cases:
            result = SprinklerNW.eliminationAsk(qvar, evidence)
            print("qvar: %s\nevidence: %s\nexpect: %s\nresult: %s" %
                  (qvar.name,
                   ",".join(["%s=%s" % (x[0].name, x[1]) for x in evidence]),
                   expect,
                   result.values[qvalue]))
            assert_almost_equal(result.values[qvalue], expect, places=3)

    def student_test_0(self):
        '''
        Student network from "Probabilistic graphical models principles and
        techniques" by Koller and Friedman
        D -> G
        I -> G
        I -> S
        G -> L

        '''
        D = RandVar("Difficulty", ["easy", "hard"])
        I = RandVar("Intelligence", ["low", "high"])
        G = RandVar("Grade", ["a", "b", "c"])
        S = RandVar("SAT", ["low", "high"])
        L = RandVar("Letter", ["weak", "good"])

        Df = Factor([D], [0.6, 0.4])
        If = Factor([I], [0.7, 0.3])
        Gf = Factor([G, D, I], [0.30, 0.40, 0.30,
                                0.05, 0.25, 0.70,
                                0.90, 0.08, 0.02,
                                0.50, 0.30, 0.20])
        Sf = Factor([S, I], [0.95, 0.05,
                             0.2, 0.8])
        Lf = Factor([L, G], [0.1, 0.9,
                             0.4, 0.6,
                             0.99, 0.01])

        StudentNW = bn.BayesianNetwork([(D, Df, []),
                                        (I, If, []),
                                        (G, Gf, [D, I]),
                                        (S, Sf, [I]),
                                        (L, Lf, [G])])

        cases = [
            (L, 1, [(I, "low"), (D, "easy")], 0.513),
            (I, 1, [(L, "weak")], 0.140),
            (I, 1, [(G, "c"), (S, "high")], 0.578),
            (L, 1, [(I, "low")], 0.389),
            (I, 1, [(G, "c")], 0.079)
        ]

        for (qvar, qvalue, evidence, expect) in cases:
            result = StudentNW.eliminationAsk(qvar, evidence)
            print("qvar: %s\nevidence: %s\nexpect: %s\nresult: %s" %
                  (qvar.name,
                   ",".join(["%s=%s" % (x[0].name, x[1]) for x in evidence]),
                   expect,
                   result.values[qvalue]))
            assert_almost_equal(result.values[qvalue], expect, places=3)
