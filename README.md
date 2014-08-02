A Python library for multi variable probabilistic calculus.

# About ProbPy

ProbPy is a Python library that aims to simplify calculations with multi variable probabilistic distributions by offering an abstraction over how the data is stored and how the operations between distributions are performed.

The library can be used in the implementation of many algorithms such as Bayesian Inference algorithms, Smoothing, Filtering, among other things.

# Features

With ProbPy you can work with probability distributions. First define the Random Variables:

    X = RandVar("X", ["T", "F"])
    Y = RandVar("Y", ["T", "F"])

After that, the factors representing probability distributions can be declared.

    fy = Factor(Y, [0.2, 0.8])
    fx_y = Factor([X, Y], [0.1, 0.9, 0.5, 0.5])

Above, the first factor corresponds to a distribution `P(Y)` and the second to a distribution `P(X | Y)`.

Having this you can calculate the product of those distribution to get the join `P(X, Y)`, and normalize that distribution to get `P(Y | X)`.

    fy_x = (fx_y * fy).normalize(Y)

This was the Bayes Theorem implemented using ProbPy. For more features check the examples and the documentation. The example can be executed with the commands:

    python3 -m ProbPy.examples.earthquake
    python3 -m ProbPy.examples.bayes_theorem

# Examples

This example is in the `example.py` file.

The following code creates binary random variables. The first argument of `RandVar` is the name of the variable and the second is it's domain.

    burglary = factor.RandVar("burglary", ["True", "False"])
    earthq = factor.RandVar("earthq", ["True", "False"])
    alarm = factor.RandVar("alarm", ["True", "False"])
    john = factor.RandVar("john", ["True", "False"])
    mary = factor.RandVar("mary", ["True", "False"])

Having the variables it is now possible to create factors with them. A factor is basically the information of a probability distribution, like P(X, Y | Z), but the notion of dependency just isn't shown, hence the corresponding factor would be f(X, Y, Z).

    factor_burglary = factor.Factor([burglary], [0.001, 0.999])
    factor_earthq = factor.Factor([earthq], [0.002, 0.998])
    factor_alarm = factor.Factor([alarm, earthq, burglary], [0.95, 0.05, 0.94, 0.06, 0.29, 0.71, 0.001, 0.999])
    factor_john = factor.Factor([john, alarm], [0.90, 0.10, 0.05, 0.95])
    factor_mary = factor.Factor([mary, alarm], [0.70, 0.30, 0.01, 0.99])

In the current implementation a Bayesian network can be implemented simply with a list of tuples, where each tuple is a pair with a variable, and a factor and a list of parents.

    network = [
        (earthq,   factor_earthq,   []),
        (alarm,    factor_alarm,    [earthq,  burglary]),
        (john,     factor_john,     [alarm]),
        (burglary, factor_burglary, []),
        (mary,     factor_mary,     [alarm])
    ]

    BN = bn.BayesianNetwork(network)

Finally the Elimination Ask algorithm can be called with a query variable and a few observations.

    # Calculates: P(Burglary | John=true, Mary=true)
    observed = [(john, "True"), (mary, "True")]
    burglary_k_john_mary = BN.eliminationAsk(burglary, observed)

    # Calculates: P(John | Burglary=true)
    observed = [(burglary, "True")]
    john_k_burglary = BN.eliminationAsk(john, observed)

The observations are a list of tuples. Each tuple is a pair between a variable and it's observation in a specific situation.

# Contributing

* This project is aimed to work with Python 3.

* The project uses [PEP8](http://legacy.python.org/dev/peps/pep-0008) as a style guide. The tool [autopep8](https://pypi.python.org/pypi/autopep8/) may help in assuring the project follows the standards.

* The code should have tests. Every test is implemented in the `bayes/test` directory an [nosetests](https://nose.readthedocs.org/en/latest/) is used run them. The run the tests use `nosetests3 bayes/test`.

* The code should be documented. Documentation is done using Sphinx or written by hand when needed.

# Documentation

Documentation is handled with Sphinx. To make the documentation in html execute the following inside the `doc` directory:

    make html

The built result will be in the following directory:

    doc/_build/html/index.html

Only the following files should go in the repository:

    docs/Makefile
    docs/conf.py
    docs/*.rst
    docs/make.bat

# To Do

* Implement indexed random variables to represent distributions like P(X\_t | X\_{t-1}).

* Implemented algorithm Elimination Ask should allow more then one query variable.

* Implement Rejection Sampling algorithm.

* Implement Likelihood Weighting algorithm.

* Implement Gibbs Sampling algorithm. (MCMC)

* Implement product rule for Dist class. (Where P(X | Y) P(Y) will yield P(X, Y))

* Implement construction of factor from multidimensional matrix

* Distribution class should check if it is a distribution if after it's construction the sum of it's values is equal to one. Note that with a distribution P(X | Y), the sum of every P(X | Y = y) should sum 1 for every values of y.

* Make method to create a distribution where the user only inputs part of the information and the rest is created automatically, like, with a binary variable X, the user would input P(X = True) = 0.8, and the P(X = False) = 0.2 would automatically be generated.

* Make method where a user makes a new factor but only puts part of the information. The values for the elements that were not inputed would remain with some default value. Like 0.

* The factorOp method in the Factor class:
 * Could be implemented using a parallel approach.
 * Shouldn't take a function as an argument. It should be equal everywhere instead of the last cycle, where it should implement a function for each operation.
