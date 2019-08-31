from Constant import *

class PhysicalTerm:

    """
    A physical term is a word or phrase often used in the context of physics.
    """

    def __init__(self):
        self.info = dict()

    def __str__(self):
        return "Begriff"

class PhysicalLaw(PhysicalTerm):

    """
    A physical law describes in a general fashion how physical quantities describing the states of a system correlate
    and change in regard to each other. This may be a general quantity equation, a definition, a list of
    equations/definitions or some other mathematical term involving physical quantities.
    """

    def __init__(self):
        """
        Relations is supposed to be a dictionary of lists: {"relation_name": [sympy_form, mathtext_form], ...}
        """
        super().__init__()
        self.picture = None

    def __str__(self):
        return "Gesetz"


class Unit(PhysicalTerm):

    """
    A unit is represented by a term consisting of arbitrary symbols giving qualitative meaning to a quantity.
    """

    def __init__(self):
        """
        Creates a unit.
        """
        super().__init__()

    def __str__(self):
        return "Einheit"

    def set_dimension(self, sympy_form: str, maththext_form: str):
        """
        Assigns a dimension to this physical quantity.
        :param name:
        :return:
        """
        pass

class PhysicalQuantity(PhysicalTerm):

    """
    If a common property of two physical objects can be compared using a real number, it's called a physical quantity.
    Physical quantities sharing some aspects can be arbitrarily divided into quantity types. One can choose an
    arbitrary set of physical quantities to serve as base quantities of a so-called "unit system", which is made up of
    the units of the chosen base quantities.
    Note: Physical quantities have to remain invariant under coordinate-transformations. They may also require a
    directional property consisting of a tensor.
    """

    def __init__(self):
        """
        Creates a physical quantity. Every symbol in a physical quantity equation is a physical Quantity.
        :param args:
        """
        self.info = dict()

    def __str__(self):
        return "Größe"

    def get_value(self):
        """
        The product of a real number with the unit is called a quantity value and is usually a dynamic property of a
        physical quantity. There are also physical quantities whose quantity value is permanent. These are called
        physical constants. 
        """
        pass


class PhysicalConstant(PhysicalQuantity, Constant):
    """
    A physical quantity with a constant quantity value is called a physical constant.
    """

    def __init__(self, *args):
        super().__init__(*args)
        super().lock()


class QuantityType(dict):
    """
    Physical quantities sharing some aspects are arbitrarily subdivided into different quantity types. They don't have
    to share the same units or even the same dimension. Example: wave length and the diameter of a pipe are both
    physical quantities corresponding to a length. Precipitation depth can also be measured like a length but is
    probably not considered one by most.
    """

class Dimension():
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


