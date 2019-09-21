import copy
from Tensors.Coefficient import Coefficient
from Tensors.Fraction import Fraction
class TensorCoefficients:

    def __init__(self, cos):
        self.cos = list()
        for el in cos:
            if type(el) is Coefficient:
                self.cos.append(el)
            else:
                raise TypeError("THIS IS NOT A COEFFICIENT: type is: ", type(el))
        self.isZero = False

    def getCos(self):
        return self.cos

    def getIsZero(self):
        return self.isZero

    def testSETListEquality(self, l1, l2):
        if not len(l1) == len(l2):
            return False
        l11 = copy.deepcopy(l1)
        l22 = copy.deepcopy(l2)
        for el1 in l1:
            found = False
            for el2 in l22:
                if not found and el2 == el1:
                    l22.remove(el2)
                    found = True
            if not found:
                return False
        for el2 in l2:
            found = False
            for el1 in l11:
                if not found and el1 == el2:
                    l11.remove(el1)
                    found = True
            if not found:
                return False
        return True

    def simplify(self):
        if len(self.cos) == 0:
            return
        numCo = Fraction(0)
        i = 0
        while i < len(self.cos):
            el = self.cos[i]
            if el.isJustNum():
                if el.getSign() == "-":
                    numCo = numCo - el.getNumCo()
                else:
                    numCo = numCo + el.getNumCo()
                self.cos.pop(i)
            else:
                i += 1
        #for el in copy.deepcopy(self.cos):
        #    if el.isJustNum():
        #        if el.getSign() == "-":
        #            numCo = numCo - el.getNumCo()
        #        else:
        #            numCo = numCo + el.getNumCo()
        #        self.cos.remove(el)
        if numCo != Fraction(0):
            if numCo.isNeg():
                self.cos.append(Coefficient("-", abs(numCo)))
            else:
                self.cos.append(Coefficient("+", numCo))
        i = 0
        while i < len(self.cos):
            j = i+1
            while j < len(self.cos):
                if self.cos[i] == self.cos[j]:
                    self.cos[i] = self.cos[i]*Coefficient("+", Fraction(2))
                    self.cos.pop(j)
                elif self.cos[i].combEq(self.cos[j]):
                    self.cos.pop(j)
                    self.cos.pop(i)
                    i += -1
                    j = len(self.cos)
                else:
                    j += 1
            i += 1
        s = 0
        while s < len(self.cos):
            q = s+1
            while q < len(self.cos):
                if self.cos[s].getSymCo() == self.cos[q].getSymCo():
                    if self.cos[s].getSign() == self.cos[q].getSign():
                        self.cos[s].setNumCo(self.cos[s].getNumCo() + self.cos[q].getNumCo())
                    else:
                        self.cos[s].setNumCo(self.cos[s].getNumCo() - self.cos[q].getNumCo())
                        if self.cos[s].getNumCo().isNeg():
                            self.cos[s].setNumCo(abs(self.cos[s].getNumCo()))
                            self.cos[s].changeSign()
                    self.cos.pop(q)
                    if self.cos[s].getNumCo() == Fraction(0):
                        self.cos.pop(s)
                        s += -1
                        q = len(self.cos)
                else:
                    q += 1
            s += 1
        if len(self.cos) == 0:
            self.cos.append(Coefficient("+", Fraction(0)))
            self.isZero = True

    def cleanCancellations(self):
        if len(self.cos) == 0:
            return
        i = 0
        while i < len(self.getCos()):
            j = i+1
            while j < len(self.getCos()):
                if self.getCos()[i].combEq(self.getCos()[j]):
                    if self.getCos()[i].getSign() == self.getCos()[j].getSign():
                        self.getCos()[i] = self.getCos()[i]*Coefficient("+", Fraction(2))
                        self.getCos().pop(j)
                    else:
                        self.getCos().pop(j)
                        self.getCos().pop(i)
                        i += -1
                        j = len(self.getCos())
                else:
                    j += 1
            i += 1
        if len(self.cos) == 0:
            self.cos.append(Coefficient("+", Fraction(0)))
            self.isZero = True

    def __add__(self, other):
        new = TensorCoefficients(self.getCos()+other.getCos())
        new.cleanCancellations()
        new.simplify()
        return new

    def __sub__(self, other):
        for el in other.getCos():
            el.changeSign()
        return self+other

    def __mul__(self, other):
        coefficients = list()
        for el1 in self.getCos():
            for el2 in other.getCos():
                el11 = copy.deepcopy(el1)
                el22 = copy.deepcopy(el2)
                coefficients.append(el11*el22)
        new = TensorCoefficients(coefficients)
        new.simplify()
        return new

    def __eq__(self, other):
        if self.testSETListEquality(self.getCos(), other.getCos()):
            return True
        else:
            return False

    def __repr__(self):
        if len(self.cos) == 0:
            return ""
        if len(self.cos) == 1:
            if self.cos[0].getSign() == "-":
                return "\("+repr(self.cos[0])+"\)"
            else:
                return repr(self.cos[0])
        strx = "\("
        for i in range(len(self.cos)):
            if i > 0:
                self.cos[i].setShowSign(True)
            strx += repr(self.cos[i])
        strx += "\) "
        return strx


