from Tensors.IndexException import IndexException
class Partial:

    def __init__(self, index):
        self.index = index
        self.square = False
        self.squarePartner = None

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def patternEq(self, other):
        return self.getIndex().patternEq(other.getIndex())

    def patternEqH(self, other):
        return self.getIndex().patternEqH(other.getIndex())

    def isSquare(self):
        return self.square

    def setSquarePartner(self, partial):
        self.square = True
        self.squarePartner = partial
        self.index.setPartnerInCrime(partial.getIndex())
        # if not partial.isSquare():
        #     partial.setSquarePartner(self)

    def getSquarePartner(self):
        return self.squarePartner

    def __eq__(self, other):
        if self.getIndex() == other.getIndex():
            return True
        else:
            return False

    def __repr__(self):
        strx = ''
        if ("square" in self.index.getIndex()): #or (self.index.getIndex() == "\\square"):
            if self.index.isUp():
                strx += "\\square "
        else:
            strx += "\\partial"
            if self.index.isUp():
                strx = strx + "^{" + self.index.getIndex() + "} "
            elif self.index.isDown():
                strx = strx + "_{" + self.index.getIndex() + "} "
            else:
                raise IndexException("Problem with height of " + self.index())
        return strx

