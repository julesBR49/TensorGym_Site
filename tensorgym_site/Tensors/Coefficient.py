from Tensors.Fraction import Fraction
from Tensors.SymbolCo import SymbolCo
# a chunk that holds coefficient information: a sign and up to one number and one symbolic coefficient
class Coefficient:
    def __init__(self, sign="+", numCo=None, symCo=None):
        self.sign = sign
        if numCo is None:
            self.numCo = Fraction(1)
        else:
            self.numCo = numCo
        if symCo is None:
            self.symCo = SymbolCo()
        else:
            self.symCo = symCo
        self.showSign = False
        if self.sign == "-":
            self.showSign = True

    def isJustNum(self):
        if (self.symCo == SymbolCo()) and (self.numCo != Fraction(1)):
            return True
        else:
            return False

    def isJustSymb(self):
        if (self.symCo != SymbolCo()) and (self.numCo == Fraction(1)):
            return True
        else:
            return False

    def getSign(self):
        return self.sign

    def setSign(self, sign):
        self.sign = sign
        if self.sign == "-":
            self.setShowSign(True)
        else:
            self.setShowSign(False)

    def changeSign(self):
        if self.sign == "+":
            self.sign = "-"
            self.setShowSign(True)
        else:
            self.sign = "+"
            self.setShowSign(False)

    def getNumCo(self):
        return self.numCo

    def getSymCo(self):
        return self.symCo

    def setNumCo(self, co):
        self.numCo = co

    def setSymCo(self, co):
        self.symCo = co

    def setShowSign(self, booly):
        self.showSign = booly

    ## same but sign doesn't have to match
    def combEq(self, other):
        if (self.getNumCo() == other.getNumCo()) and (self.getSymCo() == other.getSymCo()):
            return True
        else:
            return False

    def __mul__(self, other):
        if self.sign == other.sign:
            sign = "+"
        else:
            sign = "-"
        numCo = self.getNumCo()*other.getNumCo()
        symCo = self.getSymCo()*other.getSymCo()
        return Coefficient(sign, numCo, symCo)

    def __eq__(self, other):
        if (self.getSign() == other.getSign()) and (self.getNumCo() == other.getNumCo()) and (self.getSymCo() == other.getSymCo()):
            return True
        else:
            return False

    def __repr__(self):
        strx = ""
        if self.showSign:
            strx += self.sign
        if self.numCo != Fraction(1):
            strx += repr(self.numCo)
        if self.symCo != SymbolCo():
            strx += repr(self.symCo)
        return strx



