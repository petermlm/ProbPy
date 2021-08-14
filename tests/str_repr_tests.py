from nose.tools import with_setup, nottest

from ProbPy import RandVar, Factor


class TestToString:
    def rand_var_test(self):
        r1 = RandVar(0, [0, 1])
        r2 = RandVar(0, ["ele0", "ele1"])
        r3 = RandVar("name", [0, 1])
        r4 = RandVar("name", ["ele0", "ele1"])

        assert r1.__repr__() == "(0, [0, 1])"
        assert r2.__repr__() == "(0, [ele0, ele1])"
        assert r3.__repr__() == "(name, [0, 1])"
        assert r4.__repr__() == "(name, [ele0, ele1])"

        assert r1.__str__() == "0"
        assert r2.__str__() == "0"
        assert r3.__str__() == "name"
        assert r4.__str__() == "name"

    def factor_test(self):
        X = RandVar("X", [0, 1])
        Y = RandVar("Y", [0, 1])

        f1 = Factor([], [0])
        f2 = Factor(X, [0, 1])
        f3 = Factor([X, Y], [0, 1, 2, 3])

        assert f1.__repr__() == "[0]"
        assert f2.__repr__() == "(X, [0, 1])"
        assert f3.__repr__() == "([X, Y], [0, 1, 2, 3])"
