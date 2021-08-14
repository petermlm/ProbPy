"""
This module defines the Event class and the EventEle class.

The Event class specifies an instantiation of a set of Random Variables.
Supposing the binary random variables X, Y and Z, an event could be something
of the form (X=true, Y=true, Z=false).

In ProbPy the usage of the following construction is common:

    >>> event = [(var1, val1), (var2, val2), ..., (varn, valn)]

Like this an event would be a list where each element is a tuple pairing a
variable in it's first argument and a value in it's second argument. This class
abstracts this construction.

The EventEle class is a tuple in the list.
"""


from ProbPy import RandVar


class Event:
    """
    The Event class specifies an event in order of a set of random variables.
    Supposing the binary random variables X, Y and Z, an event could be
    something of the form (X=true, Y=true, Z=false).

    :param tlist: List of tuples with event. Each tuple should be a pair
                  between a variable and a value from the variable. Argument
                  used alone.
    :param var:   Random variable of event. Used with val argument.
    :param val:   Value of variable. Used with var argument.

    If the constructor is empty, this will be an empty event. If the tlist
    argument is used the event will be exactly like it. The tlist argument
    should be of the form:

        >>> tl = [(var1, val1), (var2, val2), ..., (varn, valn)]
        >>> e = Event(tlist=tl)

    Using the var and val arguments created an event with a single variable.

        >>> e = Event(var1, val1)

    An event can have other variables added to it after it's creation with the
    setValue() method. If a variable is set using this method and it already is
    in the event, the value will change.

        >>> e = Event(var1, val1)
        >>> e.setValue(var1, nval)
        >>> e.setValue(var2, val2)

    In this example the event will be: (var1=nval, var2=val2)
    """

    def __init__(self, tlist=None, var=None, val=None):
        if tlist is not None and type(tlist) is list:
            self.event = {i[0]: i[1] for i in tlist}

        elif var is not None or val is not None:
            self.event = {var: val}

        else:
            self.event = dict()

    def varInEvent(self, var):
        """
        Checks if a variable is present in the event, returning True if it is
        and False otherwise.

        :param var: Variable which is checked.
        """

        return var in self.event.keys()

    def value(self, var):
        """
        Returns the value of a variable in the event. Returns None if the
        variable is not in the event.

        :param var: Variable from which the value is checked.
        """

        if not self.varInEvent(var):
            return None

        return self.event[var]

    def setValue(self, var, val):
        """
        Sets the value of the variable in the event. If the variable is not
        present in the event, it added it to it.

        :param var: Random variable
        :param val: Value to be assign to the variable
        """

        self.event[var] = val

    def removeVar(self, var):
        """
        Removes variable from the event, if it exists

        :param var: Variable to be removed from event
        """

        if not self.varInEvent(var):
            return

        self.event.pop(var)

    def equal(self, other_event):
        # If the sizes of the events are not the same, they are not the same
        if len(self.event) != len(other_event.event):
            return False

        # Check if each variable is the same
        for i in self.event:
            if (
                i not in other_event.event.keys()
                or self.event[i] != other_event.event[i]
            ):
                return False

        return True

    def __iter__(self):
        """
        Allows iteration of an event. The following:

            >>> [i for i in event]

        Will yield a list with tuples of the form:

            >>> [(var1, val1),
                 (var2, val2),
                 ...,
            >>>  (varn, valn)]
        """

        for i in self.event:
            yield (i, self.event[i])

    def __eq__(self, other):
        return self.equal(other)
