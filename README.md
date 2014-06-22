A Python library for multi variable probabilistic calculus.

About Bayes (Name to Change)
============================

Bayes (name to change) is a Python library that aims to simplify calculations with multi variable probabilistic distributions by offering an abstraction over how the data is stored and how the operations between distributions are performed.

The library can be used in the implementation of many algorithms such as Bayesian Inference algorithms, Smoothing, Filtering, among other things.

Features
========

TODO

Examples
========

The following code creates binary random variables. The first argument of *RandVar* is the name of the variable and the second is it's domain.

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

In the current implementation a Bayesian network can be implemented simply with a list of tuples, where each tuple is a pair with a variable and a factor.

    network = [
        (mary,     factor_mary),
        (john,     factor_john),
        (alarm,    factor_alarm),
        (earthq,   factor_earthq),
        (burglary, factor_burglary)
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

Data Representation
===================

TODO

Contributing
============

TODO

