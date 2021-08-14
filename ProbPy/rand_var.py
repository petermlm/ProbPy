"""
File that implements the RandVar (Random Variable) class
"""


import copy
import math


class RandVar:
    """
    Represents a Random Variable in a probability distribution. Each variable
    is identified by a string which is it's name. If two RandVar in a script
    have the same name, the library will assume they are the same variable.

    Each variable also has a domain. The domain is a list of values which the
    variable can take. As of this version the elements on the list should only
    be of the string type. In later versions other types will be allowed. Maybe
    even types that are other objects.

    :param name:   String or Int with the name of this variable
    :param domain: Either a list with the domain of this variable, in which the
                   elements in the domain should be strings, ints or booleans,
                   or an int number which will be the size of the domain

    Examples:
        >>> coin = RandVar("Coin", ["Head", "Tail"])
        >>> ball = RandVar("Ball", ["Red", "Green", "Blue"])
        >>> generic = RandVar(10, list(range(10)))
        >>> X = RandVar("X", 4)
        >>> Y = RandVar("Y")

    In the example, the X variable will have a domain like [0, 1, 2, 3]
    The Y variable will be a binary variable by default, with domain:

        >>> [True, False]

    Variables which name start with "_" are anonymous. They will always be
    different from other anonymous variables and from non anonymous variables.
    To create an anonymous the following two methods are valid:
        >>> Anon1 = RandVar("_anonymous", [True, False])
        >>> Anon2 = RandVar(domain=[True, False])
    """

    def __init__(self, name="_", domain=None):
        # Check the name
        if type(name) not in [str, int]:
            raise RandVarNameEx(name)

        # Check the domain
        if type(domain) == list and len(domain) > 0:
            for i in domain:
                if type(i) not in [str, int, bool]:
                    raise RandVarDomainEx(domain)

        elif type(domain) == int:
            domain = list(range(domain))

        elif domain is None:
            domain = [True, False]

        else:
            raise RandVarDomainEx(domain)

        # Store the attributes
        self.name = name
        self.domain = domain

    def equal(self, var):
        """
        Checks if the Random Variable in var is equal to self
        """

        # If this is an anonymous variable, they will always be different
        if self.name is None or self.name[0] == "_":
            return False

        # Check the name
        elif self.name != var.name:
            return False

        # Check the domain
        elif self.domain != var.domain:
            return False

        return True

    def __repr__(self):
        list_str = "["

        for i in self.domain[:-1]:
            list_str += str(i) + ", "
        list_str += str(self.domain[-1]) + "]"

        return "(%s, %s)" % (str(self.name), str(list_str))

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.equal(other)

    def __ne__(self, other):
        return not self.equal(other)

    def __hash__(self):
        return self.name.__hash__()


class RandVarNameEx(Exception):
    """Exception use for a bad Random Variable name"""

    def __init__(self, bad_name):
        self.bad_name = bad_name

    def __str__(self):
        return "Bad Random Variable name: %s" % repr(self.bad_name)


class RandVarDomainEx(Exception):
    """Exception use for a bad domain for a Variable"""

    def __init__(self, bad_domain):
        self.bad_domain = bad_domain

    def __str__(self):
        return "Bad Random Variable domain: %s" % repr(self.bad_domain)
