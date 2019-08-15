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