from formularyManipulator.View import *
import guiSetup

class Controller:

    def __init__(self):
        self.view = View()
        guiSetup.setUpBindings(self, self.view)

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    controller = Controller()
    controller.run()