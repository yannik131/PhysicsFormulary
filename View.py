from tkinter import *
from Processor import *
from Singleton import *
import copy
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
        self.standard_dict = {"Name": [1, 50], "Definition": [10, 50], "Weiteres": [3, 50]}
        self.size_mapping = {**self.standard_dict, **{"Formelzeichen (mathtext)": [1, 50], "Formelzeichen (sympy)":
                                                      [1, 50], "Einheit": [1, 50], "Gleichung": [2, 50]}}

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
            self.formula_name.set(math_object.info["Gleichung"][0])
        else:
            menu = self.formula_selection.children["menu"]
            menu.delete(0, END)
            self.formula_name.set(math_object.info["Name"])

        info = math_object.info
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        for key in info:
            self.text.insert(END, key, "bold_italics")
            if key == "map":
                string_copy = dict()
                for entry in info["map"]:
                    string_copy[entry] = info["map"][entry].info["Name"]
                self.text.insert(END, ": " + str(string_copy) + "\n", "normal")
            else:
                self.text.insert(END, ": " + str(info[key]) + "\n", "normal")

        self.text.config(state=DISABLED)

    def insert_text(self, text, style, font):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, text)
        self.text.config(state=DISABLED)

    def add_to_database(self, input, category):
        if category is Unit:
            title="Einheit definieren"
        elif category is PhysicalQuantity:
            title="Größe definieren"
        elif category is PhysicalLaw:
            title="Gesetz definieren"
        elif category is PhysicalTerm:
            title="Begriff definieren"
        input = guiSetup.input_window(self.root, input, title)
        if input["Name"] == "" or (category in [Unit, PhysicalQuantity] and \
                                   input["Formelzeichen (mathtext)"] == ""):
            return
        new_object = category()
        for entry in input:
            new_object.info[entry] = input[entry]
        for math_object in self.database:
            if type(math_object) is category:
                if math_object.info["Name"] == input["Name"]:
                    raise RuntimeError("%s already in database!" % input["Name"])

        if category is PhysicalLaw:
            new_object.info["Gleichung"] = eval(new_object.info["Gleichung"])
            self.assign_quantities(new_object)
        elif category is PhysicalQuantity:
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

    def drag_n_drop(self, event):
        given_listbox_x = self.given_listbox.winfo_rootx()
        given_listbox_y = self.given_listbox.winfo_rooty()
        given_listbox_width = self.given_listbox.winfo_width()
        given_listbox_heigth = self.given_listbox.winfo_height()
        mouse_x = event.x_root
        mouse_y = event.y_root
        if mouse_x >= given_listbox_x and mouse_x <= (given_listbox_x+given_listbox_width) and\
            mouse_y >= given_listbox_y and mouse_y <= (given_listbox_y+given_listbox_heigth):
            self.add_to_given()

    def add(self, category):
        input = copy.deepcopy(self.standard_dict)
        if category in [PhysicalQuantity, Unit]:
            input["Formelzeichen (mathtext)"] = [1, 50]
        if category is Unit:
            input["Formelzeichen (sympy)"] = [1, 50]
        if category is PhysicalLaw:
            input["Gleichung"] = [2, 50]
        if category is PhysicalQuantity:
            input["Einheit"] = [1, 50]
        self.add_to_database(input, category)

    def assign_units(self, quantity: PhysicalQuantity):
        units = re.findall("[a-zA-Z]+", quantity.info["Einheit"])
        if not units:
            quantity.info["map"] = dict()
            return
        input = dict()
        for sympy_var in units:
            input[sympy_var] = self.size_mapping["Einheit"]
        input = guiSetup.input_window(self.root, input, "Zuordnung der Einheiten (per Name)")
        quantity.info["map"] = dict()
        for sympy_var in input:
            unit = input[sympy_var]
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
        eq = law.info["Gleichung"][0]
        variables = re.findall("[a-zA-Z]+", eq)
        if not variables:
            law.info["map"] = dict()
        input = dict()
        for sympy_var in variables:
            if sympy_var not in self.processor.exceptions:
                input[sympy_var] = self.size_mapping["Einheit"]
        input = guiSetup.input_window(self.root, input, "Zuordnung der Größen (per Name)")
        law.info["map"] = dict()
        for sympy_var in input:
            quantity = input[sympy_var]
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

    def edit_object(self, math_object=None):
        if not math_object:
            math_object = self.get_selection()
        input = dict()
        string_copy = dict()
        for key in math_object.info:
            if key == "map":
                continue
            input[key] = self.size_mapping[key]+[str(math_object.info[key])]
            string_copy[key] = str(math_object.info[key])
        input = guiSetup.input_window(self.root, input, "Editieren")
        for key in input:
            if input[key] != string_copy[key]:
                #entry was changed
                if key == "Gleichung":
                    try:
                        new_list = eval(input[key])
                        if not type(new_list) is list:
                            raise Exception()
                    except:
                        print("Can't interpret as list: %s" % input[key])
                        continue
                    math_object.info["Gleichung"] = new_list
                    self.assign_quantities(math_object)
                else:
                    math_object.info[key] = input[key]
                    if key == "Einheit":
                        self.assign_units(math_object)
        self.update_list(selection=math_object.info["Name"])

    def update_axis(self, math_object=None):
        if not math_object:
            math_object = self.get_selection()
        if not math_object:
            return
        self.formula_axis.clear()
        formula, pos, fontsize = None, None, None
        if type(math_object) is PhysicalLaw:
            formula =  math_object.info["Gleichung"][1]
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
        text = selected.info["Name"]
        popup.add_command(label="\"%s\" bearbeiten"%text, command=self.edit_object)
        if type(selected) in [PhysicalQuantity, PhysicalLaw]:
            popup.add_command(label="\"%s\" ist gegeben"%text, command=self.add_to_given)
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
                    text += item.info["Gleichung"][1] + ","
            for item in self.processor.given:
                if type(item) is PhysicalQuantity:
                    text += item.info["Formelzeichen (mathtext)"] + ","
            text = text[:-1]
        text += "\\right\\}\\ \\mathit{ges.:}\\ "
        if self.processor.sought:
            text += self.processor.sought.info["Formelzeichen (mathtext)"]
        self.rearrange_axis.text(0.01, 0.7, "$%s$"%text, fontsize=20)
        self.rearrange_canvas.draw()

    def update_list(self, selection=""):
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
            self.given_listbox.insert(END, str(given)+": "+given.info["Name"])

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
        if not selected:
            return
        text = selected.info["Name"]
        popup.add_command(label="\"%s\" aus gesucht entfernen" % text, command=self.remove_given)
        popup.add_command(label="\"%s\" bearbeiten" % text, command=lambda s=selected: self.edit_object(s))
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
