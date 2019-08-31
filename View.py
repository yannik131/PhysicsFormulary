from tkinter import *
from Processor import *
from Singleton import *
import guiSetup
import re
import pickle

class View(metaclass=Singleton):

    def __init__(self, database):
        self.root = Tk()
        self.root.attributes("-zoomed", True)
        self.root.title("Physik-Formelsammlung")
        guiSetup.set_up(self.root, self)
        self.database = database
        self.processor = Processor()
        self.listbox_items = list()
        self.update_solution()

    def save(self):
        with open("database.p", "wb") as file:
            pickle.dump(self.database, file)

    def remove_from_database(self, math_object=None):
        if not math_object:
            math_object = self.get_selection()
        if math_object:
            self.database.remove(math_object)
            self.update_list()

    def update_formula_frame(self, math_object=None):
        if not math_object:
            math_object = self.get_selection()
        if not math_object:
            return
        if type(math_object) is PhysicalLaw:
            menu = self.formula_selection.children["menu"]
            menu.delete(0, END)
            for key in math_object.info["Gleichungen"]:
                command = lambda text: self.formula_name.set(text)
                menu.add_command(label=key, command=lambda text=key: command(text))
            self.formula_name.set(list(math_object.info["Gleichungen"].keys())[0])
        else:
            menu = self.formula_selection.children["menu"]
            menu.delete(0, END)
            self.formula_name.set(math_object.info["Name"])

        info = math_object.info
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        for key in info:
            self.text.insert(END, key, "bold_italics")
            self.text.insert(END, ": "+str(info[key])+"\n", "normal")
        self.text.config(state=DISABLED)

    def insert_text(self, text, style, font):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, text)
        self.text.config(state=DISABLED)

    def add_to_database(self, instance_type: PhysicalTerm, input, title):
        guiSetup.input_window(self.root, input, title)
        if input["Name"].get() == "" or (instance_type in [Unit, PhysicalQuantity] and \
                                         input["Formelzeichen (mathtext)"].get() == ""):
            return
        new_object = instance_type()
        for entry in input:
            new_object.info[entry] = input[entry].get()
        for math_object in self.database:
            if type(math_object) is instance_type:
                if math_object.info["Name"] == input["Name"].get():
                    raise RuntimeError("%s already in database!" % input["Name"].get())

        if instance_type is PhysicalLaw:
            new_object.info["Gleichungen"] = eval(new_object.info["Gleichungen"])
            self.assign_quantities(new_object)
        elif instance_type is PhysicalQuantity:
            self.assign_units(new_object)
        self.database.append(new_object)
        self.sort_database()
        self.update_list(selection=new_object.info["Name"])
        self.save()

    def sort_database(self):
        def func(math_object):
            id = str(math_object)
            if id == "Einheit":
                return 0
            elif id == "Größe":
                return 1
            elif id == "Gesetz":
                return 2
            elif id == "Begriff":
                return 3
        self.database = sorted(self.database, key=func)

    def add_unit(self):
        input =  {"Name": StringVar(), "Definition": StringVar(), "Formelzeichen (mathtext)": StringVar(),
                  "Formelzeichen (sympy)": StringVar(), "Weiteres": StringVar()}
        self.add_to_database(Unit, input, "Einheit definieren")

    def add_physical_quantity(self):
        input = {"Name": StringVar(), "Formelzeichen (mathtext)": StringVar(),
                 "Definition": StringVar(), "Einheit": StringVar(), "Weiteres": StringVar()}
        self.add_to_database(PhysicalQuantity, input, "Physik. Größe definieren")

    def add_physical_term(self):
        input = {"Name": StringVar(), "Definition": StringVar(), "Weiteres": StringVar()}
        self.add_to_database(PhysicalTerm, input, "Physik. Begriff definieren")

    def add_physical_law(self):
        input = {"Name": StringVar(), "Definition": StringVar(), "Weiteres": StringVar(),
                 "Gleichungen": StringVar()}
        self.add_to_database(PhysicalLaw, input, "Physik. Gesetz definieren")

    def assign_units(self, quantity: PhysicalQuantity):
        units = re.findall("[a-zA-Z]+", quantity.info["Einheit"])
        input = dict()
        for sympy_var in units:
            input[sympy_var] = StringVar()
        guiSetup.input_window(self.root, input, "Zuordnung der Einheiten (per Name)")
        if not "map" in quantity.info:
            quantity.info["map"] = dict()
        for sympy_var in input:
            unit = input[sympy_var].get()
            found = False
            for math_object in self.database:
                if type(math_object) is Unit:
                    if math_object.info["Name"] == unit:
                        quantity.info["map"][sympy_var] = math_object
                        found = True
                        break
            if not found:
                raise RuntimeError("%s: Unit \"%s\" not yet defined" % (sympy_var, unit))

    def assign_quantities(self, law: PhysicalLaw):
        for equation in law.info["Gleichungen"]:
            eq = law.info["Gleichungen"][equation][0]
            variables = re.findall("[a-zA-Z]+", eq)
            input = dict()
            for sympy_var in variables:
                if sympy_var not in self.processor.exceptions:
                    input[sympy_var] = StringVar()
            guiSetup.input_window(self.root, input, "Zuordnung der Größen (per Name)")
            if not "map" in law.info:
                law.info["map"] = dict()
            for sympy_var in input:
                quantity = input[sympy_var].get()
                for math_object in self.database:
                    if type(math_object) is PhysicalQuantity:
                        if math_object.info["Name"] == quantity:
                            law.info["map"][sympy_var] = math_object
                if not sympy_var in list(law.info["map"].keys()):
                    raise RuntimeError("%s: Quantity \"%s\" not yet defined" % (sympy_var, quantity))

    def given_select(self):
        selection = self.get_given_selection()
        self.update_formula_frame(selection)
        self.update_axis(selection)

    def database_select(self):
        selection = self.get_selection()
        self.update_formula_frame(selection)
        self.update_axis(selection)

    def edit_object(self):
        math_object = self.get_selection()
        input = dict()
        for key in math_object.info:
            input[key] = StringVar()
            input[key].set(math_object.info[key])
        guiSetup.input_window(self.root, input, "Editieren")
        if type(math_object) is PhysicalLaw:
            before = str(math_object.info["Gleichungen"])
        elif type(math_object) is PhysicalQuantity:
            before = math_object.info["Einheit"]
        for key in math_object.info:
            math_object.info[key] = input[key].get()
        try:
            if type(math_object) is PhysicalLaw:
                math_object.info["Gleichungen"] = eval(math_object.info["Gleichungen"])
                if before != str(math_object.info["Gleichungen"]):
                    self.assign_quantities(math_object)
            elif type(math_object) is PhysicalQuantity and before != math_object.info["Einheit"]:
                self.assign_units(math_object)
        except:
            if type(math_object) is PhysicalQuantity:
                math_object.info["Einheit"] = before
            elif type(math_object) is PhysicalLaw:
                math_object.info["Gleichungen"] = eval(before)

        self.update_list(selection=math_object.info["Name"])

    def update_axis(self, math_object=None):
        if not math_object:
            math_object = self.get_selection()
        if not math_object:
            return
        self.formula_axis.clear()
        formula, pos, fontsize = None, None, None
        if type(math_object) is PhysicalLaw:
            formula =  math_object.info["Gleichungen"][self.formula_name.get()][1]
            pos = [0.1, 0.4]
            fontsize = 20
        elif "Formelzeichen (mathtext)" in math_object.info:
            formula = math_object.info["Formelzeichen (mathtext)"]
            pos = [0.45, 0.4]
            fontsize = 30
        if formula:
            self.formula_axis.text(pos[0], pos[1], "$%s$" % formula, fontsize=fontsize)
        else:
            self.formula_axis.text(0, 0, "")
        self.canvas.draw()

    def listbox_popup(self, event):
        popup = Menu(self.root, tearoff=False)
        selected = self.get_selection()
        text = str(selected)+": "+selected.info["Name"]
        popup.add_command(label="\"%s\" bearbeiten"%text, command=self.edit_object)
        if type(selected) in [PhysicalQuantity, PhysicalLaw]:
            popup.add_command(label="\"%s\" zu gegeben hinzufügen"%text, command=self.add_to_given)
        if type(selected) is PhysicalQuantity:
            popup.add_command(label="\"%s\" ist gesucht"%text, command=self.add_to_sought)
        popup.tk_popup(event.x_root, event.y_root, 0)

    def add_to_given(self):
        selection = self.get_selection()
        if type(selection) in [PhysicalQuantity, PhysicalLaw]:
            if not selection in self.processor.given:
                self.processor.given.append(selection)
        self.update_given_listbox()
        try:
            self.processor.solve()
        except:
            pass
        self.update_solution()

    def add_to_sought(self):
        selection = self.get_selection()
        self.processor.sought = selection
        self.sought_text.set(selection.info["Name"])
        try:
            self.processor.solve()
        except:
            pass
        self.update_solution()

    def update_solution(self):
        text = str()
        self.rearrange_axis.clear()
        if self.processor.solution_mathtext:
            self.rearrange_axis.text(0.01, 0.3, "$%s$"%self.processor.solution_mathtext, fontsize=20)
        text += "\\ \\mathit{geg.:}\\ \\left\\{"
        if len(self.processor.given) > 0:
            for item in self.processor.given:
                if type(item) is PhysicalLaw:
                    for law in item.info["Gleichungen"]:
                        text += item.info["Gleichungen"][law][1] + ","
            for item in self.processor.given:
                if type(item) is PhysicalQuantity:
                    text += item.info["Formelzeichen (mathtext)"] + ","
            text = text[:-1]
        text += "\\right\\}\\ \\mathit{ges.:}\\ "
        if self.processor.sought:
            text += self.processor.sought.info["Formelzeichen (mathtext)"]
        self.rearrange_axis.text(0.01, 0.7, "$%s$"%text, fontsize=20)
        self.rearrange_canvas.draw()

    def update_list(self, selection=None):
        self.listbox.delete(0, END)
        self.listbox_items.clear()
        search_phrase = self.search_phrase.get()
        for i, math_object in enumerate(self.database):
            info = math_object.info
            found = search_phrase in (str(math_object)+": "+math_object.info["Name"])
            for text in [*info.values()]:
                if type(text) is dict:
                    for key in [*text.keys()]:
                        if search_phrase in key:
                            found = True
                if search_phrase in text:
                    found = True
            if not search_phrase or found:
                self.listbox.insert(END, str(math_object)+": "+math_object.info["Name"])
                self.listbox_items.append(i)
        if not selection:
            self.listbox.selection_set(0)
        else:
            for i, math_object in enumerate(self.database):
                if selection == math_object.info["Name"]:
                    selection = i
                    break
            self.listbox.selection_set(selection)
        self.update_formula_frame()

    def update_given_listbox(self):
        self.given_listbox.delete(0, END)
        for given in self.processor.given:
            self.given_listbox.insert(END, given.info["Name"])

    def get_given_selection(self):
        selection = self.given_listbox.curselection()
        if selection:
            selection = selection[0]
            return self.processor.given[selection]
        return None

    def remove_given(self):
        selection = self.get_given_selection()
        self.processor.given.remove(selection)
        self.update_given_listbox()
        try:
            self.processor.solve()
        except:
            pass
        self.update_solution()

    def given_listbox_popup(self, event):
        popup = Menu(self.root, tearoff=False)
        selected = self.get_given_selection()
        text = str(selected) + ": " + selected.info["Name"]
        popup.add_command(label="\"%s\" aus gesucht entfernen" % text, command=self.remove_given)
        popup.tk_popup(event.x_root, event.y_root, 0)

    def get_selection(self):
        selection = self.listbox.curselection()
        if selection:
            selection = selection[0]
            return self.database[self.listbox_items[selection]]
        else:
            return None

    def mainloop(self):
        self.root.mainloop()