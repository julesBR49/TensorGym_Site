from Tensors.Gemma import Gemma
class Index:
    #symbol is string, up = 1, down = 0
    def __init__(self, symbol, height=1, owner='', summ=False, crossSum=False, sumType=None):
        self.symbol = symbol
        self.height = height
        self.sum = summ
        self.crossSum = crossSum
        self.partnerInCrime = None
        if sumType is None:
            self.sumType = Gemma()
        else:
            self.sumType = sumType
        self.owner = owner

    def isUp(self):
        if self.height == 1:
            return True
        else:
            return False

    def isDown(self):
        if self.height == 0:
            return True
        else:
            return False

    def raiseIndex(self):
        self.height = 1

    def lowerIndex(self):
        self.height = 0

    def changeIndex(self, newSymbol):
        self.symbol = newSymbol

    def getSymbol(self):
        if self.symbol == "\\%":
            return "\\ "
        else:
            return self.symbol

    def setIndex(self, newSym):
        self.symbol = newSym

    def getIndex(self):
        if self.symbol == "\\%":
            return "\\ "
        else:
            return self.symbol

    def getHeight(self):
        return self.height

    def changeHeight(self):
        if self.height == 0:
            self.height = 1
        else:
            self.height = 0

    def hasSum(self):
        return self.sum

    def getOwner(self):
        return self.owner

    def setOwner(self, owner):
        self.owner = owner

    def addOwner(self, owner):
        self.owner += owner

    def getSumType(self):
        return self.sumType  # SumType object

    def setSumType(self, sumType):
        if type(sumType) is Gemma:
            self.sumType = sumType
        elif type(sumType) is list:
            self.sumType.setType(sumType)
        elif type(sumType) is set:
            self.sumType.setType(list(sumType))

    def hasCrossSum(self):
        return self.crossSum

    def changeSum(self, summ, partner=None):
        self.sum = summ
        self.partnerInCrime = partner

    def getPartnerInCrime(self):
        return self.partnerInCrime

    def setSum(self, summ, partner=None):
        self.sum = summ
        self.partnerInCrime = partner

    def changeCrossSum(self, newSum):
        self.crossSum = newSum

    def sumsWith(self, other):
        if self.symbol.replace(" ", "") == other.getIndex().replace(" ", "") and self.height != other.getHeight():
            return True
        else:
            return False

    def basicEquals(self, other):
        if self.getIndex().replace(" ", "") == other.getIndex().replace(" ", ""):
            return True
        else:
            return False

    def basicEqualsH(self, other):
        if (self.getIndex().replace(" ", "") == other.getIndex().replace(" ", "")) and (self.getHeight() == other.getHeight()):
            return True
        else:
            return False

    def patternEq(self, other):
        if self.getSumType() != other.getSumType():
            return False
        if self.hasSum() and other.hasSum():
            return True
        if self.getHeight() == other.getHeight():
            return True
        return False

    def patternEqH(self, other):
        if self.getSumType() != other.getSumType():
            return False
        return True

    def getKey(self):
        selfKey = ''
        for el in sorted(self.getOwner()):
            selfKey += el
        self.getSumType().sort()
        for el in self.getSumType().getType():
            selfKey += el
        return selfKey

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __gt__(self, other):
        return self.getKey() > other.getKey()

    def __le__(self, other):
        return self.getKey() <= other.getKey()

    def __ge__(self, other):
        return self.getKey() >= other.getKey()

    def __eq__(self, other):
        if not(self.getSumType() == other.getSumType()):
            return False
        if self.hasSum() and other.hasSum():
            return True
        elif self.hasSum() and (other.getIndex() == "\\ "):
            return True
        elif (self.getIndex() == "\\ ") and other.hasSum():
            return True
        elif self.hasSum() or other.hasSum():
            return False
        elif (self.getIndex().replace(" ", "") == other.getIndex().replace(" ", "")) and (self.getHeight() == other.getHeight()):
            return True
        else:
            return False

    def __repr__(self):
        if self.symbol == "\\%":
            return "\\ "
        else:
            return self.symbol



