"""
The Equation module.
"""

from Variable import *

class Equation(MathObject):

    """
    The Equation class handles storing of single equations in an object.
    """

    def __init__(self, *args):
        """
        Constructs a new Equation-object.

        :param args: Passed to super
        """

        self.variableMapping = dict()

    def setVariable(self, sympyForm: str, variable: Variable):
        """
        Tells the equation what variables it's made of.
        Note: Not every variable-name is unique. For example, "m" could both characterize a mass or the magnetic
        quantum number. This is why setting the variables is necessary.
        :param sympyForm: Symbol of a variable in the equation.
        :param variable: Variable object to connect the variable symbol in the equation with.
        :return: Nothing.
        """
        if not sympyForm in self.sympyForm:
            raise AttributeError("Variable with name %s not in equation!" % name)
        self.variableMapping[sympyForm] = variable
