class PhysicalQuantity(MathObject):
    """
    If a common property of two physical objects can be compared using a real number, it's called a physical quantity.
    Physical quantities sharing some aspects can be arbitrarily divided into quantity types. One can choose an
    arbitrary set of physical quantities to serve as base quantities of a so-called "unit system", which is made up of
    the units of the chosen base quantities.
    Note: Physical quantities have to remain invariant under coordinate-transformations. They may also require a
    directional property consisting of a tensor.
    """

    def __init__(self, *args):
        """
        Creates a physical quantity. One has to carefully think about what to make a physical quantity and what not:
        Is v
        :param args:
        """

        """
        The product of a real number with the unit is called a quantity value and is usually a dynamic property of a
        physical quantity. There are also physical quantities whose quantity value is permanent. These are called
        physical constants. 
        """


class PhysicalConstant(PhysicalQuantity):
    """
    A physical quantity with a constant quantity value is called a physical constant.
    """

class QuantityType:

    """
    Physical quantities sharing some aspects are arbitrarily subdivided into different quantity types. They don't have
    to share the same units or even the same dimension. Example: wave length and the diameter of a pipe are both
    physical quantities corresponding to a length. Precipitation depth can also be measured as a length but dividing
    it into a quantity type is arbitrary.
    """


class Dimension(MathObject):

    """
    If the quotient of two physical quantities is a real number, they share the same dimension. All sides of a physical
    equation have to have the same dimension.
    Dimensions are used only in reference to a chosen unit system and convey qualitative information of a physical
    quantity. In the context of this application, units are divided in different dimensions and physical quantities are
    divided into different quantity types. After choosing a unit system, every base quantity is assigned a dimension of
    the same name as the base quantity. Then, every physical quantity that is not a base quantity has its dimension
    determined by dividing its unit by the units of the base quantities and inserting the resulting exponent in the
    dimensional analysis (i. e. in the SI base system, dim Q = L^a*M^*b*T^c*...). The unit of a base quantity is called
    the coherent unit of its corresponding dimension.
    """

class Equation(MathObject):

    """
    The Equation class handles storing of single equations in an object.
    """

    def __init__(self, *args):
        """
        Constructs a new Equation-object.

        :param args: Passed to super
        """
        super().__init__(*args)
        self.variable_mapping = dict()
        self.description = str()

    def set_variable(self, sympy_form: str, variable):
        """
        Tells the equation what variables it's made of.
        Note: Not every variable-name is unique. For example, "m" could both characterize a mass or the magnetic
        quantum number. This is why setting the variables is necessary.
        :param sympy_form: Symbol of a variable in the equation.
        :param variable: Variable object to connect the variable symbol in the equation with.
        :return: Nothing.
        """
        if sympy_form not in self.sympy_form:
            raise AttributeError("Variable with name %s not in equation!" % sympy_form)
        self.variable_mapping[sympy_form] = variable

class QuantityEquation(Equation):
    """
    Two physical quantities with the same dimensions can be associated using an equation.
    """

class Definition(QuantityEquation):

    def __init__(self, *args):
        super().__init__(*args)

class Relation(QuantityEquation):

    def __init__(self, *args):
        super().__init__(*args)