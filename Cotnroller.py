from View import *
from Metrology import *
import guiSetup

class Controller(metaclass=Singleton):

    def __init__(self):
        self.database = dict()
        self.view = View(self.database)
        guiSetup.set_up_bindings(self, self.view)

        newtons_first_law = PhysicalLaw(title="Erstes Newtonsches Gesetz",
                                        definition="Ein Körper, auf dem keine äußere Kraft" \
                                                   "wirkt, verändert seinen Impuls nicht.",
                                        additionalInfo="Beschreibt das Beharrungs" \
                                                       "vermögen oder die Trägheit der Körper.")
        newtons_first_law.addRelation("Impulssatz",
                                      Relation(sympy_form=None, mathtext_form="\\vec{F} = 0 \Rightarrow \\vec{p}" \
                                                                              "= \\mathit{const.}"))
        newtons_first_law.addRelation("Geschwindigkeitskonstanz",
                                      Relation(sympy_form=None, mathtext_form="m = \\text{const.} \\Rightarrow" \
                                                                              " \vec{v} = \\mathit{const.}"))
        newtons_second_law = PhysicalLaw(title="Zweites Newtonsches Gesetz",
                                         definition="Wirkt eine Kraft auf einen Körper, so it die dadurch erfolgende "\
                                         "Impulsänderung zur wirkenden Kraft proportional. Die Impulsänderung "\
                                         "geschieht in Richtung der Kraft.",
                                         additionalInfo="Beschreibt, wie der Bewegungszustand eines Körpers durch auf "\
                                         "ihn wirkende Kräfte verändert wird.")
        newtons_second_law.addRelation("Defintion der Kraft", Relation(sympy_form=None,
                                       mathtext_form="\\frac{\\mathit{d\\vec{p}}}{\\mathit{dt}} = \\frac{d\\left("\
                                       "m\\vec{v}\\right)}{\\mathit{dt}} = \\vec{F}"))
        self.database[newtons_first_law.title] = newtons_first_law
        self.database[newtons_second_law.title] = newtons_second_law
        self.view.update_list()

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    controller = Controller()
    controller.run()