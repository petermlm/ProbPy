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

    Examples:
        >>> coin = RandVar("Coin", ["Head", "Tail"])
        >>> ball = RandVar("Ball", ["Red", "Green", "Blue"])
    """

    def __init__(self, name, domain):
        """
        :param name:   String with the name of this variable
        :param domain: List with the domain of this variable
        """

        if type(name) != str:
            raise RandVarNameEx(name)

        if type(domain) != list or len(domain) == 0:
            raise RandVarDomainEx(domain)

        for i in domain:
            if type(i) != str:
                raise RandVarDomainEx(domain)

        self.name = name
        self.domain = domain

    def __repr__(self):
        list_str = "["

        for i in self.domain[:-1]:
            list_str += i + ", "
        list_str += self.domain[-1] + "]"

        return "(" + self.name + ", " + list_str + ")"

    def __str__(self):
        return self.name


class RandVarNameEx(Exception):
    """ Exception use for a bad Random Variable name """

    def __init__(self, bad_name):
        self.bad_name = bad_name

    def __str__(self):
        return "Bad Random Variable name: " + repr(self.bad_name)


class RandVarDomainEx(Exception):
    """ Exception use for a bad domain for a Variable """

    def __init__(self, bad_domain):
        self.bad_domain = bad_domain

    def __str__(self):
        return "Bad Random Variable domain:" + repr(self.bad_domain)
