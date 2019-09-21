import copy
class Fraction:

    def __init__(self, num, den=1):
        self.num = num
        self.den = den

    def getNum(self):
        return self.num

    def getDen(self):
        return self.den

    def __repr__(self):
        if not self.den == 1:
            string = "\\frac{" + str(self.num) + "}{" + str(self.den) + "}"
        else:
            string = str(self.num)
        return string

    def lowestTerms(self):
        x = copy.deepcopy(self.den)
        while x > 0:
            if copy.deepcopy(self.num) % x == 0 and copy.deepcopy(self.den) % x == 0:
                return Fraction(int(self.num/x), int(self.den/x))
            x += -1
        return Fraction(self.num, self.den)

    def isNeg(self):
        if self.getNum() < 0:
            return True
        else:
            return False

    def __add__(self, other):
        #print("add ", self, other)
        if self.den == other.den:
            return Fraction((copy.deepcopy(self.num) + copy.deepcopy(other.num)), copy.deepcopy(self.den))
        else:
            return Fraction(((copy.deepcopy(self.num) * copy.deepcopy(other.den))+(copy.deepcopy(other.num) * copy.deepcopy(self.den))), copy.deepcopy(self.den)*copy.deepcopy(other.den)).lowestTerms()

    def __sub__(self, other):
        #print("sub ", self, other)
        if self.den == other.den:
            return Fraction((copy.deepcopy(self.num) - copy.deepcopy(other.num)), copy.deepcopy(self.den))
        else:
            return Fraction(((copy.deepcopy(self.num) * copy.deepcopy(other.den))-(copy.deepcopy(other.num)*copy.deepcopy(self.den))), copy.deepcopy(self.den)*copy.deepcopy(other.den)).lowestTerms()

    def __mul__(self, other):
        #print("mult ", self, other)
        return Fraction(copy.deepcopy(self.num)*copy.deepcopy(other.num), copy.deepcopy(self.den)*copy.deepcopy(other.den)).lowestTerms()

    def __truediv__(self, other):
        #print("div ", self, other)
        return Fraction(copy.deepcopy(self.num)*copy.deepcopy(other.den), copy.deepcopy(self.den)*copy.deepcopy(other.num)).lowestTerms()

    def __mod__(self, other):
        divided = copy.deepcopy(self)/copy.deepcopy(other)
        if divided.getDen() == 1:
            return Fraction(0)
        elif divided.getDen() > divided.getNum():
            return divided
        else:
            while divided.getDen() < divided.getNum():
                divided = divided - Fraction(1)
            return divided

    def __abs__(self):
        return Fraction(abs(copy.deepcopy(self.getNum())), copy.deepcopy(self.getDen()))

    def __gt__(self, other):
        return (copy.deepcopy(self.getNum())/copy.deepcopy(self.getDen())) > (copy.deepcopy(other.getNum())/copy.deepcopy(other.getDen()))

    def __lt__(self, other):
        return (copy.deepcopy(self.getNum())/copy.deepcopy(self.getDen())) < (copy.deepcopy(other.getNum())/copy.deepcopy(other.getDen()))

    def __eq__(self, other):
        copySel = copy.deepcopy(self)
        copyOth = copy.deepcopy(other)
        copySel.lowestTerms()
        copyOth.lowestTerms()
        if copySel.getNum() == copyOth.getNum() and copySel.getDen() == copyOth.getDen():
            return True
        else:
            return False




