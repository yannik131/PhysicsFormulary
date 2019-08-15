"""
The Variable module.
"""

from MathObject import *
from Units import *

class Variable(MathObject):

    """
    The Variable class is used to store (physical) variables in an object.
    """

    def __init__(self, unit: Unit, *args):
        """
        Creates a variable.
        :param unit: Unit of this variable.
        :param args: Passed to MathObject.
        """
        super().__init__(*args)
        self.unit = unit

class Constant(Variable):

    """
    Constants represent (physical) variables that will most likely not change in the future.
    """

    def __init__(self, value, *args):
        """
        Creates a constant.
        :param value: The permanent value of the constant.
        :param args: Passed to MathObject
        """
        super().__init__(*args)
        self.value = value
        self.__locked = True

    def __setattr__(self, key, value):
        """
        Utilizes the __setattr__ method to make the constant immutable.
        :param key: Name of the variable to change.
        :param value: Value of the assignment.
        :return: Nothing.
        """
        if self.__dict__.get("_Constant__locked", False) and key == "value":
            raise AttributeError("Trying to assign to a constant!")
        self.__dict__[key] = value
