_author_ = 'Bruce-Robertson'
from Tensors.TypeError import TypeError
from Tensors.SymmetryProperties import SymmetryProperties
from Tensors.IndexException import IndexException
from Tensors.Index import Index
from Tensors.Gemma import Gemma
from Tensors.functions import displayPartialList
import copy
class Tensor:


    """
    A class used to represent a Tensor

    ...

    Attributes
    ----------
    symbol : str
        the symbol representing the tensor (in LaTeX notation)
    symmetry : SymmetryProperties
        object that holds the indices for the tensor
    isSymmetric : boolean
        defines whether the tensor is a symmetric tensor
    partials : list<Partial>
    
    sign : string
    symTenSym : list<string>
    numTSums : int
    numPTSums : int
    rank : int
    numPartials : int
    ownerHash : string
        used for equality testing


    Methods
    -------
    reinitOwnerHash(self)
        updates the value of ownerHash
    getOwnerHash(self)
        updates and then returns the ownerHash
    setTSums(self)
        calculates and sets the value of numTSums based on the current properties of the tensors indices
    setPTSums(self)
        calculates and sets the value of numPTSums based on the current properties of the tensors indices and partial derivative indices
    setSums(self)
        TODO: figure out exactly what this function does - I think it sets the sum types for the indices belonging to the tensor and partials
    changeSymmetry(self, newSymmetry)
        sets isSymmetric value
    getIsSymmetric(self)
        returns isSymmetric value
    getSym(self)
        returns symmetry attribute (SymmetryProperties object)
    getSymbol(self)
        returns the tensory symbol (a string)
    addPartial(self, p)
        adds a partial derivative to p and resets the summation pattern
    getIndices(self)
        returns the indices of the tensor (a list<Index>)
    getAllIndices(self)
        returns a list with the first elements being the indices belonging to the partials and the last element a list of the indices belonging to the tensor
    getSeparateIndices(self)
        returns a list<Index> containing the indices of the partial derivatives, in order, followed by the indices of the tensor as seperate elements
    getPartials(self)
        returns a list<Partial> containing the tensor's partial derivatives
    getNumPartials(self)
        returns the number of partials, an int
    getRank(self)
        returns the rank of the tensor, an int
    getNumTSums(self)
        returns the number of sums within the tensor's indices, an int
    getNumPTSums(self):
        returns the number of sums between the tensor and its partial derivatives, an int
    getSign(self)
        returns the sign of the tensor, a string ("+" or "-")
    changeSign(self, newSign)
        sets the sign of the tensor, a string ("+" or "-")
    addPartials(self, partial)
        adds a partial object to the tensor and resets the sums (TODO again should it reset here?)

    """

    ## Constructs a tensor
    # @param symbol a string
    # @param sym a symmetry property object - essentially it holds the indices for the tensor
    # @param partials a list of partial objects - these are the partial derivatives acting on the tensor
    # @param isSymmetric boolean - defines whether the tensor is a symmetric tensor
    # @param symmetricTensorSymbols a list of strings representing the symbols of the user-defined symmetric tensors
    #
    def __init__(self, symbol, sym, partials=None, sign="+", isSymmetric=False, symmetricTensorSymbols=None):
        self.symbol = symbol
        if type(sym) is SymmetryProperties:
            self.symmetry = sym
        else:
            raise TypeError()
        self.isSymmetric = isSymmetric
        if partials is None:
            self.partials = list()
        else:
            self.partials = partials
        self.sign = sign
        #if self.symbol == "h":
        #    self.isSymmetric = True
        #    self.symmetry.setSymmetric(True)
        if symmetricTensorSymbols is None:
            self.symTenSym = list()
        else:
            self.symTenSym = symmetricTensorSymbols
        if self.symbol in self.symTenSym:
            self.isSymmetric = True
            self.symmetry.setSymmetric(True)
        # TODO: can this use the defined function instead of duplicate code?
        self.numTSums = 0 # number of sums within the tensors indices
        if len(sym.getIndices()) > 1:
            for i in range(len(sym.getIndices())):
                for j in range(i+1, len(sym.getIndices())):
                    if sym.getIndices()[i].sumsWith(sym.getIndices()[j]):
                        sym.getIndices()[i].changeSum(True)
                        sym.getIndices()[j].changeSum(True)
                        self.numTSums += 1
        # TODO: can this use the defined function instead of duplicate code?
        self.numPTSums = 0 # numbers of sums between the partials indices and the tensors indices
        if len(sym.getIndices()) > 0 and len(partials) > 0:
            for p in range(len(partials)):
                for i in range(len(sym.getIndices())):
                    if partials[p].getIndex().sumsWith(sym.getIndices()[i]):
                        #if not sym.getUpInds()[i].hasSum():
                        sym.getIndices()[i].changeSum(True)
                        partials[p].getIndex().changeSum(True)
                        self.numPTSums += 1
                        #else:
                            #raise IndexException("Too many instances of the index " + repr(sym.getUpInds()[i].getSymbol()))
                #for d in range(len(sym.getDownInds())):
                 #   if partials[p].getIndex().sumsWith(sym.getDownInds()[d]):
                        #if not sym.getDownInds()[d].hasSum():
                  #      sym.getDownInds()[d].changeSum(True)
                   #     partials[p].getIndex().changeSum(True)
                    #    self.numPTSums += 1
                            #if (not sym.getDownInds()[d].isUp()) and (isSymmetric):
                            #    sym.getDownInds()[d].changeHeight()
                            #    partials[p].getIndex().changeHeight()
                            #elif (not sym.getDownInds()[d].isUp()):
                            #    if len(sym.getUpInds()) > d and sym.getUpInds()[d].getIndex() == Index("\\ "):
                            #        ind = copy.deepcopy(sym.getDownInds()[d])
                            #        ind.changeHeight()
                            #        sym.getUpInds()[d] = ind
                            #        sym.getDownInds()[d] = Index("\\%", 0)
                            #        partials[p].getIndex().changeHeight()
                        # else:
                        #    raise IndexException("Too many instances of the index " + repr(sym.getDownInds()[d].getSymbol()))
        self.rank = (len(sym.getIndices())-2*self.numTSums-2*self.numPTSums)
        self.numPartials = len(self.partials)
        self.ownerHash = self.symbol+str(self.numTSums)+str(self.numPTSums)
        self.setSums()

    def reinitOwnerHash(self):
        self.ownerHash = self.symbol+str(self.numTSums)+str(self.numPTSums)

    def getOwnerHash(self):
        self.reinitOwnerHash()
        return self.ownerHash

    def setTSums(self):
        self.numTSums = 0
        if len(self.symmetry.getIndices()) > 1:
            for i in range(len(self.symmetry.getIndices())):
                for j in range(i+1, len(self.symmetry.getIndices())):
                    if self.symmetry.getIndices()[i].sumsWith(self.symmetry.getIndices()[j]):
                        self.symmetry.getIndices()[i].changeSum(True)
                        self.symmetry.getIndices()[j].changeSum(True)
                        self.numTSums += 1

    # TODO: what about sums within the partials (square) - should these have their own part in the hash?
    def setPTSums(self):
        self.numPTSums = 0
        if len(self.symmetry.getIndices()) > 0 and len(self.partials) > 0:
            for p in range(len(self.partials)):
                for i in range(len(self.symmetry.getIndices())):
                    if self.partials[p].getIndex().sumsWith(self.symmetry.getIndices()[i]):
                        #if not self.symmetry.getIndices()[i].hasSum():
                        self.symmetry.getIndices()[i].changeSum(True)
                        self.partials[p].getIndex().changeSum(True)
                        self.numPTSums += 1
                        #else:
                        #    print(self)
                        #    raise IndexException("Too many instances of the index " + repr(self.symmetry.getDownInds()[d].getSymbol()))

    def setSums(self):
        tHash = self.getOwnerHash()
        for ind in self.getIndices():
            ind.setOwner("t"+tHash)
        for p in self.getPartials():
            p.getIndex().setOwner("tp"+tHash)
        indices = self.getSeparateIndices()
        for itt in range(len(indices)):
            indices[itt].setSum(False)
            indices[itt].setSumType(Gemma())
        for i in range(len(indices)):
            possSum = copy.deepcopy(indices[i])
            for j in range(i+1, len(indices)):
                if indices[j].sumsWith(possSum):
                    indices[i].setSum(True)
                    indices[j].setSum(True)
                    sumType = Gemma()
                    sumType.add(indices[i].getOwner())
                    sumType.add(indices[j].getOwner())
                    indices[i].setSumType(copy.deepcopy(sumType))
                    indices[j].setSumType(copy.deepcopy(sumType))

    ## redefines the Symmetry
    # @param new symmetry a boolean value
    def changeSymmetry(self, newSymmetry):
        self.isSymmetric = newSymmetry

    ## returns whether symmetric = true or false
    # @return whether symmmetric = true or false
    def getIsSymmetric(self):
        return self.isSymmetric

    def getSym(self):
        return self.symmetry

    def getSymbol(self):
        return self.symbol

    def addPartial(self, p):
        p.getIndex().setSum(False)
        p.getIndex().setSumType(Gemma())
        self.partials.append(p)
        self.setPTSums()
        self.setSums()
        # TODO: should the owner hash be reinitialized here? and/ or should i move all sum setting and hash reinitializing to the funciton that uses the hash?

    def getIndices(self):
        return self.symmetry.getIndices()

    def getAllIndices(self):
        indsList = list()
        for p in self.getPartials():
            indsList.append(p.getIndex())
        indsList.append(self.getIndices())
        return indsList

    def getSeparateIndices(self):
        indsList = list()
        for p in self.getPartials():
            indsList.append(p.getIndex())
        indsList += (self.getIndices())
        return indsList

    def getPartials(self):
        return self.partials

    def getNumPartials(self):
        return self.numPartials

    def getRank(self):
        return self.rank

    def getNumTSums(self):
        return self.numTSums

    def getNumPTSums(self):
        return self.numPTSums

    def getSign(self):
        return self.sign

    def changeSign(self, newSign):
        self.sign = newSign

    def addPartials(self, partial):
        partial.getIndex().setSum(False)
        partial.getIndex().setSumType(Gemma())
        self.partials.append(partial)
        self.setPTSums()
        self.setSums()

    def addPartialList(self, lp):
        for p in lp:
            p.getIndex().setSum(False)
            p.getIndex().setSumType(Gemma())
        self.partials += lp
        self.setPTSums()
        self.setSums()

    def getEqualIndices(self, index):
        pointer = list()
        for ind in self.getIndices():
            if ind.basicEquals(index):
                pointer.append(ind)
        for p in self.getPartials():
            if p.getIndex().basicEquals(index):
                pointer.append(p.getIndex())
        return pointer

    def changeIndicesTenH(self, fromTen, toTen):
        print("fromTen: ", fromTen)
        print("toTen: ", toTen)
        fromTenList = fromTen.getFullIndices()
        toTenList = toTen.getFullIndices()
        self.changeIndicesListH(fromTenList, toTenList)

    def changeIndicesListH(self, fromList, toList):
        print("fromList: ", fromList)
        print("toList: ", toList)
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
        self.setSums()

    def getEqualIndicesH(self, index):
        pointer = list()
        for ind in self.getIndices():
            if ind.basicEqualsH(index):
                pointer.append(ind)
        for p in self.getPartials():
            if p.getIndex().basicEqualsH(index):
                pointer.append(p.getIndex())
        return pointer
    ## assume summation patterns have been reinitialized
    ## patternEq checks if
    #
    def patternEqNotAllPs(self, other):
        print("self: ", self)
        print("other: ", other)
        if not (self.getSymbol() == other.getSymbol()):
            return False
        if len(self.getPartials()) < len(other.getPartials()):
            return False
        selfNoPs = copy.deepcopy(self)
        selfNoPs.setPartials([])
        otherNoPs = copy.deepcopy(other)
        otherNoPs.setPartials([])
        selfNoPs.setSums()
        otherNoPs.setSums()
        if not (selfNoPs.getSym().basicPatternEqH(otherNoPs.getSym())):
            return False
        #if self.getNumTSums() != other.getNumTSums():
        #    return False
        if self.getNumPTSums() < other.getNumPTSums():
            return False
        if (len(self.getPartials())-self.getNumPTSums()) < (len(other.getPartials())-other.getNumPTSums()):  # num free partial indices
            return False
        return True

    def patternEq(self, other):
        if not self.getSymbol() == other.getSymbol():
            return False
        if not self.getIsSymmetric() == other.getIsSymmetric():
            return False
        if not self.testPatternSETListEquality(self.getPartials(), other.getPartials()):
            return False
        if not (self.getSym().patternEq(other.getSym())):
            return False
        return True

    def patternEqH(self, other):
        if not self.getSymbol() == other.getSymbol():
            return False
        if not self.getIsSymmetric() == other.getIsSymmetric():
            return False
        if not self.testPatternSETListEqualityH(self.getPartials(), other.getPartials()):
            return False
        if not (self.getSym().patternEqH(other.getSym())):
            return False
        return True

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

    # TODO: move all these testSETListEquality methods to their own file
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

    def setPartials(self, new):
        self.partials = new
        self.setPTSums()

    def getOrderedIndices(self):
        return self.symmetry.getOrderedIndices()

    def getFullIndices(self):
        indicesList = list()
        for partial in self.getPartials():
            indicesList.append(partial.getIndex())
        indicesList.sort()
        #print("before tensors: ", indicesList)
        for index in self.getOrderedIndices():
            indicesList.append(index)
        #print(indicesList)
        return indicesList

    def __eq__(self, other):
        if not self.getSymbol() == other.getSymbol():
            return False
        if not self.getSym() == other.getSym():
            return False
        if not self.testSETListEquality(self.getPartials(), other.getPartials()):
            return False
        return True

    def eq2(self, other):
        #if sexlf.getSign() != other.getSign():
        #    return False
        if not self.getRank() == other.getRank():
            return False
        if self.getSymbol() != other.getSymbol():
            return False
        if not self.getNumTSums() == other.getNumTSums():
            return False
        if not self.getNumPTSums() == other.getNumPTSums():
            return False
        if not((self.getIsSymmetric() and other.getIsSymmetric()) or ((not self.getIsSymmetric()) and not(other.getIsSymmetric()))):
            return False
        thisNonSumPartials = list()
        for partial in self.getPartials():
            if not partial.getIndex().hasSum():
                thisNonSumPartials.append(partial)
        otherNonSumPartials = list()
        for partial in other.getPartials():
            if not partial.getIndex().hasSum():
                otherNonSumPartials.append(partial)
        if not self.testSETListEquality(thisNonSumPartials, otherNonSumPartials):
            return False
        if not self.getSym() == other.getSym():
            return False
        return True

    ## tests for equality assuming only fully symmetric or not, NOT testing sign
    def complicatedEqualityTest(self, other):
        if self.getSymbol() != other.getSymbol():
            return False
        elif len(self.partials) != len(other.getPartials()):
            return False
        elif (self.numTSums != other.getNumTSums()) or (self.numPTSums != other.getNumPTSums()):
            return False
        else:
            selfPIndices = set()
            otherPIndices = set()
            for p in self.partials:
                if not p.getIndex().hasSum():
                    selfPIndices.add(p.getIndex())
            for p in other.getPartials():
                if not p.getIndex().hasSum():
                    otherPIndices.add(p.getIndex())

            if selfPIndices != otherPIndices:
                return False

            selfTIndices = list()
            otherTIndices = list()
            for i in self.symmetry.getIndices():
                if not i.hasSum():
                    selfTIndices.append(i)
            for i in other.getIndices():
                if not i.hasSum():
                    otherTIndices.append(i)
            if not (self.getIsSymmetric() and other.getIsSymmetric()):
                if selfTIndices != otherTIndices:
                    return False
            else:
                if set(selfTIndices) != set(otherTIndices):
                    return False
            return True

    # this compares the order of the tensors 
    def __lt__(self, other):
        return self.getNumPartials() < other.getNumPartials()

    def __repr__(self):
        strx = ""
        strx += displayPartialList(self.partials)
        # for p in self.partials:
        #     strx = strx + repr(p)
        strx = strx + self.symbol
        strx = strx + repr(self.symmetry)
        return strx



