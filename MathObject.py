class MathObject:

    def __init__(self, name: str, sympyForm: str, mathtextForm: str = None):

        """
        Creates a MathObject instance. This is the superclass of all the mathematical objects like equations,
        variables or units used in the formulary. It is saved twofold:
        1. as a SymPy-representation to handle the logic
        2. as a mathtext-string to display the equation with

        :param name: The non-unique name of the MathObject
        :param sympyForm: SymPy-representation of the MathObject
        :param mathtextForm: Text-representation that can be displayed using matplotlib.maththext
        :return: Returns nothing
        """

        self.name = name
        self.sympyForm = sympyForm
        if mathtextForm is None:
            self.mathtextForm = sympyForm
        else:
            self.mathtextForm = mathtextForm

