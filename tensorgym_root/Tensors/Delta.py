from Tensors.SymmetryProperties import SymmetryProperties
from Tensors.Partial import Partial
from Tensors.TypeError import TypeError
class Delta:

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
                else:
                    raise TypeError

    # get symmetry properties
    def getSym(self):
        return self.sym

    def getIndices(self):
        return self.sym.getIndices()

    def getPartials(self):
        return self.partials

    def setIndices(self, sym):
        if type(sym) is SymmetryProperties:
            self.sym = sym
        else:
            raise TypeError

    # @param partials is a list
    def setPartials(self, partials):
        self.partials = list()
        for el in partials:
            if type(el) is Partial:
                self.partials.append(el)
            else:
                raise TypeError

    # calls symmetry properties pattern equality for deltas
    def patternEq(self, other):
        return self.getSym().patternEq(other.getSym())

    # calls symmetry properties pattern equality H for deltas (height of indices doesn't matter)
    def patternEqH(self, other):
        return self.getSym().patternEqH(other.getSym())

    # must be exactly equal - doesn't take into account summation patterns, etc
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
                strx += repr(el)
            strx += "\\(" + "\\delta" + repr(self.sym) + "\\)"
        else:
            strx += "\\delta" + repr(self.sym)
        return strx
