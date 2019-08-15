class MathObject:

    def __init__(self, name: str, sympy_form: str, mathtext_form: str = None):

        """
        Creates a MathObject instance. This is the superclass of all the mathematical objects like equations,
        variables or units used in the formulary. It is saved twofold:
        1. as a SymPy-representation to handle the logic
        2. as a mathtext-string to display the equation with

        :param name: The non-unique name of the MathObject
        :param sympy_form: SymPy-representation of the MathObject
        :param mathtext_form: Text-representation that can be displayed using matplotlib.maththext
        :return: Returns nothing
        """

        self.name = name
        self.sympy_form = sympy_form
        if mathtext_form is None:
            self.mathtext_form = sympy_form
        else:
            self.mathtext_form = mathtext_form

