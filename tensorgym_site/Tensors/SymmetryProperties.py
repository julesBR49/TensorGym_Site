from Tensors.Index import Index
from Tensors.IndexException import IndexException
import copy
class SymmetryProperties:

    def __init__(self, strx=""):
        self.indices = list()
        self.isSymmetric = False
        if not strx == "":
            strx = ' '.join(strx.split(" "))
            strx = strx.replace("{","")
            strx = strx.replace("}","")
            strx = strx.replace("(","")
            strx = strx.replace(")","")
            strx = strx.replace("[","")
            strx = strx.replace("]","")
            if strx.startswith("_"):
                strx = strx.replace("_", "")
                inds = strx.split("^")
                if len(inds) > 1:
                    up = inds[1]
                else: up = ""
                down = inds[0]
            elif strx.startswith("^"):
                strx = strx.replace("^","")
                inds = strx.split("_")
                if len(inds) > 1:
                    down = inds[1]
                else: down = ""
                up = inds[0]
            else: raise IndexException("must be up or down")
            while "\\ " in up:  # deal with case of space command - rest of indices might not be commands so dealt with separately
                up = up.replace("\\ ", "\\%")
            up = ''.join(up.split())
            if "\\" in up:
                upInds = up.split("\\")
                for el in upInds:
                    if el != "":
                        self.indices.append(Index("\\" + el, 1))
            else:
                upInds = list()
                for i in range(len(up)):
                    upInds.append(up[i])
                for el in upInds:
                    if el != "":
                        self.indices.append(Index(el, 1))
            if "\\ " in down:
                down = down.replace("\\ ", "\\%")
            down = ''.join(down.split())
            if "\\" in down:
                downInds = down.split("\\")
                for el in downInds:
                    if el != "":
                        self.indices.append(Index("\\" + el, 0))
            else:
                downInds = list()
                for i in range(len(down)):
                    downInds.append(down[i])
                for el in downInds:
                    if el != "":
                        self.indices.append(Index(el, 0))

    def getIndices(self):
        return self.indices

    def getIsSymmetric(self):
        return self.isSymmetric

    def setSymmetric(self, bool):
        self.isSymmetric = bool

    def changeIndex(self, oldInd, newInd):
        for i in range(len(self.indices)):
            if self.indices[i].basicEqualsH(oldInd):
                self.indices[i] = newInd

    def getUpInds(self):
        upInds = list()
        for index in self.getIndices():
            if index.isUp():
                upInds.append(index)
        return upInds

    def getDownInds(self):
        downInds = list()
        for index in self.getIndices():
            if index.isDown():
                downInds.append(index)
        return downInds

    def getOrderedIndices(self):
        retList = list()
        if self.isSymmetric:
            sumList = list()
            upList = list()
            downList = list()
            for ind in self.getIndices():
                if ind.hasSum():
                    sumList.append(ind)
                elif ind.isUp():
                    upList.append(ind)
                elif ind.isDown():
                    downList.append(ind)
            sumList.sort()
            retList += sumList + upList + downList
        else:
            up = self.getUpInds()
            down = self.getDownInds()
            u = len(up)
            d = len(down)
            leticia = max([u, d])
            if leticia < len(self.getNonEmptyIndices()):
                retList += self.getNonEmptyIndices()
            else:
                for i in range(max([u, d])):
                    if (i >= len(up)) or (up[i].getIndex() == "\\ " and i < len(down)):
                        retList.append(down[i])
                    elif (i >= len(down)) or (down[i].getIndex() == "\\ " and i < len(up)):
                        retList.append(up[i])
        return retList

    def patternEq(self, other):
        if self.isSymmetric:
            return self.testPatternSETListEquality(self.getIndices(), other.getIndices())
        if self.getIsSymmetric() != other.getIsSymmetric():
            return False
        selfUp = self.getUpInds()
        selfDown = self.getDownInds()
        otherUp = other.getUpInds()
        otherDown = other.getDownInds()
        while len(selfUp) < len(selfDown):
            selfUp.append(Index("\\ ", 1))
        while len(otherUp) < len(otherDown):
            otherUp.append(Index("\\ ", 1))
        while len(selfDown) < len(selfUp):
            selfDown.append(Index("\\ ", 0))
        while len(otherDown) < len(otherUp):
            otherDown.append(Index("\\ ", 0))
        for i in range(len(selfUp)):
            if not selfUp[i].patternEq(otherUp[i]):
                return False
        for j in range(len(selfDown)):
            if not selfDown[j].patternEq(otherDown[j]):
                return False
        return True

    def getNonEmptyIndices(self):
        nE = list()
        for el in self.getIndices():
            if not el.getIndex() == "\\ ":
                nE.append(el)
        return nE

    def basicPatternEqH(self, other):
        if self.getIsSymmetric() != other.getIsSymmetric():
            return False
        if len(self.getNonEmptyIndices()) != len(other.getNonEmptyIndices()):
            return False
        return True

    def patternEqH(self, other):
        if self.getIsSymmetric() != other.getIsSymmetric():
            return False
        if self.isSymmetric:
            return self.testPatternSETListEqualityH(self.getIndices(), other.getIndices())
        selfUp = self.getUpInds()
        selfDown = self.getDownInds()
        otherUp = other.getUpInds()
        otherDown = other.getDownInds()
        while len(selfUp) < len(selfDown):
            selfUp.append(Index("\\ ", 1))
        while len(otherUp) < len(otherDown):
            otherUp.append(Index("\\ ", 1))
        while len(selfDown) < len(selfUp):
            selfDown.append(Index("\\ ", 0))
        while len(otherDown) < len(otherUp):
            otherDown.append(Index("\\ ", 0))
        selfBoth = list()
        for i in range(len(selfUp)):
            if selfUp[i] == (Index("\\ ", 1)):
                selfBoth.append(selfDown[i])
            else:
                selfBoth.append(selfUp[i])
        otherBoth = list()
        for j in range(len(otherUp)):
            if otherUp[j] == (Index("\\ ", 1)):
                otherBoth.append(otherDown[j])
            else:
                otherBoth.append(otherUp[j])
        if not len(selfBoth) == len(otherBoth):
            return False
        for b in range(len(selfBoth)):
            if not(selfBoth[b].patternEqH(otherBoth[b])):
                return False
        return True

    def __eq__(self, other):
        if self.isSymmetric:
            return self.testSETListEquality(self.getIndices(), other.getIndices())
        selfUp = self.getUpInds()
        selfDown = self.getDownInds()
        otherUp = other.getUpInds()
        otherDown = other.getDownInds()
        while len(selfUp) < len(selfDown):
            selfUp.append(Index("\\ ", 1))
        while len(otherUp) < len(otherDown):
            otherUp.append(Index("\\ ", 1))
        while len(selfDown) < len(selfUp):
            selfDown.append(Index("\\ ", 0))
        while len(otherDown) < len(otherUp):
            otherDown.append(Index("\\ ", 0))
        if selfUp == otherUp and selfDown == otherDown:
            return True
        else:
            return False

    def __repr__(self):
        stringRepr = ""
        downInd = self.getDownInds()
        upInd = self.getUpInds()
        if len(downInd) > 0:
            stringRepr = stringRepr + "_{"
            for i in range(len(downInd)):
                if i < len(downInd)-1:
                    stringRepr = stringRepr + downInd[i].getIndex() + " "
                else:
                    stringRepr = stringRepr + downInd[i].getIndex()
            stringRepr = stringRepr + "}"
        if len(upInd) > 0:
            stringRepr = stringRepr + "^{"
            for i in range(len(upInd)):
                if i < len(upInd)-1:
                    stringRepr = stringRepr + upInd[i].getIndex() + " "
                else:
                    stringRepr = stringRepr + upInd[i].getIndex()
            stringRepr = stringRepr + "}"
        if (len(upInd) == 0) and (len(downInd) == 0):
            stringRepr += "^{}"
        return stringRepr

    #def testSETListEquality(self, l1, l2):
    #    if not len(l1) == len(l2):
    #        return False
    #    for el1 in l1:
    #        if el1 not in l2:
    #            return False
    #    for el2 in l2:
    #        if el2 not in l1:
    #            return False
    #    return True

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
