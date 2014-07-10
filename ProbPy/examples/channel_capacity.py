"""
In this example an implementation for the Blahut-Arimoto algorithm is shown.
The algorithm calculates the channel capacity for a given channel and is
implemented using ProbPy
"""

from ProbPy.prob.rand_var import RandVar
from ProbPy.prob.factor import Factor
from ProbPy.prob.inf_theory import *

import math
import random


def ChannelCapacity(Input, Output, Prior, Channel, base=2, delta=0.01):
    """
    Implementation of Blahut-Arimoto algorithm for Channel Capacity computation

    :param Input:   Input variable of channel
    :param Output:  Output variable of channel
    :param Prior:   Prior distribution for computation
    :param Channel: Factor that represents the probability transition matrix of
                    the channel
    :param base:    Base of logarithms and exponentials
    :param delta:   Maximum error for algorithms halt
    :returns:       Channel capacity as computed by the algorithm
    """

    p = Prior

    while True:
        # Compute cj value
        f = (p * Channel).marginal(Output)
        l = (Channel / f).log(2)
        cj = (Channel * l).marginal(Input).exp(2)

        # Calculate limits
        il = (p * cj).marginal([]).log(2)
        iu = math.log(max(cj.values), 2)

        # Check if the algorithm should stop
        if iu-il.values[0] < delta:
            break

        # Prepare for next step
        p = p * (cj / (p * cj).marginal(Input))

    # Return the only value in lower limit's factor
    return il.values[0]


def ex1():
    """
    Example of the Channel Capacity algorithm applied to a binary symmetric
    channel. Such channels have an explicit way to have their channel capacity
    computed. Which is:

        C = 1 - H(p),

    where p is the probability of error in the channel:

           p
        0 --- 0
          \ / 1-p
           \
          / \ 1-p
        1 --- 1
           p

    In this example the probability of error is 0.1
    """

    p = 0.9

    Input = RandVar("Input", ["T", "F"])
    Output = RandVar("Output", ["T", "F"])

    Prior = Factor(Input, [0.5, 0.5])
    Channel = Factor([Input, Output], [p, 1-p, 1-p, p])

    cc = ChannelCapacity(Input, Output, Prior, Channel)
    explicit = 1 - entropy(Factor(Input, [p, 1-p]))

    print("Channel Capacity of a binary symmetric channel")
    print("Blahut-Arimoto:", cc)
    print("Explicit:      ", explicit)


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


if __name__ == "__main__":
    ex1()
    ex2()
    ex3()
