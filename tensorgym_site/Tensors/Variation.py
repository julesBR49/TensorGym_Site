import copy
class Variation:
    def __init__(self, num, den, kind="\\partialv", partials=None, sign="+", brackets=False):
        self.brackets = brackets
        self.kind = kind
        self.num = num  # summation
        self.trueDen = den
        self.den = self.switchHeight(den)
        self.partials = list()
        if partials is not None:
            for el in partials:
                self.partials.append(el)
        self.sign = sign
        if self.num.getSign() != self.den.getSign():
            self.changeSign()
        self.num.setSign("+")
        self.den.setSign("+")
        self.PVSums = 0
        self.setPVSums()
        self.ownerHash = self.kind+str(self.numPVSums)
        self.setSums()

    def reinitOwnerHash(self):
        self.ownerHash = self.kind+str(self.numPVSums)

    def getOwnerHash(self):
        self.reinitOwnerHash()
        return self.ownerHash

    def setPVSums(self):
        self.numPVSums = 0
        varInds = self.getVarIndices()
        for p in self.partials:
            summed = False
            for v in varInds:
                if not summed and p.getIndex().sumsWith(v):
                    p.getIndex().setSum(True)
                    summed = True
                    self.numPVSums += 1

    def getSign(self):
        return self.sign

    def changeSign(self):
        if self.sign == "+":
            self.sign = "-"
        else:
            self.sign = "+"

    def setSign(self, newSign):
        self.sign = newSign

    def getPartials(self):
        return self.partials

    def getNum(self):
        return self.num

    def getDen(self):
        return self.den

    def getTrueDen(self):
        return self.trueDen

    def getKind(self):
        return self.kind

    def changeNum(self, num):
        self.num = num

    def changeDen(self, den):
        self.den = den

    def changeTrueDen(self, den):
        self.trueDen = self.switchHeight(den)

    def changePartials(self, partials):
        self.partials = partials

    def setPartials(self, ps):
        self.partials = ps
        self.setPVSums()

    def addPartials(self, newP):
        self.partials.append(newP)
        self.setSums()
        self.setPVSums()

    def addPartial(self, newP):
        self.partials.append(newP)
        self.setSums()
        self.setPVSums()

    def getEqualIndices(self, index):
        pointer = list()
        topL = self.getNum().getEqualIndices(index)
        botL = self.getDen().getEqualIndices(index)
        pointer = pointer + topL + botL
        for p in self.getPartials():
            if p.getIndex().basicEquals(index):
                pointer.append(p.getIndex())
        return pointer

    def getEqualIndicesH(self, index):
        pointer = list()
        #topL = self.getNum().getEqualIndicesH(index)
        #botL = self.getDen().getEqualIndicesH(index)
        for ind in self.getNum().getEqualIndicesH(index):
            pointer.append(ind)
        for ind in self.getDen().getEqualIndicesH(index):
            pointer.append(ind)
        for p in self.getPartials():
            if p.getIndex().basicEqualsH(index):
                pointer.append(p.getIndex())
        return pointer

    def __repr__(self):
        self.changeTrueDen(self.getDen())
        string = " "
        for partial in self.partials:
            string = string + repr(partial)
        if self.brackets:
            string = string + "\\("
        string = string + "\\frac{ " + self.kind
        if not self.getNum().hasBrackets():
            string += "(" + repr(self.num) + ")"
        else:
            string += repr(self.num)
        string += "}{" + self.kind
        if not self.getDen().hasBrackets():
            string += "(" + repr(self.trueDen) + ")"
        else:
            string += repr(self.trueDen)
        string += "}"
        if self.brackets:
            string += "\\("
        return string

    def testPatternSETListEquality(self, l1, l2):
        if not len(l1) == len(l2):
            return False
        l11 = copy.deepcopy(l1)
        l22 = copy.deepcopy(l2)
        for el in l1:
            found = False
            for el2 in l22:
                if not found and el2.patternEq(el):
                    l22.remove(el2)
                    found = True
            if not found:
                return False
        for el in l2:
            found = False
            for el1 in l11:
                if not found and el1.patternEq(el):
                    l11.remove(el1)
                    found = True
            if not found:
                return False
        return True

    def setSums(self):
        for topSum in self.getNum().getSums():
            for topInd in topSum.getIndices():
                topInd.addOwner("vn")
        for botSum in self.getDen().getSums():
            for botInd in botSum.getIndices():
                botInd.addOwner("vd")
        for p in self.getPartials():
            p.getIndex().addOwner("vp")
        hashy = self.getOwnerHash()
        for index in self.getFullIndices():
            index.addOwner(hashy)
        indices = self.getFullIndices()
        for i in range(len(indices)):
            sums = False
            possSum = copy.deepcopy(indices[i])
            for j in range(i+1, len(indices)):
                if indices[j].sumsWith(possSum):
                    indices[i].setSum(True)
                    indices[j].setSum(True)
                    sumType = set()
                    sumType.add(indices[i].getOwner())
                    sumType.add(indices[j].getOwner())
                    indices[i].setSumType(sumType)
                    indices[j].setSumType(sumType)
                    sums = True
            if not sums:
                indices[i].setSum(False)
                indices[i].setSumType(set())

    def testPatternSETListEqualityH(self, l1, l2):
        if not len(l1) == len(l2):
            return False
        l11 = copy.deepcopy(l1)
        l22 = copy.deepcopy(l2)
        for el in l1:
            found = False
            for el2 in l22:
                if el2.patternEqH(el) and not found:
                    l22.remove(el2)
                    found = True
            if not found:
                return False
        for el in l2:
            found = False
            for el1 in l11:
                if el1.patternEqH(el) and not found:
                    l11.remove(el1)
                    found = True
            if not found:
                return False
        return True

    def patternEq(self, other):
        if not self.testPatternSETListEquality(self.getPartials(), other.getPartials()):
            return False
        if not(self.getKind() == other.getKind()):
            return False
        if not self.getNum().patternEq(other.getNum()):
            return False
        if not self.getDen().patternEq(other.getDen()):
            return False
        return True

    def patternEqH(self, other):
        if not self.testPatternSETListEqualityH(self.getPartials(), other.getPartials()):
            return False
        if not(self.getKind() == other.getKind()):
            return False
        if not self.getNum().patternEqH(other.getNum()):
            return False
        if not self.getDen().patternEqH(other.getDen()):
            return False
        return True

    def __eq__(self, other):
        if self.getSign() != other.getSign():
            return False
        if self.getKind() != other.getKind():
            return False
        if not self.testSETListEquality(self.getPartials(), other.getPartials()):
            return False
        if not self.getNum() == other.getNum():
            return False
        if not self.getTrueDen() == other.getTrueDen():
            return False
        return True


    def switchHeight(self, realDen):
        den = copy.deepcopy(realDen)
        for i in range(len(den.getSums())):
            for j in range(len(den.getSums()[i].getTensors())):
                for h in range(len(den.getSums()[i].getTensors()[j].getPartials())):
                    den.getSums()[i].getTensors()[j].getPartials()[h].getIndex().changeHeight()
                for h in range(len(den.getSums()[i].getTensors()[j].getIndices())):
                    den.getSums()[i].getTensors()[j].getIndices()[h].changeHeight()
            for e in range(len(den.getSums()[i].getEtas())):
                for j in range(len(den.getSums()[i].getEtas()[e].getIndices())):
                    den.getSums()[i].getEtas()[e].getIndices()[j].changeHeight()
            for d in range(len(den.getSums()[i].getDeltas())):
                for j in range(len(den.getSums()[i].getDeltas()[d].getIndices())):
                    den.getSums()[i].getDeltas()[d].getIndices()[j].changeHeight()
        return den

    def getFullIndices(self):
        partialList = list()
        for partial in self.getPartials():
            partialList.append(partial.getIndex())
        partialList.sort()
        numSumsList = list()
        for numSum in self.getNum().getSums():
            numSumsList.append(numSum.getSortedIndicesList())
        denSumsList = list()
        for denSum in self.getDen().getSums():
            denSumsList.append(denSum.getSortedIndicesList())
        numSumsList.sort()
        denSumsList.sort()
        retList = list()
        for el in partialList:
            retList.append(el)
        #retList += partialList
        for el in numSumsList:
            for el2 in el:
                retList.append(el2)
        for el in denSumsList:
            for el2 in el:
                retList.append(el2)
        return retList

    def getVarIndices(self):
        numSumsList = list()
        for numSum in self.getNum().getSums():
            numSumsList.append(numSum.getSortedIndicesList())
        denSumsList = list()
        for denSum in self.getDen().getSums():
            denSumsList.append(denSum.getSortedIndicesList())
        numSumsList.sort()
        denSumsList.sort()
        retList = list()
        for el in numSumsList:
            for el2 in el:
                retList.append(el2)
        for el in denSumsList:
            for el2 in el:
                retList.append(el2)
        return retList

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




