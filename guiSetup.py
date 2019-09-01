from View import *
from Metrology import *
import matplotlib as matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
from tkinter import *

def set_up(root, view):
    set_up_frames(root, view)
    set_up_search_area(view)
    set_up_list(view)
    set_up_formula_area(view)
    set_up_given_sought_area(view)
    set_up_rearrange_frame(view)
    set_up_menu(view)

def set_up_frames(root, view):
    for i in range(3):
        root.columnconfigure(i, weight=1)

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=4)
    root.rowconfigure(2, weight=3)
    view.search_bar_frame = Frame(root)
    view.search_bar_frame.grid(row=0, column=0, columnspan=3, sticky=W+E+S+N)
    view.list_frame = Frame(root)
    view.list_frame.grid(row=1, column=0, sticky=W+E+N+S)
    view.formula_frame = Frame(root)
    view.formula_frame.grid(row=1, column=1, sticky=W+E+S+N)
    view.given_sought_frame = Frame(root)
    view.given_sought_frame.grid(row=1, column=2, sticky=W+E+S+N)
    view.rearrange_frame = Frame(root)
    view.rearrange_frame.grid(row=2, column=0, columnspan=3, sticky=W+E+S+N)

def color_frames(view):
    view.search_bar_frame.config(bg="blue")
    view.rearrange_frame.config(bg="white")
    view.given_searched_frame.config(bg="green")
    view.formula_frame.config(bg="cyan")
    view.list_frame.config(bg="red")

def set_up_search_area(view):
    Label(view.search_bar_frame, text="Suchtext:").grid(row=0, column=0, sticky=W+E)
    view.search_phrase = StringVar()
    view.search_entry = Entry(view.search_bar_frame, textvariable=view.search_phrase, width=50)
    view.search_entry.grid(row=1, column=0, padx=10, sticky=W+E)

def set_up_list(view):
    view.list_frame.rowconfigure(0, weight=1)
    view.list_frame.columnconfigure(1, weight=1)
    scrollbar = Scrollbar(view.list_frame, orient=VERTICAL)
    view.listbox = Listbox(view.list_frame, yscrollcommand=scrollbar.set, selectmode=SINGLE)
    scrollbar.config(command=view.listbox.yview)
    scrollbar.grid(row=0, column=0, sticky=N + S)
    view.listbox.grid(row=0, column=1, sticky=W+E+S+N)

def set_up_rearrange_frame(view):
    figure = matplotlib.figure.Figure(figsize=(0.01, 0.01), dpi=100)
    view.rearrange_axis = figure.add_subplot(111)
    view.rearrange_axis.get_yaxis().set_visible(False)
    view.rearrange_axis.get_xaxis().set_visible(False)

    canvas = view.rearrange_canvas = FigureCanvasTkAgg(figure, master=view.rearrange_frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

def set_up_formula_area(view):
    view.formula_frame.rowconfigure(0, weight=1)
    view.formula_frame.rowconfigure(1, weight=4)
    view.formula_frame.columnconfigure(0, weight=1)
    # The matplotlib figureCanvas uses pack. I don't want to deal with pack, so the figure gets its own frame.
    view.formula_display_frame = Frame(view.formula_frame)
    view.formula_display_frame.grid(row=0, column=0, sticky=W + E + S + N)

    # The figure box uses coordinates in range 0-1. This is needed to place text in the figure.
    # Note: If the figsize is not set really tiny, the figure will not only expand in its master frame, but also take up
    # extra space from the other frames.
    figure = matplotlib.figure.Figure(figsize=(0.01, 0.01), dpi=100)
    view.formula_axis = figure.add_subplot(111)
    view.formula_axis.get_xaxis().set_visible(False)
    view.formula_axis.get_yaxis().set_visible(False)

    canvas = view.canvas = FigureCanvasTkAgg(figure, master=view.formula_display_frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    view.formula_information_frame = Frame(view.formula_frame)
    view.formula_information_frame.grid_propagate(False)
    view.formula_information_frame.grid(row=1, column=0, sticky=W+E+S+N)
    view.formula_information_frame.columnconfigure(0, weight=1)
    view.formula_information_frame.rowconfigure(1, weight=3)
    view.formula_information_frame.rowconfigure(2, weight=2)

    scrollbar = Scrollbar(view.formula_information_frame, orient=VERTICAL)
    view.text = Text(view.formula_information_frame, yscrollcommand=scrollbar.set)
    scrollbar.config(command=view.text.yview)
    view.text.config(state=DISABLED)
    scrollbar.grid(row=1, column=1, sticky=N+S)
    view.text.grid(row=1, column=0, sticky=W+E+N+S)
    view.text.tag_configure("bold_italics", font=("Courier", 11, "bold", "italic"))
    view.text.tag_configure("normal", font=("Courier", 11))
    view.formula_name = StringVar()
    view.formula_name.trace("w", lambda *args: view.update_axis())
    view.formula_selection = OptionMenu(view.formula_information_frame, view.formula_name, value="")
    view.formula_selection.grid(row=0, column=0, sticky=W+E)

def set_up_given_sought_area(view):
    view.given_sought_frame.rowconfigure(0, weight=1)
    view.given_sought_frame.rowconfigure(1, weight=4)
    view.given_sought_frame.rowconfigure(2, weight=1)
    view.given_sought_frame.rowconfigure(3, weight=2)
    view.given_sought_frame.columnconfigure(0, weight=1)
    Label(view.given_sought_frame, text="Gegeben:").grid(row=0, column=0, sticky=N+E+W)
    scrollbar = Scrollbar(view.given_sought_frame, orient=VERTICAL)
    view.given_listbox = Listbox(view.given_sought_frame, yscrollcommand=scrollbar.set)
    scrollbar.config(command=view.given_listbox.yview)
    scrollbar.grid(row=1, column=2, sticky=N+S)
    view.given_listbox.grid(row=1, column=0, sticky=W+E+N+S)
    Label(view.given_sought_frame, text="Gesucht:").grid(row=2, column=0, sticky=N+E+W)
    view.sought_text = StringVar()
    Label(view.given_sought_frame, textvariable=view.sought_text).grid(row=3, column=0, sticky=W+E)

def set_up_bindings(controller, view):
    view.listbox.bind("<<ListboxSelect>>", lambda event: view.database_select())
    view.given_listbox.bind("<<ListboxSelect>>", lambda event: view.given_select())
    view.given_listbox.bind("<Delete>", lambda event: view.remove_given())
    view.listbox.bind("<ButtonRelease-3>", view.listbox_popup)
    view.listbox.bind("<Double-Button-1>", lambda event: view.edit_object())
    view.listbox.bind("<ButtonRelease-1>", view.drag_n_drop)
    view.given_listbox.bind("<ButtonRelease-3>", view.given_listbox_popup)
    view.text.bind("<1>", lambda event: view.text.focus_set()) #Enable copying
    view.search_phrase.trace("w", lambda name, index, mode: view.update_list())
    view.root.bind("<Control-s>", lambda event: view.save())
    view.root.bind("<Delete>", lambda event: view.remove_from_database())

def set_up_menu(view):
    menubar = Menu(view.root)
    filemenu = view.filemenu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Datei", menu=filemenu)
    filemenu.add_command(label="Physikalische Größe definieren", command=lambda: view.add(PhysicalQuantity))
    filemenu.add_command(label="Physikalisches Gesetz definieren", command=lambda: view.add(PhysicalLaw))
    filemenu.add_command(label="Physikalischen Begriff definieren", command=lambda:view.add(PhysicalTerm))
    filemenu.add_command(label="Einheit definieren", command=lambda: view.add(Unit))
    view.root.config(menu=menubar)

class WatchedText(Text):
    """
    C&P https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
    """
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result

def input_window(root, name_dict, title="Eingabefenster"):
    toplevel = Toplevel(root)
    toplevel.title(title)
    text_dict = dict()
    for i, name in enumerate(name_dict):
        text_dict[name] = StringVar()
        Label(toplevel, text=name+":").grid(row=i, column=0)
        size = name_dict[name][:2]
        t = WatchedText(toplevel, height=size[0], width=size[1])
        if len(name_dict[name]) == 3:
            default = name_dict[name][2]
            text_dict[name].set(default)
            t.insert(END, default)
        t.grid(row=i, column=1, padx=5, pady=5)
        t.bind("<<TextModified>>", lambda event, name=name, t=t: text_dict[name].set(t.get(1.0, END)))
        if i == 0:
            t.focus_set()
    Button(toplevel, text="OK", command=toplevel.destroy).grid(row=i+1, column=0, columnspan=2, padx=5)
    toplevel.bind("<Control-Return>", lambda event: toplevel.destroy())
    toplevel.wait_window()
    for name in text_dict:
        text = text_dict[name].get()
        while text.endswith("\n"):
            text = text[:-1]
        text_dict[name] = text
    return text_dict
