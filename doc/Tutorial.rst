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

What is a factor
++++++++++++++++

A factor may be defined and understood in many ways. It can be understood as a multi-dimensional matrix, a function that maps the values of a random variable to a real value, a probability distribution, or another number of abstractions done over a similar structure.

A first approach in understanding a factor deals with probability distributions. Supposing binary variable X which has a domain of either True or False. Let us now consider a distribution over that variable P(X) for which we assign the following probabilities::

    P(X=True)  = 0.8,
    P(X=False) = 0.2.

To represent this distribution in ProbPy the X variable needs to be defined first. Defining that variable can be done with the following::

    X = RandVar("X", ["True"], ["False"])

Once the variable is defined, the factor is defined like the following::

    fX = Factor(X, [0.8, 0.2])

The line above creates a factor of X, meaning that the value X=True will be mapped to 0.8, and X=False will be mapped to 0.2. Like this the factor represents a probability distribution, but it doesn't necessarily has to. The same line can be used to simply create a factor that mappes the values of X to any other value::

    fX = Factor(X, [8000, 2000])

ProbPy implements factors in such a way that their usage is possible across a variety of contexts. Their underlying structure is always the same and the way operations are implemented is also always the same. To know more about the details of how factor are implemented in ProbPy read `these three blog posts <http://petermlm.wordpress.com/2014/07/19/188/>`_.

Constructor
+++++++++++

The constructor of the Factor class can be used in many ways. The simplest way is the one displayed above, in which the factor will only map one variable. But what about multiple variables. It is done like the following::

    X = RandVar("X", ["True", "False"])
    Y = RandVar("Y", ["A", "B", "C"])
    fXY = Factor([X, Y], [[0.1, 0.9], [0.5, 0.5], [0.9, 0.1]])

The first argument is now a list of variables in the factor. The second argument is now a list of list. This list of list is indexed by the variables in the first argument. The innermost lists are indexed by the first variable, X. The outermost list is index by the second variable, Y.

This notion can be generalized for more variables, suppose a factor with three variables::

    X = RandVar("X", ["True", "False"])
    Y = RandVar("Y", ["A", "B", "C"])
    Z = RandVar("Z", ["Up", "Down"])
    fXY = Factor([X, Y, Z], [[[0.1, 0.9], [0.5, 0.5], [0.9, 0.1]],
                             [[0.4, 0.6], [0.5, 0.5], [0.6, 0.4]]])

In this example the innermost list is indexed by X, followed by the "middle" list indexed by Y, and finally the outermost list index by Z.

In alternative to having lists of lists the constructor supports a flatten list as argument::

    l = [0.1, 0.9, 0.5, 0.5, 0.9, 0.1, 0.4, 0.6, 0.5, 0.5, 0.6, 0.4]
    fXY = Factor([X, Y, Z], l)

Defining a list like this may be more confusing for a user, but it may be better if the list is defined using some computational method. Using any method, the final representation will always be a flatten list.

Factor Operation
++++++++++++++++

TODO

Marginal
++++++++

TODO

Normalization
+++++++++++++

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
