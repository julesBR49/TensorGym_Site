class Metric:

    def __init__(self, sym):
        self.sym = sym

    def getIndices(self):
        return self.sym.getIndices()

    def __eq__(self, other):
        if set(self.sym.getIndices()) == set(other.sym.getIndices()):
            return True
        else:
            return False

    def __repr__(self):
        stringRepr = "\\eta" + self.sym.toString()
        return stringRepr

