class Constant:

    def __init__(self):
        self.__locked = False

    def lock(self):
        self.__locked = True

    def __setitem__(self, key, value):
        if self.__dict__.get(key, False) and not key == "dimension":
            raise AttributeError("Trying to assign to constant!")

