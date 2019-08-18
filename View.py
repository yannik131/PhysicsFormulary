from tkinter import *
import guiSetup
import matplotlib as matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

class View:

    def __init__(self):
        self.root = Tk()
        self.root.attributes("-zoomed", True)
        self.root.title("Physik-Formelsammlung")
        guiSetup.setUp(self.root, self)

    def mainloop(self):
        self.root.mainloop()