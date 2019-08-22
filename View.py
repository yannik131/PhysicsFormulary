from tkinter import *
from Singleton import *
from Metrology import *
import guiSetup

class View(metaclass=Singleton):

    def __init__(self, database):
        self.root = Tk()
        self.root.attributes("-zoomed", True)
        self.root.title("Physik-Formelsammlung")
        guiSetup.set_up(self.root, self)
        self.database = database

    def update_list(self):
        for math_object in self.database:
            self.listbox.insert(END, math_object)

    def update_formula_frame(self):
        self.formula_axis.clear()
        text = self.listbox.get(self.listbox.curselection())
        print(text)
        math_object = self.database[text]
        if type(math_object) is PhysicalLaw:
            self.formula_axis.text(0.1, 0.4, "$%s$" % math_object.relations[list(math_object.relations.keys())[0]]\
                                   .mathtext_form, fontsize=20)
            self.canvas.draw()

    def mainloop(self):
        self.root.mainloop()