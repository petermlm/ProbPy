from ProbPy.prob.rand_var import RandVar
from ProbPy.prob.factor import Factor
import math
import random


def ChannelCapacity(Input, Output, Prior, Channel, base=2, delta=0.01):
    p = Prior

    while True:
        f = (p * Channel).marginal(Output)
        l = (Channel / f).log(2)
        cj = (Channel * l).marginal(Input).exp(2)

        il = (p * cj).marginal([]).log(2)
        iu = math.log(max(cj.values), 2)

        if iu-il.values[0] < delta:
            break

        p = p * (cj / (p * cj).marginal(Input))

    return il.values[0]


def ex1():
    Input = RandVar("Input", ["T", "F"])
    Output = RandVar("Output", ["T", "F"])

    Prior = Factor(Input, [0.5, 0.5])
    Channel = Factor([Input, Output], [0.9, 0.1, 0.1, 0.9])

    print(ChannelCapacity(Input, Output, Prior, Channel))


def ex2():
    domain = [str(i) for i in range(2)]
    Input = RandVar("Input", domain)
    Output = RandVar("Output", domain)

    Prior = Factor(Input, [1.0 / 2.0] * 2)
    channel_dist = [random.random() for i in range(4)]
    Channel = Factor([Input, Output], channel_dist).normalize(Input)

    print(ChannelCapacity(Input, Output, Prior, Channel))


def ex3():
    domain = [str(i) for i in range(10)]
    Input = RandVar("Input", domain)
    Output = RandVar("Output", domain)

    Prior = Factor(Input, [1.0 / 10.0] * 10)
    channel_dist = [random.random() for i in range(100)]
    Channel = Factor([Input, Output], channel_dist).normalize(Input)

    print(ChannelCapacity(Input, Output, Prior, Channel))

ex1()
ex2()
ex3()
