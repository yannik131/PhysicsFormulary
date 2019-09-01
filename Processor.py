from Metrology import *
from sympy import *
import re

class Processor:

    def __init__(self):
        self.given = list()
        self.sought = None
        self.solution_mathtext = None
        self.exceptions = ["sin", "cos", "tan", "asin", "atan", "acos", "ln"]

    def solve(self):
        law = None
        for math_object in self.given:
            if type(math_object) is PhysicalLaw:
                law = math_object
        contains_everything = True
        eq = law.info["Gleichung"][0]
        variables = re.findall("[a-zA-Z]+", eq)
        for var in variables:
            if var not in self.exceptions and law.info["map"][var] not in self.given and \
                    law.info["map"][var] is not self.sought:
                contains_everything = False
                break
        if not contains_everything:
            raise RuntimeError("Law doesn't contain the sought quantities")
        sides = eq.split("=")
        sought_sympy_form = None
        for quantity in law.info["map"]:
            q = law.info["map"][quantity]
            if self.sought == q:
                sought_sympy_form = quantity
        raw_solution = sought_sympy_form+"="+latex(solveset(sides[0]+"-"+sides[1], sought_sympy_form))
        variables = re.findall("[a-zA-Z]+", raw_solution)
        for var in variables:
            if var in law.info["map"]:
                quantity = law.info["map"][var]
                raw_solution.replace(var, quantity.info["Formelzeichen (mathtext)"])
        self.solution_mathtext = raw_solution
