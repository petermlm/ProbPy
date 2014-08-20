.. Written by Pedro Melgueira (petermlm) (pedromelgueira[at]gmail[dot]com)

ProbPy Tutorial
===============

Install
-------

TODO

Random Variables
----------------

ProbPy works with discrete random variables that are later used to define factors and events. A random variable, as described in ProbPy, has a name and a domain. The name of the variable is used to identify the variable. Its type is always *str*. The domain of the variable is a list which size must be greater than 0. Each element of that list is an element of the domain of the variable. The types of the elements in the domain may be *int* or *str*.

The following code shows examples of random variable declarations::

    X = RandVar("X", ["True", "False"])
    Y = RandVar("Y", ["a", "b", "c", "d", "e"])
    Z = RandVar("Z", [list(range(10))])

The *RandVar* class is the ProbPy class that represents a random variable. Its first argument is the name of the variable and its second argument is the list containing the domain.

The name of the variable is used to identify the variable. It might seem redundant to have a Python variable **X** and call that variable **X**, but what happens is that the random variables are placed in lists and also get copied to new factors which are created with the calculations. Maintaining the name as an attribute assures that they can be identified anytime regardless of the name of their Python container.

The domain of the variable needs to be a list of *int* elements or *str* elements. That list must have at least one element. Whether it makes sense or not to have a random variable with only one element in its domain is up to the user. The order of the domain's elements is going to be important as it will be seen in the part of this tutorial about factors, which follows.

In ProbPy, two variables are consider equal is both their name and their domain matches. Notice how four variables are compared to the first one in terms of being the same variable or not::

    X = RandVar("X", ["True", "False"])

    v1 = RandVar("X", ["True", "False"])
    v2 = RandVar("Y", ["True", "False"])
    v3 = RandVar("X", ["False", "True"])
    v4 = RandVar("Y", ["False", "True"])

    X == v1  # True. Same name and domain
    X == v2  # False. Name is not the same
    X == v3  # False. Domain is not the same
    X == v4  # False. Nothing is not the same

Factors
-------

TODO

Events
------

TODO

Bayesian Networks
-----------------

TODO

Information Theory
------------------

TODO
