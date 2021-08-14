A Python library for discrete multi variable probabilistic calculus.

# About ProbPy

ProbPy is a Python library that aims at simplifying calculations with discrete multi variable probabilistic distributions by offering an abstraction over how data is stored and how the operations between distributions are performed.

The library can be used in the implementation of many algorithms such as Bayes Theorem, Bayesian Inference algorithms like Variable Elimination, Gibbs Ask (MCMC), HMMs implementations, Information Theory, etc.

Hosted at [GitHub](https://github.com/petermlm/ProbPy).

# Example and Features

With ProbPy you can work with factors that represent probability distributions. First define the Random Variables:

    X = RandVar("X", ["A", "B", "C"])
    Y = RandVar("Y", ["True", "False"])

The first argument of the constructor is the name of the variable and the second is its domain. After that, the factors representing probability distributions can be declared.

    fy = Factor(Y, [0.2, 0.8])
    fx_y = Factor([X, Y], [[0.1, 0.4, 0.5],
                           [0.5, 0.1, 0.4]])

Above, the first factor corresponds to a distribution `P(Y)` and the second to a distribution `P(X | Y)`. The first argument is the list of variables, or single variable, indexing the factor. The second argument are the values of that factor. Note that the values of second factor `fx_y`, are inserted using a list of lists. The rightmost variable `Y` indexes the outer list, variable `X` indexes the inner list.

Having this, you can calculate the product of those distribution to get the join `P(X, Y)`. This can be done either using a method of one of the factors or using the `*` operator, which will yield the same result:

    fyx = fx_y * fy
    fyx = fx_y.mult(fy)

These operations and others can be used to implement more complex operations, for example, the Bayes theorem:

    fy_x = (fx_y * fy).normalize(Y)

The line above first calculates the factor `P(X, Y)` and normalize it to Y to yield `P(Y | X)`. Another way to calculate the same result would be to do:

    fyx = fx_y * fy
    fy_x = fyx / fyx.marginal(X)

The `marginal` method calculates the marginal distribution `P(X)` from `P(X, Y)`.

Among other features, factors can also have some variables initialized. Suppose the factor `P(X, Y, Z)` in which every variable is binary and an event `X=True`, `Z=False`. You can initialize this variables to get a factor only over `Y`.

    X = RandVar("X", ["T", "F"])
    Y = RandVar("Y", ["T", "F"])
    Z = RandVar("Z", ["T", "F"])

    fxyz = Factor([X, Y, Z], [
        # Z = True
        [[10, 20],
         [30, 40]],

        # Z = False
        [[50, 60],
         [70, 80]]])

    e = Event()
    e.setValue(X, "T")
    e.setValue(Z, "F")

    fy = fxyz.instVar(e)
    print(fy.values)  # [50, 70]

In the code above you will see the Event class being used to create an event. The factor `fxyz` has it's variables `x` and `z` instantiated yielding another factor that only has the `y` variable.

The library has the `RandVar` and `Factor` classes as seen above. It also has the `BayesianNetwork` class that represents a Bayesian Network and has a few inference algorithms implemented, like the Gibbs Ask algorithm.

**To see examples check the examples directory. To get a full list of features of this library check the documentation provided in this repository. Remeber to execute the examples from the parent directory if ProbPy is not installed, like the following:**

    python3 examples/earthquake.py

# Installing

To install ProbPy from the Python Package Index use *pip*:

    pip install ProbPy

Alternatively, download ProbPy from GitHub and install with the following commands:

    git clone https://github.com/petermlm/ProbPy
    python setup.py install

If you are developing ProbPy, instead of installing the library use the following commands so you don't have to reinstall ProbPy every time an alteration is made:

    git clone https://github.com/petermlm/ProbPy
    python setup.py develop

# Tests

ProbPy uses nose for testing. Install nose either in a virtual env or globally and run:

    nosetests

# Style

ProbPy uses [Python Black](https://github.com/psf/black) for auto formatting.
However, several lines in the examples and tests will have a comment so black
doesn't format lines like this:

   values == [9, 18, 27, 36,
              10, 20, 30, 40,
              11, 22, 33, 44,
              12, 24, 36, 48]

Since it is useful to see matrices in such a form.

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

# Contributing

* This project is implemented using Python 3.2. Earlier versions of python are not supported.

* The project uses [PEP8](http://legacy.python.org/dev/peps/pep-0008) as a style guide. The tool [autopep8](https://pypi.python.org/pypi/autopep8/) may help in assuring the project follows the standards.

* The code should have tests. Every test is implemented in the `ProbPy/test` directory and [nosetests](https://nose.readthedocs.org/en/latest/) is used run them. To run the tests use `nosetests3 ProbPy/test`.

* The code should be documented. Documentation is done using Sphinx which takes the doc strings of the code and produces the documentation or it is written directly when needed.

# FAQ

**Q: What is the main problem that ProbPy tries to solve? Why was it developed?**

The aim of ProbPy is to offer a simple way to work with random variables, discrete probability distributions and factors of the form `P(X, Y, Z | W)`, `f(A, B, C)`, and use them to implement probabilistic calculations like Bayes Theorem, Graphical Models such as Bayesian Networks, Bayesian Inference algorithms, Fuzzy Logic operations, Information Theory calculations, among other things.

The library provides an abstraction that makes it possible for the user to work with the distributions, factors, algorithms, etc, without having to know how they are implemented.

**Q: Who is developing ProbPy and why did development started?**

The original author, and current administrator, started developing ProbPy to implement a few probabilistic algorithms for his Master's Degree Thesis. The project started growing and it was made into an Open Source Project.

**Q: Is this project comparable in any way to Numpy?**

No. Numpy can represent multidimensional matrices and implements a lot of algebraic operations using them. But this library uses its own representation of factors and such representation makes it simple to have factors with an arbitrary number of random variables (dimensions) and makes it easy to implement operations between them. Numpy could not be simply used to implement those operations, and hence, would not bring anything helpful to this project.

**Q: Can I use Numpy and ProbPy in the same project.**

Yes but not directly, meaning that a ProbPy factor can't be directly multiplied with a NumPy array, or a NumPy function cannot be directly used with a ProbPy object, and vice versa. Both library can be use without any conflicts.

**Q: Does the project use any other library in its implementation?**

No. Pretty much every operations and algorithms implemented in ProbPy comes down to the ability of relating an arbitrarily big factor with another, that is, doing multiplication between factors, like `f(X, Y, i, j) f(A, B, i, j) = f(X, Y, A, B, i, j)`. The data structure and algorithms that allows this are implemented directly in Python and no other library is used because they would not help in this specific representation.

**Q: What are the dependencies of ProbPy?**

For usage, just Python 3.2. For development, see the *Contributing* section.

**Q: Can ProbPy be used for very large quantities of data? Is it efficient in doing so?**

ProbPy is of course built to be as efficient as possible, but being a project that is still in it's infancy there are a lot of details that were made to be more maintainable then efficient. With this in mind note that there are a lot of improvements that can be made in regards to efficiency, like implementing certain operations using a parallel approach, implementing certain operations in C, rewriting some methods to be more efficient, among others.

If execution time and resource consumption is crucial for your project, you might be better off implementing your specific data structures and algorithms instead of using a general purpose library such as ProbPy. If an implementation is done for a specific problem it's bound to be more efficient then a library.

# To Do List

* A tutorial in the documentation!!

* Implement Likelihood Weighting algorithm.

* Implement Undirected Graphical Models and inference algorithms.

* Missing documentation that is anything other then what comes out of docstrings.

* The factorOp method in the Factor class:
 * Could be implemented using a parallel approach.
 * Shouldn't take a function as an argument. It should be equal everywhere instead of the last cycle, where it should implement a function for each operation.

* Implement indexed random variables to represent distributions like P(X\_t | X\_{t-1}) make operations with these distributions simpler to implement (Forward algorithm with HMMs, and similar operations)
