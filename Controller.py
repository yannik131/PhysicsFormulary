from View import *
from Metrology import *
import guiSetup
import pickle
import os

class Controller(metaclass=Singleton):

    def __init__(self):
        self.load()
        self.view = View(self.database)
        guiSetup.set_up_bindings(self, self.view)
        self.view.update_list()

    def load(self):
        if os.path.exists("database.p"):
            with open("database.p", "rb") as file:
                self.database = pickle.load(file)
        else:
            self.database = list()

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    controller = Controller()
    controller.run()