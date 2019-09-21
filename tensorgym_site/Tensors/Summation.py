from Tensors.TypeError import TypeError
from Tensors.Partial import Partial
from Tensors.Fraction import Fraction
from Tensors.TensorCoefficients import TensorCoefficients
from Tensors.SymbolCo import SymbolCo
from Tensors.Coefficient import Coefficient
import copy
class Summation:

    def __init__(self, sums=None, partials=None, sign="+", brackets=False):
        self.brackets = brackets
        self.summation = list()
        if sums is not None:
            for i in range(len(sums)):
                if i == 0:
                    self.summation.append(sums[i])
                else:
                    sums[i].setShowSign(True)
                    self.summation.append(sums[i])
        self.partials = list()
        if partials is not None:
            for el in partials:
                if type(el) is Partial:
                    self.partials.append(el)
                else: raise TypeError
        self.sign = sign
        if len(self.summation) > 1 or len(self.partials) > 0:
            self.brackets = True

    def isZero(self):
        if (len(self.summation) == 1) and (self.summation[0].getNumCo() == Fraction(0)):
            return True
        else:
            return False

    def getSign(self):
        return self.sign

    def setSign(self, s):
        self.sign = s

    def changeSign(self, sign):
        self.sign = sign

    def swapSign(self):
        if self.sign == "+":
            self.setSign("-")
        else:
            self.setSign("+")

    def setBrackets(self, bool):
        self.brackets = bool

    def hasBrackets(self):
        if self.brackets: return True
        else: return False

    def getSums(self):
        return self.summation

    def getPartials(self):
        return self.partials

    def addPartial(self, newPartial):
        if type(newPartial) is Partial:
            self.partials.append(newPartial)

    def setPartials(self, partials):
        self.partials = partials

    def addPartials(self, listPs):
        if type(listPs) is list:
            for p in listPs:
                self.addPartial(p)
        else:
            self.addPartial(listPs)

    def hasPartials(self):
        return len(self.partials) > 0

    def distributeSign(self):
        if self.sign == "-":
            for summy in self.summation:
                summy.swapSign()
            self.changeSign("+")

    def removeTerm(self, term):
        if term in self.summation:
            self.summation.remove(term)


    def addTerm(self, newTerm):
        self.summation.append(newTerm)
        if len(self.summation) > 1:
            self.brackets = True
            for i in range(1, len(self.summation)):
                self.summation[i].setShowSign(True)

    def replaceTerm(self, oldTerm, newTerm):
        done = False
        for s in range(len(self.summation)):
            if not done:
                if self.summation[s] == oldTerm:
                    self.summation[s] = newTerm
                    done = True


    def remZeroTerms(self):
        if len(self.summation) == 0:
            return
        zeroMult = copy.deepcopy(self.summation[0]).setZero()
        for summy in copy.deepcopy(self.summation):
            if summy.getNumCo() == Fraction(0):
                self.removeTerm(summy)
        if len(self.summation) == 0:
            self.addTerm(zeroMult)
        return


    #def distributePartials(self):
    #    for i in range(len(self.summation)):
    #        for p in range(len((self.partials))):
    #            self.summation[i].addPartials(self.partials[p])
    #    self.partials = list()
    #    self.summation.sort()

    def sortEach(self):
        for mult in self.summation:
            mult.sort()

    def sortTerms(self):
        self.summation.sort()

    def __repr__(self):
        self.remZeroTerms()
        if len(self.summation) > 1: #or (len(self.summation) == 1 and self.summation[0].getSign() == "-"):
            self.setBrackets(True)
        if (len(self.summation) > 0) and self.brackets and (self.summation[0].getSign() == "+"):
            self.summation[0].setShowSign(False)
        strx = ""
        if self.sign == "-":
            strx += self.sign
        for i in range(len(self.partials)):
            strx += repr(self.partials[i])
        if self.brackets:
            strx += "\\("
        for i in range(len(self.summation)):
            if i == 0 and self.summation[i].getSign() == "+":
                self.summation[i].setShowSign(False)
            if i > 0:
                self.summation[i].setShowSign(True)
            strx += repr(self.summation[i])
        if self.brackets:
            strx += "\\)"
        return strx

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

    def combineLikeTerms(self):
        if len(self.summation) == 0:
            return
        zeroMult = copy.deepcopy(self.summation[0]).setZero()
        i = 0
        for summy in self.summation:
            summy.combineCoefficients()
            summy.setSums()
        while i < len(self.summation):
            currentTerm = self.summation[i]
            j = i+1
            while j < len(self.summation):
                testTerm = self.summation[j]
                if currentTerm.combEq(testTerm):
                    self.summation.pop(j)
                    if currentTerm.getSign() == testTerm.getSign():  # if same sign add coefficients
                        currentTerm.setTensorCos(currentTerm.getTensorCos()+testTerm.getTensorCos())
                        #self.summation.pop(j)
                    else:  # subtract coefficients
                        currentTerm.setTensorCos(currentTerm.getTensorCos()-testTerm.getTensorCos())
                        if currentTerm.getTensorCos() == TensorCoefficients([Coefficient("-", Fraction(1))]):
                            currentTerm.setTensorCos([Coefficient()])
                            currentTerm.swapSign()
                        if currentTerm.getTensorCos().getIsZero():  # get rid of BOTH and start again
                            self.summation.pop(i)
                            i += -1
                            #self.summation.pop(j-1)
                            j = len(self.summation)  # this term is gone so we no longer test against it
                        #else:
                        #    self.summation.pop(j)
                else:
                    j += 1
            i += 1
        if len(self.summation) == 0:
            self.addTerm(zeroMult)

    def remRef(self, mult):
        for i in range(len(self.summation)):
            if self.summation[i] is mult:
                self.summation.pop(i)
                return

    def combineLikeTermsWithoutSymCo(self):
        if len(self.summation) == 0:
            return
        zeroMult = copy.deepcopy(self.summation[0]).setZero()
        i = 0
        while i < len(self.summation):
            currentTerm = self.summation[i]
            j = i+1
            while j < len(self.summation):
                testTerm = self.summation[j]
                #print("current term: ", currentTerm.getTensorCos(), type(currentTerm.getTensorCos()), "test term: ", testTerm.getTensorCos(), type(testTerm.getTensorCos()))
                if type(currentTerm.getTensorCos()) is TensorCoefficients and type(testTerm.getTensorCos()) is TensorCoefficients:

                    if currentTerm.combEq(testTerm) and (currentTerm.getSymbolCo() == testTerm.getSymbolCo()) and (currentTerm.getTensorCos() == testTerm.getTensorCos()):
                        self.summation.pop(j)
                        if currentTerm.getSign() == testTerm.getSign():  # if same sign add coefficients
                            currentTerm.setNumCo(currentTerm.getNumCo()+testTerm.getNumCo())
                            #self.summation.pop(j)
                        else:  # subtract coefficients
                            currentTerm.setNumCo(currentTerm.getNumCo()-testTerm.getNumCo())
                            if currentTerm.getNumCo() < Fraction(0):
                                currentTerm.setNumCo(abs(currentTerm.getNumCo()))
                                currentTerm.swapSign()
                            elif currentTerm.getNumCo() == Fraction(0):  # get rid of BOTH and start again
                                self.summation.pop(i)
                                i += -1
                                #self.summation.pop(j-1)
                                j = len(self.summation)  # this term is gone so we no longer test against it
                            #else:
                                #self.summation.pop(j)
                    else:
                        j += 1
                else:
                    raise TypeError("not tensor cos")
            i += 1
        if len(self.summation) == 0:
            self.addTerm(zeroMult)

    def removePartial(self, partial):
        if partial in self.partials:
            self.partials.remove(partial)

    def __add__(self, other):
        self.remZeroTerms()
        other.remZeroTerms()
        if other.isZero():
            return self
        if self.isZero():
            return other
        self.distributeSign()
        other.distributeSign()
        if self.hasPartials():
            self.distributePartials()
        if other.hasPartials():
            other.distributePartials()
        #self.removeSumsWithinMult()
        #other.removeSumsWithinMult()
        return Summation(copy.deepcopy(self.getSums()) + copy.deepcopy(other.getSums()))


    def noPAdd(self, other):
        self.remZeroTerms()
        other.remZeroTerms()
        if other.isZero():
            return self
        if self.isZero():
            return other
        self.distributeSign()
        other.distributeSign()
        #self.distributePartials()
        #other.distributePartials()
        #self.removeSumsWithinMult()
        #other.removeSumsWithinMult()
        if len(self.getPartials()) == 0 and len(other.getPartials()) == 0:
            return Summation(copy.deepcopy(self.getSums()) + copy.deepcopy(other.getSums()))
        else:
            raise TypeError("cannot add/ subtract terms under a derivative")

    def __sub__(self, other):
        if self.getSign() == "+":
            self.changeSign("-")
        else:
            self.changeSign("+")
        return self+other

    def noPSub(self, other):
        if self.getSign() == "+":
            self.changeSign("-")
        else:
            self.changeSign("+")
        return self.noPAdd(other)

    def removeSumsWithinMult(self):
        sums = copy.deepcopy(self.getSums())
        for term in sums:
            toRem = copy.deepcopy(term)
            self.removeTerm(term)
            toRem = toRem.multOutSums()  # is now a summation object
            for sum in toRem.getSums():
                self.addTerm(sum)

    def distributePartials(self):
        while len(self.partials) > 0:
            partial = self.partials[0]
            self.summation = copy.deepcopy(self.distributePartial(partial).getSums())  # replace sums list with product rule
            self.removePartial(partial)

    def distributePartial(self, partial):
        if partial is None:
            return self
        else:
            sums = Summation()
            for multiplication in self.getSums():
                productRuleOfSum = multiplication.distributePartial(copy.deepcopy(partial), copy.deepcopy(multiplication.getTensors()) + copy.deepcopy(multiplication.getVariations()))  # returns a summation object
                sums = sums+productRuleOfSum
            return sums  # summation object with no derivatives

    def __mul__(self, other):
        self.remZeroTerms()
        other.remZeroTerms()
        if self.isZero():
            return copy.deepcopy(self)
        if other.isZero():
            return copy.deepcopy(other)
        if self.getSign() == other.getSign():
            sign = "+"
        else:
            sign = "-"
        if len(self.getSums()) == 1:
            if self.getSums()[0].isOnlyPartials():
                other.addPartials(self.getSums()[0].getPartials())
                self.getSums()[0].setPartials(list())
        if len(other.getSums()) == 1:
            if other.getSums()[0].isOnlyPartials():
                self.addPartials(other.getSums()[0].getPartials())
                other.getSums()[0].setPartials(list())
        if self.hasPartials():
            self.distributePartials()
        if other.hasPartials():
            other.distributePartials()
        sumsList = list()
        for sum1 in self.getSums():
            for sum2 in other.getSums():
                sumsList.append(copy.deepcopy(sum1)*copy.deepcopy(sum2))
        return Summation(sumsList, list(), sign)

    def noPMul(self, other):
        self.remZeroTerms()
        other.remZeroTerms()
        if self.isZero():
            return copy.deepcopy(self)
        if other.isZero():
            return copy.deepcopy(other)
        if self.getSign() == other.getSign():
            sign = "+"
        else:
            sign = "-"
        if len(self.getSums()) == 1:
            if self.getSums()[0].isOnlyPartials():
                other.addPartials(self.getSums()[0].getPartials())
                self.getSums()[0].setPartials(list())
                for t in range(len(other.getSums())):
                    #other.replaceTerm(term, term*self.getSums()[0])
                    other.getSums()[t] = other.getSums()[t]*self.getSums()[0]
                return other
        if len(other.getSums()) == 1:
            if other.getSums()[0].isOnlyPartials():
                self.addPartials(other.getSums()[0].getPartials())
                other.getSums()[0].setPartials(list())
                for t in range(len(self.getSums())):
                    #self.replaceTerm(term, term*other.getSums()[0])
                    self.getSums()[t] = self.getSums()[t]*other.getSums()[0]
                return self
        #self.distributePartials()
        #other.distributePartials()
        if len(self.getPartials()) == 0 and len(other.getPartials()) == 0:
            sumsList = list()
            for sum1 in self.getSums():
                for sum2 in other.getSums():
                    sumsList.append(copy.deepcopy(sum1)*copy.deepcopy(sum2))
            return Summation(sumsList, list(), sign)
        else:
            raise TypeError("cannot multiply terms under a derivative")

    def multOutPartials(self, other):
        self.remZeroTerms()
        other.remZeroTerms()
        if self.getSign() == other.getSign():
            sign = "+"
        else:
            sign = "-"
        if len(self.getSums()) == 1:
            if self.getSums()[0].isOnlyPartials():
                other.addPartials(self.getSums()[0].getPartials())
                self.getSums()[0].setPartials(list())
                for t in range(len(other.getSums())):
                    #other.replaceTerm(term, term*self.getSums()[0])
                    other.getSums()[t] = other.getSums()[t]*self.getSums()[0]
                return other
        if len(other.getSums()) == 1:
            if other.getSums()[0].isOnlyPartials():
                self.addPartials(other.getSums()[0].getPartials())
                other.getSums()[0].setPartials(list())
                for t in range(len(self.getSums())):
                    #self.replaceTerm(term, term*other.getSums()[0])
                    self.getSums()[t] = self.getSums()[t]*other.getSums()[0]
                return self
        raise TypeError("cannot multiply partials if no partial")

    def multList(self, list):
        if len(list) == 0:
            raise TypeError("list MUST HAVE ELEMENTS!!!")
        if (len(list) == 1):
            return list[0]
        elif len(list) == 2:
            return list[0]*list[1]
        else:
            return list[0]*self.multList(list[1:])

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

    def testPatternSETListEqualityH(self, l1, l2):
        if not len(l1) == len(l2):
            return False
        l11 = copy.deepcopy(l1)
        l22 = copy.deepcopy(l2)
        for el in l1:
            found = False
            for el2 in l22:
                if not found and el2.patternEqH(el):
                    l22.remove(el2)
                    found = True
            if not found:
                return False
        for el in l2:
            found = False
            for el1 in l11:
                if not found and el1.patternEqH(el):
                    l11.remove(el1)
                    found = True
            if not found:
                return False
        return True

    def patternEqIncludes(self, other):
        if not (other.getPartials() == list() or self.testPatternSETListEquality(self.getPartials(), other.getPartials())):
            return False
        selfSums = copy.deepcopy(self.getSums())
        for el in other.getSums():
            found = False
            for elS in selfSums:
                if not found and el.patternEq(elS):
                    found = True
                    selfSums.remove(elS)
            if not found:
                return False
        return True

    def patternEqIncludesH(self, other):
        if not (other.getPartials() == list() or self.testPatternSETListEqualityH(self.getPartials(), other.getPartials())):
            return False
        selfSums = copy.deepcopy(self.getSums())
        for el in other.getSums():
            found = False
            for elS in selfSums:
                if not found and el.patternEqH(elS):
                    found = True
                    selfSums.remove(elS)
            if not found:
                return False
        return True

    def patternEq(self, other):
        if not(self.testPatternSETListEquality(self.getPartials(), other.getPartials())):
            return False
        if not(self.testPatternSETListEquality(self.getSums(), other.getSums())):
            return False
        return True

    def patternEqH(self, other):
        if not(self.testPatternSETListEqualityH(self.getPartials(), other.getPartials())):
            return False
        if not(self.testPatternSETListEqualityH(self.getSums(), other.getSums())):
            return False
        return True

    def getIndices(self):
        retList = list()
        for p in self.getPartials():
            retList.append(p.getIndex())
        for summy in self.getSums():
            retList += summy.getIndices()
        return retList

    def getSortedIndicesList(self):
        indsList = list()
        for partial in self.getPartials():
            indsList.append([partial.getIndex()])
        for summy in self.getSums():
            indsList.append(summy.getSortedIndicesList())
        indsList.sort()
        retList = list()
        for el in indsList:
            for el2 in el:
                retList.append(el2)
        return retList

    def changeIndicesMult(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesList(fromMultList, toMultList)

    def changeIndicesMultH(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesListH(fromMultList, toMultList)

    def changeIndicesMultHNOSUMS(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesListHNOSUMS(fromMultList, toMultList)

    def changeIndicesSum(self, fromSum, toSum):
        fromSumList = fromSum.getSortedIndicesList()
        toSumList = toSum.getSortedIndicesList()
        self.changeIndicesList(fromSumList, toSumList)

    def changeIndicesList(self, fromList, toList):
        if len(fromList) != len(toList):
            raise TypeError("indices to replace do not match in length!")
        for i in range(len(fromList)):
            if not fromList[i].patternEq(toList[i]):
                raise TypeError("these indices are not replaceable - they have different summation types")
            toChange = self.getEqualIndices(fromList[i])
            for ind in toChange:
                ind.setIndex(toList[i].getIndex() + "%")
        for newInd in self.getIndices():
            if not (newInd.getIndex() == "\\ "):
                newInd.changeIndex(newInd.getIndex().replace("%", ""))

    def changeIndicesListH(self, fromList, toList):
        if len(fromList) != len(toList):
            raise TypeError("indices to replace do not match in length!")
        for i in range(len(fromList)):
            if not fromList[i].patternEqH(toList[i]):
                raise TypeError("these indices are not replaceable - they have different summation types")
            toChange = self.getEqualIndicesH(fromList[i])
            for ind in toChange:
                if ind.getHeight() != toList[i].getHeight():
                    ind.changeHeight()
                ind.setIndex(toList[i].getIndex() + "%")
        for newInd in self.getIndices():
            if not (newInd.getIndex() == "\\ "):
                newInd.changeIndex(newInd.getIndex().replace("%", ""))

    def simplestChangeIndicesList(self, fromList, toList):
        if len(fromList) != len(toList):
            raise TypeError("indices to replace do not match in length!")
        for i in range(len(fromList)):
            toChange = self.getEqualIndices(fromList[i])
            for ind in toChange:
                ind.setIndex(toList[i].getIndex() + "%")
        for newInd in self.getIndices():
            if not (newInd.getIndex() == "\\ "):
                newInd.changeIndex(newInd.getIndex().replace("%", ""))

    def changeIndicesListHNOSUMS(self, fromList, toList):
        if len(fromList) != len(toList):
            raise TypeError("indices to replace do not match in length!")
        for i in range(len(fromList)):
            #if not fromList[i].patternEqH(toList[i]):
            #    raise TypeError("these indices are not replaceable - they have different summation types")
            toChange = self.getEqualIndicesH(fromList[i])
            for ind in toChange:
                if ind.getHeight() != toList[i].getHeight():
                    ind.changeHeight()
                ind.setIndex(toList[i].getIndex() + "%")
        for newInd in self.getIndices():
            if not (newInd.getIndex() == "\\ "):
                newInd.changeIndex(newInd.getIndex().replace("%", ""))

    def getEqualIndices(self, index):
        pointer = list()
        for p in self.getPartials():
            if p.getIndex().basicEquals(index):
                pointer.append(p.getIndex())
        for summy in self.summation:
            for ind in summy.getEqualIndices(index):
                pointer.append(ind)
        return pointer

    def getEqualIndicesH(self, index):
        pointer = list()
        for p in self.getPartials():
            if p.getIndex().basicEquals(index) and (p.getIndex().getHeight() == index.getHeight()):
                pointer.append(p.getIndex())
        for summy in self.summation:
            for ind in summy.getEqualIndicesH(index):
                pointer.append(ind)
        return pointer

    def __eq__(self, other):
        if self.getSign() != other.getSign():
            return False
        if not self.testSETListEquality(self.getPartials(), other.getPartials()):
            return False
        if not self.testSETListEquality(self.getSums(), other.getSums()):
            return False
        return True





