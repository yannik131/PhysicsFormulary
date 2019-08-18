from View import *
from Options import *

def setUp(root, view):
    setUpFrames(root, view)
    setUpSearchArea(view)
    setUpList(view)
    setUpFormulaArea(view)

def setUpFrames(root, view):
    for i in range(3):
        root.columnconfigure(i, weight=1)

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=3)
    root.rowconfigure(2, weight=2)

    view.search_bar_frame = Frame(root)
    view.search_bar_frame.config(bg="blue")
    view.search_bar_frame.grid(row=0, column=0, columnspan=3, sticky=W+E+S+N)
    view.list_frame = Frame(root)
    view.list_frame.config(bg="red")
    view.list_frame.grid(row=1, column=0, sticky=W+E+N+S)
    view.formula_frame = Frame(root)
    view.formula_frame.config(bg="cyan")
    view.formula_frame.grid(row=1, column=1, sticky=W+E+S+N)
    view.given_searched_frame = Frame(root)
    view.given_searched_frame.config(bg="green")
    view.given_searched_frame.grid(row=1, column=2, sticky=W+E+S+N)
    view.rearrange_frame = Frame(root)
    view.rearrange_frame.config(bg="white")
    view.rearrange_frame.grid(row=2, column=0, columnspan=3, sticky=W+E+S+N)

def setUpSearchArea(view):
    view.search_bar_frame.rowconfigure(1, weight=1)

    Label(view.search_bar_frame, text="Suchen in:").grid(row=0, column=0)

    def addSearchCheckbutton(text, optionsVariable, column):
        Options().addOption(BooleanVar, optionsVariable, True)
        checkbutton = Checkbutton(view.search_bar_frame, text=text, variable=Options()[optionsVariable])
        checkbutton.grid(row=0, column=column, padx=10)

    addSearchCheckbutton("Definitionen", "definitionSearch", 1)
    addSearchCheckbutton("Relationen", "relationSearch", 2)
    addSearchCheckbutton("Größenart", "quantityTypeSearch", 3)
    addSearchCheckbutton("Größe", "quantitySearch", 4)
    addSearchCheckbutton("Dimension", "dimensionSearch", 5)
    addSearchCheckbutton("Einheit", "unitSearch", 6)
    addSearchCheckbutton("Erläuterung", "explanationSearch", 7)
    view.searchEntry = Entry(view.search_bar_frame)
    view.searchEntry.grid(row=1, column=0, padx=10, sticky=W+E)

def setUpList(view):
    view.list_frame.rowconfigure(0, weight=1)
    view.list_frame.columnconfigure(0, weight=1)
    view.formula_listbox = Listbox(view.list_frame)
    view.formula_listbox.grid(row=0, column=0, sticky=W+E+S+N)
    view.formula_listbox.insert(END, "test!")

def setUpFormulaArea(view):
    view.formula_frame.rowconfigure(0, weight=1)
    view.formula_frame.rowconfigure(1, weight=4)
    view.formula_frame.columnconfigure(0, weight=1)
    # The matplotlib figureCanvas uses pack. I don't want to deal with pack, so the figure gets its own frame.
    view.formula_display_frame = Frame(view.formula_frame)
    view.formula_display_frame.grid(row=0, column=0, sticky=W + E + S + N)

    view.formulaInformationFrame = Frame(view.formula_frame)
    view.formulaInformationFrame.grid(row=1, column=0, sticky=W+E+S+N)
    view.formulaInformationFrame.config(bg="pink")

    #The figure box uses coordinates in range 0-1. This is needed to place text in the figure.
    #Note: If the figsize is not set really tiny, the figure will not only expand in its master frame, but also take up
    #extra space from the other frames.
    figure = matplotlib.figure.Figure(figsize=(0.01, 0.01), dpi=100)
    view.formula_axis = figure.add_subplot(111)
    view.formula_axis.get_xaxis().set_visible(False)
    view.formula_axis.get_yaxis().set_visible(False)
    view.formula_axis.text(0.1, 0.4, "$\\overline{v}_{x_i} \\ \\coloneq \\ \\frac{x_i(t_2)-x_i(t_1)}{t_2-t_1}$", fontsize=20)

    canvas = FigureCanvasTkAgg(figure, master=view.formula_display_frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


def setUpBindings(controller, view):
    pass


    # text = StringVar()
    # entry = Entry(mainframe, width=70, textvariable=text)
    # entry.pack()
    #
    # label = Label(mainframe)
    # label.pack()
    #
    # fig = matplotlib.figure.Figure(figsize=(6, 2), dpi=100)
    # ax = fig.add_subplot(111)
    #
    # canvas = FigureCanvasTkAgg(fig, master=label)
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    # canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)