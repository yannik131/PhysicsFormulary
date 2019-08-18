"""
The Units module.
"""

from MathObject import *

class Unit(MathObject):

    """
    The unit class. A unit is represented by a term consisting of only SI base units excluding abbreviations
    like N for m*kg/s² or J for m*kg/s³ Note that every unit does have its own name.
    """

    def __init__(self, *args):
        """
        Creates a unit.
        :param args: passed to MathObject
        """

        super().__init__(*args)


class SIBaseUnits(dict):

    """
    This is a collection of all the base units of the SI-System: m, kg, s, A, K, mol, and cd.
    """

    def __init__(self):
        """
        Creates an immutable dictionary with the base units as entries.
        """

        self["m"] = Unit("Meter", "m")
        self["kg"] = Unit("Kilogramm", "kg")
        self["s"] = Unit("Sekunde", "s")
        self["A"] = Unit("Ampere", "A")
        self["K"] = Unit("Temperatur", "K")
        self["mol"] = Unit("Mol", "mol")
        self["cd"] = Unit("Candela", "cd")
        self.__locked = True

    def __setitem__(self, key, value):
        if self.__dict__.get("_SIBaseUnits__locked", False):
            raise AttributeError("The base units surely have not changed again!")

        self.__dict__[key] = value

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
