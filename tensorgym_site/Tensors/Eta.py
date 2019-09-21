from Tensors.SymmetryProperties import SymmetryProperties
from Tensors.Partial import Partial
from Tensors.TypeError import TypeError
class Eta:

    def __init__(self, sym, partials=None):
        if type(sym) is SymmetryProperties:
            self.sym = sym
            self.sym.setSymmetric(True)
        else:
            raise TypeError
        self.partials = list()
        if partials is not None:
            for el in partials:
                if type(el) is Partial:
                    self.partials.append(el)
                else: raise TypeError

    def getSym(self):
        return self.sym

    def getIndices(self):
        return self.sym.getIndices()

    def getPartials(self):
        return self.partials

    def setIndices(self, sym):
        if type(sym) is SymmetryProperties:
            self.sym = sym
        else: raise TypeError

    def setPartials(self, partials):
        self.partials = list()
        for el in partials:
            if type(el) is Partial:
                self.partials.append(el)
            else:
                raise TypeError

    def patternEq(self, other):
        return self.getSym().patternEq(other.getSym())

    def patternEqH(self, other):
        return self.getSym().patternEqH(other.getSym())

    def __eq__(self, other):
        same = True
        if not len(self.getIndices()) == len(other.getIndices()):
            same = False
        for el in self.getIndices():
            if el not in other.getIndices():
                same = False
        if not len(self.getPartials()) == len(other.getPartials()):
            same = False
        for el in self.getPartials():
            if el not in other.getPartials():
                same = False
        if same:
            return True
        else:
            return False

    def __repr__(self):
        strx = ""
        if len(self.getPartials()) > 0:
            for el in self.getPartials():
                strx = strx + repr(el)
            strx = strx + "\\(" + "\\eta" + repr(self.sym) + "\\)"
        else:
            strx = strx + "\\eta" + repr(self.sym)
        return strx

