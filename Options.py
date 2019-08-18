from Singleton import *
import tkinter

class Options(dict, metaclass=Singleton):

    def addOption(self, t: tkinter.Variable, name: str, default_value):
        self[name] = t()
        self[name].set(default_value)