from Metrology import *

class MathObject:

    def __init__(self, sympy_form: str, mathtext_form: str = None):

        """
        Creates a MathObject instance. This is the superclass of all the mathematical objects like equations,
        variables or units used in the formulary. It is saved twofold:
        1. as a SymPy-representation to handle the logic
        2. as a mathtext-string to display the equation with

        :param sympy_form: SymPy-representation of the MathObject
        :param mathtext_form: Text-representation that can be displayed using matplotlib.maththext
        :return: Returns nothing
        """

        self.sympy_form = sympy_form
        if mathtext_form is None:
            self.mathtext_form = sympy_form
        else:
            self.mathtext_form = mathtext_form

class Relation(MathObject):

    """
    The Relation class handles storing of single mathematical relations in an object. A relation is considered a
    mathematical term associating to mathematical objects in any way (i. e. an equation: a = b; a definition: a := b;
    a consequence: a = b => b = 4; etc.
    """

    def __init__(self, sympy_form: str, mathtext_form: str = None):
        """
        Constructs a new Equation-object.

        :param args: Passed to super
        """
        if sympy_form == None and mathtext_form == None:
            raise ValueError("Both arguments are None!")
        super().__init__(sympy_form, mathtext_form)
        self.variable_mapping = dict()

    def set_variable(self, sympy_form: str, variable):
        """
        Tells the equation what variables it's made of.
        Note: Not every variable-name is unique. For example, "m" could both characterize a mass or the magnetic
        quantum number. This is why setting the variables is necessary.
        :param sympy_form: Symbol of a variable in the equation.
        :param variable: Physical quantity corresponding to the symbol.
        :return: Nothing.
        """
        if sympy_form not in self.sympy_form:
            raise AttributeError("Variable with name %s not in equation!" % sympy_form)
        self.variable_mapping[sympy_form] = variable