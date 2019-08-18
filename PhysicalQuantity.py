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