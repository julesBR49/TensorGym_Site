from Tensors.EquationNode import EquationNode
from Tensors.Sign import Sign
from Tensors.MultGroup import MultGroup
from Tensors.TensorCoefficients import TensorCoefficients
from Tensors.Coefficient import Coefficient
from Tensors.SymbolCo import SymbolCo
from Tensors.Fraction import Fraction
from Tensors.Summation import Summation
import copy
class EquationTree:
    def __init__(self, root=None):
        if root is None:
            self.root = EquationNode()
        else:
            self.root = root
        self.oneCommands = ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon", "\\zeta", "\\eta", "\\theta", "\\iota", "\\kappa", "\\lambda", "\\mu", "\\nu", "\\ksi" "\\xi", "\\omikron", "\\omicron", "\\pi", "\\rho", "\\sigma", "\\tau", "\\upsilon", "\\phi", "\\chi", "\\psi", "\\omega", "\\sqrt"]
        self.eqIndicator = False

    def getRoot(self):
        return self.root

    def setRoot(self, newRoot):
        self.root = newRoot

    def setEqIndicator(self, ind):
        self.eqIndicator = ind

    def inorder(self, node, tempList):
        if node is not None:
            self.inorder(node.getLeft(), tempList)
            tempList.append(node.getElement())
            self.inorder(node.getRight(), tempList)

    def traverse(self):
        tempList = list()
        self.inorder(self.root, tempList)
        return tempList

    def foil(self, node):
        if node is None:
            return
        if (node.getLeft() is None) and (node.getRight() is None):
            return node
        else:
            right = self.foil(node.getRight())
            left = self.foil(node.getLeft())
            if not node.isAlgOpp():
                raise TypeError("Nodal element issue")
            if node.getElement() == Sign("+"):
                newEl = right.getElement()+left.getElement()
                node.setElement(newEl)
            elif node.getElement() == Sign("-"):
                newEl = right.getElement()-left.getElement()
                node.setElement(newEl)
            elif node.getElement() == Sign("*"):
                newEl = copy.deepcopy(right.getElement())*copy.deepcopy(left.getElement())
                node.setElement(newEl)
            node.setLeft(None)
            node.setRight(None)
            return node

    def noPfoil(self, node):
        if (node.getLeft() is None) and (node.getRight() is None):
            return node
        else:
            right = self.noPfoil(node.getRight())
            left = self.noPfoil(node.getLeft())
            if not node.isAlgOpp():
                raise TypeError("Nodal element issue")
            if node.getRight().isLeaf() and node.getLeft().isLeaf():
                set = False
                if node.getElement() == Sign("+"):
                    if not(right.getElement().hasPartials()) and not(left.getElement().hasPartials()):
                        newEl = right.getElement().noPAdd(left.getElement())
                        node.setElement(newEl)
                        set = True
                elif node.getElement() == Sign("-"):
                    if not(right.getElement().hasPartials()) and not(left.getElement().hasPartials()):
                        newEl = right.getElement().noPSub(left.getElement())
                        node.setElement(newEl)
                        set = True
                elif node.getElement() == Sign("*"):
                    if not(right.getElement().hasPartials()) and not(left.getElement().hasPartials()):
                        newEl = right.getElement().noPMul(left.getElement())
                        node.setElement(newEl)
                        set = True
                if set:
                    node.setLeft(None)
                    node.setRight(None)
            elif node.getElement() == Sign("*"):
                if node.getRight().isLeaf() and node.getLeft().getElement == Sign("*"):
                    if not node.getRight().getElement().hasPartials():
                        lr = node.getLeft().getRight()
                        ll = node.getLeft().getLeft()
                        if lr.isSum() and (not lr.getElement().hasPartials()):
                            newEl = right.getElement().noPMul(lr.getElement())
                            right.setElement(newEl)
                            node.setLeft(ll)
                        elif ll.isSum() and (not ll.getElement().hasPartials()):
                            newEl = right.getElement().noPMul(ll.getElement())
                            right.setElement(newEl)
                            node.setLeft(lr)
                elif node.getLeft().isLeaf() and node.getRight().getElement() == Sign("*"):
                    if not node.getLeft().getElement().hasPartials():
                        rr = node.getRight().getRight()
                        rl = node.getRight().getLeft()
                        if rr.isSum() and (not rr.getElement().hasPartials()):
                            newEl = left.getElement().noPMul(rr.getElement())
                            left.setElement(newEl)
                            node.setRight(rl)
                        elif rl.isSum() and (not rl.getElement().hasPartials()):
                            newEl = left.getElement().noPMul(rl.getElement())
                            left.setElement(newEl)
                            node.setRight(rr)
                elif node.getLeft().getElement() == Sign("*") and node.getRight().getElement() == Sign("*"):
                    mul = True
                    if left.getLeft().isSum() and not(left.getLeft().getElement().hasPartials()):
                        lOpen = left.getLeft()
                        lPart = left.getRight()
                    elif left.getRight().isSum() and not(left.getRight().getElement().hasPartials()):
                        lOpen = left.getRight()
                        lPart = left.getLeft()
                    else:
                        mul = False
                        lOpen = None
                        lPart = left
                    if right.getLeft().isSums() and not(right.getLeft().getElement().hasPartials()):
                        rOpen = right.getLeft()
                        rPart = right.getRight()
                    elif right.getRight().isSums() and not(right.getRight().getElement().hasPartials()):
                        rOpen = right.getRight()
                        rPart = right.getLeft()
                    else:
                        mul = False
                        rOpen = None
                        rPart = right
                    if mul:
                        node.setLeft(EquationNode(lOpen.noPMul(rOpen)))
                        node.getRight().setRight(rPart)
                        node.getRight().setLeft(lPart)
        return node

    def distributePs(self, node):
        if node is None:
            return
        if node.getLeft() is None and node.getRight() is None:
            node.getElement().distributePartials()
            return
        else:
            self.distributePs(node.getLeft())
            self.distributePs(node.getRight())
            if node.getElement() == Sign("*") and (node.getLeft() is not None and node.getLeft().isLeaf()) and (node.getRight() is not None and node.getRight().isLeaf()):
                if len(node.getLeft().getElement().getSums()) == 1:
                    if node.getLeft().getElement().getSums()[0].isOnlyPartials():
                        node.getRight().getElement().addPartials(node.getLeft().getElement().getSums()[0].getPartials())
                        node.getLeft().getElement().getSums()[0].setPartials([])
                        if node.getLeft().getElement().getSums()[0] == MultGroup("-"):
                            node.getLeft().getElement().getSums()[0].swapSign()
                            node.getRight().getElement().swapSign()
                        if node.getLeft().getElement().getSums()[0] == MultGroup("+"):
                            node.setElement(node.getRight().getElement())
                            node.setLeft(None)
                            node.setRight(None)
                elif len(node.getRight().getElement().getSums()) == 1:
                    if node.getRight().getElement().getSums()[0].isOnlyPartials():
                        node.getLeft().getElement().addPartials(node.getRight().getElement().getSums()[0].getPartials())
                        node.getRight().getElement().getSums()[0].setPartials([])
                        if node.getRight().getElement().getSums()[0] == MultGroup("-"):
                            node.getRight().getElement().getSums()[0].swapSign()
                            node.getLeft().getElement().swapSign()
                        if node.getRight().getElement().getSums()[0] == MultGroup("+"):
                            node.setElement(node.getLeft().getElement())
                            node.setLeft(None)
                            node.setRight(None)

    def replaceOnlyTensor(self, summ, jfk, lbj, typae):
        i = 0
        while i < len(summ):
            pres = summ[i]
            if typae == 'ten':
                toAssassinate = pres.findTensor(jfk)
            elif typae == 'var':
                toAssassinate = pres.findVariation(jfk)
            else:
                raise TypeError("can only assassinate variations or tensors")
            if toAssassinate is not None:
                if typae == 'ten':
                    pres.removeTensorRef(toAssassinate)
                else:
                    pres.removeVarRef(toAssassinate)
                lbjNEW = copy.deepcopy(lbj)
                jfkNEW = copy.deepcopy(jfk)
                kittens = copy.deepcopy(toAssassinate.getPartials())
                cats = list()
                k = 0
                while k < len(kittens):
                    partial = kittens[k]
                    inJFK = False
                    copyPars = copy.deepcopy(jfkNEW.getPartials())
                    j = 0
                    while (j < len(copyPars)) and (not inJFK):
                    #while j < len(jfkNEW.getPartials()) and not inJFK:
                        jPart = copyPars[j]
                        if jPart.patternEqH(partial):
                            kittens.remove(partial)
                            copyPars.remove(jPart)
                            cats.append(jPart)
                            inJFK = True
                        else:
                            j += 1
                    if not inJFK:
                        k += 1
                #jfkNEW.addPartialList(kittens)
                #lbjNEW.addPartialList(kittens)
                toAssassinate.setPartials(cats)
                lbjNEW.changeIndicesTenH(jfkNEW, toAssassinate)
                lbjNEW.addPartialList(kittens)
                if typae == 'ten':
                    pres.addTensors(lbjNEW)
                else:
                    pres.addVariations(lbjNEW)
            else:
                i += 1

    def replaceTensor(self, node, jfk, lbj, neg, typae):  # jfk is tensor, lbj is summation object
        i = len(node.getElement().getSums())-1
        done = False
        while not done and i >= 0:
            pres = node.getElement().getSums()[i]
            if typae == 'ten':
                toAssassinate = pres.findTensor(jfk)  # uses patternEq to find
            elif typae == 'var':
                toAssassinate = pres.findVariation(jfk)
            else:
                raise TypeError("can only assassinate variations or tensors")
            if toAssassinate is not None:  # fugitive has been found
                done = True
                node.getElement().remRef(pres)  # remove method removes first instance
                if typae == "ten":
                    pres.removeTensorRef(toAssassinate)  # PRES IS A MULTGROUP
                else:
                    pres.removeVarRef(toAssassinate)
                if neg:
                    pres.swapSign()
                toAssassinate.setSums()
                toIndsTen = copy.deepcopy(toAssassinate)
                toIndsTen.setPartials([])  # remove all partials
                fromIndsTen = copy.deepcopy(jfk)
                partials = copy.deepcopy(toAssassinate.getPartials())
                for partial in jfk.getPartials():
                    rem = False
                    for oPartial in partials:
                        if (not rem) and (oPartial.patternEqH(partial)):
                            partials.remove(oPartial)  # leave only non-shared partials: this will later be added to new Summation object (lbj)
                            toIndsTen.addPartial(oPartial)  # add back shared partials
                toMult = MultGroup("+")
                toMult.addThing(toIndsTen)
                fromMult = MultGroup("+")
                fromMult.addThing(fromIndsTen)
                lbjNEW = copy.deepcopy(lbj)
                lbjNEW.changeIndicesMultHNOSUMS(fromMult, toMult) #!!!!!!!!!!!!
                lbjNEW.setPartials(partials)  # SUMMATION OBJECT
                newPres = EquationNode(lbjNEW)
                if pres.getSign() == "-" and node.getElement() != Summation():
                    signage = Sign("-")
                    pres.swapSign()
                else:
                    signage = Sign("+")
                if not(pres == MultGroup("+")):  # if it's not empty
                    jackie = EquationNode(Summation([pres]))
                    self.replaceTensor(jackie, copy.deepcopy(jfk), copy.deepcopy(lbj), neg, typae)
                    signNode = EquationNode(Sign("*"))
                    signNode.setRight(jackie)
                    signNode.setLeft(newPres)  # multiply Jackie and the replacement
                    victim = signNode.getLeft()
                else:
                    signNode = newPres
                    victim = signNode
                if node.getElement() != Summation():  # if it's not empty
                    vietnam = EquationNode(node.getElement())
                    node.setElement(signage)
                    node.setLeft(signNode)
                    node.setRight(vietnam)  # add together the full replacement and the leftovers
                    self.replaceTensor(node.getRight(), jfk, lbj, neg, typae)  # change pointer to node with element we haven't looked at yet
                else:
                    #if signage == Sign("-"):
                    #    victim.getElement().getSums()[0].swapSign()
                    #if signage == Sign("-"):

                    node.setElement(signNode.getElement())
                    node.setRight(signNode.getRight())
                    node.setLeft(signNode.getLeft())
                    #self.replaceTensor(victim, jfk, lbj, neg, typae)
            else:
                i += -1

    def replaceSum(self, node, ogSumsInit, newSumsInit):
        if not node.isSum():
            return
        sums = node.getElement().getSums()
        ogSums = ogSumsInit.getSums()  # list of MultGroup objects
        newSums = newSumsInit.getSums()  # list of MultGroup objects
        if len(ogSums) == 1:
            if ogSums[0].isOnlyTensor():
                if len(newSums) == 1 and newSums[0].isOnlyTensor():
                    self.replaceOnlyTensor(sums, ogSums[0].getTensors()[0], newSums[0].getTensors()[0], 'ten')
                else:
                    if ogSums[0].getSign() == "-":
                        neg = True
                    else:
                        neg = False
                    self.replaceTensor(node, ogSums[0].getTensors()[0], newSumsInit, neg, 'ten')
                    return
            elif ogSums[0].isOnlyVar():
                if len(newSums) == 1 and newSums[0].isOnlyVar():
                    self.replaceOnlyTensor(sums, ogSums[0].getVariations()[0], newSums[0].getVariations()[0], 'var')
                else:
                    if ogSums[0].getSign() == "-":
                        neg = True
                    else:
                        neg = False
                    self.replaceTensor(node, ogSums[0].getVariations()[0], newSumsInit, neg, 'var')
                    return
            elif len(newSums) == 1:
                ogSum = ogSums[0]
                newSum = newSums[0]
                i = 0
                while i < len(sums):
                    summy = sums[i]  # MultGroup object
                    if summy.patternEqIncludesH(ogSum):
                        newSummy = copy.deepcopy(newSum)  # MultGroup object
                        newSummy.changeIndicesMultH(ogSum, summy)
                        newSummy.addNumCo(summy.getNumCo()/ogSum.getNumCo())
                        newSummy.addSymCo(summy.getSymCo()/ogSum.getSymCo())
                        if not(summy.getTensorCo() == ogSum.getTensorCo()):
                            newSummy.setTensorCo(summy.getTensorCo()*newSummy.getTensorCo())
                        if not (summy.getSign() == ogSum.getSign()):
                            newSummy.swapSign()
                        sums[i] = newSummy
                        #node.getElement().replaceTerm(summy, newSummy)
                    i += 1  # whether or not anything was replaced, we need to move on
            elif len(newSums) != 1:
                ogSum = ogSums[0]
                i = 0
                while i < len(sums):
                    summy = sums[i]
                    posVersion = copy.deepcopy(ogSum)
                    posVersion.swapSign()  # create a positive version to test against
                    if (summy.patternEqH(ogSum)) or (summy.patternEqH(posVersion)):
                        newAdd = copy.deepcopy(newSumsInit)
                        if summy.getSign() != ogSum.getSign():  # if they have opposite signs, factor out a negative, then multiply it through new
                            for newSum in newAdd.getSums():
                                newSum.swapSign()
                        newAdd.changeIndicesMultH(ogSum, summy)
                        node.getElement().removeTerm(summy)
                        for newSum in newAdd.getSums():
                            sums.insert(i, newSum)
                            i += 1
                    elif summy.patternEqIncludesH(ogSum):
                        newAdd = copy.deepcopy(newSumsInit)
                        newAdd.changeIndicesMultH(ogSum, summy)
                        node.getElement().removeTerm(summy)
                        ## deal with what is left of multgroup
                        outerMult = MultGroup("+")
                        if summy.getSign() != ogSum.getSign():
                            outerMult.swapSign()
                        outerMult.addNumCo(summy.getNumCo()/ogSum.getNumCo())
                        outerMult.addSymbolCo(summy.getSymCo()/ogSum.getSymCo())
                        if not(summy.getTensorCos() == ogSum.getTensorCos()):
                            outerMult.setTensorCos(summy.getTensorCo())
                        ## create the reconstructed tree
                        #if outerMult.getSign() == "-":
                        #    outerMult.swapSign()
                        newNode = EquationNode(Sign("*"))
                        newNode.setRight(EquationNode(Summation([outerMult])))
                        newNode.setLeft(EquationNode(Summation(newAdd.getSums())))
                        node.setLeft(EquationNode(node.getElement()))
                        node.setRight(newNode)
                        node.setElement(Sign("+"))
                        node = node.getLeft()
                    else:
                        i += 1

        else:  # neither length is one
            testSums = copy.deepcopy(sums)
            testSumsPos = copy.deepcopy(sums)
            newAdd = copy.deepcopy(newSums)
            foundSums = list()
            for sum in testSumsPos:
                sum.swapSign()
            allIn = True
            for ogSum in ogSums:
                rem = False
                for summy in testSums:
                    if ogSum.patternEqH(summy) and (not rem):
                        testSums.remove(summy)
                        foundSums.append(summy)
                        rem = True
                if not rem:
                    allIn = False
            allInPos = False
            if not allIn:
                foundSums.clear()
                allInPos = True
                for ogSum in ogSums:
                    rem = False
                    for summy in testSumsPos:
                        if ogSum.patternEqH(summy) and (not rem):
                            testSumsPos.remove(summy)
                            foundSums.append(summy)
                            rem = True
                    if not rem:
                        allInPos = False
            if allInPos:
                for summy in newAdd:
                    summy.swapSign()
                allIn = True
            if allIn:
                old = ogSumsInit.getSortedIndicesList()
                new = Summation(foundSums).getSortedIndicesList()
                for newSum in newAdd:
                    newSum.changeIndicesListH(old, new)
                sums = node.getElement().getSums()
                i = 0
                for foundSum in foundSums:
                    rem = False
                    for oldSum in sums:
                        if (oldSum == foundSum) and (not rem):
                            i = sums.index(oldSum)
                            sums.remove(oldSum)
                            rem = True
                for newSum in newAdd:
                    sums.insert(i, newSum)
                    i += 1

    def replace(self, node, ogSum, newSum):
        if node is not None:
            self.replace(node.getRight(), ogSum, newSum)
            self.replace(node.getLeft(), ogSum, newSum)
            if node.isSum():
                self.replaceSum(node, ogSum, newSum)

    def replaceInds(self, node, oldList, newList):
        if node is not None:
            self.replaceInds(node.getRight(), oldList, newList)
            self.replaceInds(node.getLeft(), oldList, newList)
            if node.isSum():
                node.getElement().simplestChangeIndicesList(oldList, newList)

    def gcf(self, node):
        if not node.isSum():
            return
        sums = node.getElement().getSums()
        if len(sums) == 1 or len(sums) == 0:
            return
        for summy in sums:
            summy.factorNumFromTensorCo()
            summy.factorSymFromTensorCo()
        otherTerm = MultGroup("+")
        added = False
        symCo = copy.deepcopy(sums[0].getSymbolCo())
        tensors = copy.deepcopy(sums[0].getTensors())
        variations = copy.deepcopy(sums[0].getVariations())
        etas = copy.deepcopy(sums[0].getEtas())
        deltas = copy.deepcopy(sums[0].getDeltas())
        partials = copy.deepcopy(sums[0].getPartials())
        tensorCos = copy.deepcopy(sums[0].getTensorCos())
        numCosList = list()
        for sum1 in sums:
            numCosList.append(sum1.getNumCo())
        numCo = min(numCosList)
        inAll = True
        for frac in numCosList:
            if frac % numCo != Fraction(0):
                inAll = False
        if inAll:
            otherTerm.addNumCo(numCo)
            added = True
            for sum2 in sums:
                sum2.setNumCo(sum2.getNumCo()/numCo)
        inAll = True
        for sum1 in sums:
            if not symCo == sum1.getSymbolCo():
                inAll = False
        if inAll:
            otherTerm.setSymCo(symCo)
            added = True
            for sum2 in sums:
                sum2.setSymCo(SymbolCo())
        inAll = True
        for sum1 in sums:
            if not tensorCos == sum1.getTensorCos():
                inAll = False
        if inAll:
            otherTerm.addTensorCos(tensorCos)
            added = True
            for sum2 in sums:
                sum2.setTensorCos(TensorCoefficients([Coefficient()]))
        for tensor in tensors:
            inAll = True
            for sum1 in sums:
                if tensor not in sum1.getTensors():
                    inAll = False
            if inAll:
                otherTerm.addTensors(tensor)
                added = True
                for sum2 in sums:
                    sum2.removeTensor(tensor)
        for variation in variations:
            inAll = True
            for sum1 in sums:
                if variation not in sum1.getVariations():
                    inAll = False
            if inAll:
                otherTerm.addVariations(variation)
                added = True
                for sum2 in sums:
                    sum2.removeVar(variation)
        for delta in deltas:
            inAll = True
            for sum1 in sums:
                if delta not in sum1.getDeltas():
                    inAll = False
            if inAll:
                otherTerm.addDeltas(delta)
                added = True
                for sum2 in sums:
                    sum2.removeDelta(delta)
        for eta in etas:
            inAll = True
            for sum1 in sums:
                if eta not in sum1.getEtas():
                    inAll = False
            if inAll:
                otherTerm.addEtas(eta)
                added = True
                for sum2 in sums:
                    sum2.removeEta(eta)
        for partial in partials:
            inAll = True
            for sum1 in sums:
                if partial not in sum1.getPartials():
                    inAll = False
            if inAll:
                otherTerm.addPartials(partial)
                added = True
                for sum2 in sums:
                    sum2.removePartial(partial)
        if added:
            node.setRight(EquationNode(Summation([otherTerm])))
            node.setLeft(EquationNode(node.getElement()))
            node.setElement(Sign("*"))

    def combineLikeTerms(self, node):
        if node is not None:
            self.combineLikeTerms(node.getRight())
            self.combineLikeTerms(node.getLeft())
            if node.isSum():
                node.getElement().combineLikeTerms()

    def combineLikeTermsWithoutSymCo(self, node):
        if node is not None:
            self.combineLikeTermsWithoutSymCo(node.getRight())
            self.combineLikeTermsWithoutSymCo(node.getLeft())
            if node.isSum():
                node.getElement().combineLikeTermsWithoutSymCo()

    def subTreeRepr(self, node, strx):
        if node is not None:
            brac = node.getBrackets()
            if brac:
                strx += "\\("

            if type(node.getElement()) is Sign and node.getElement() == Sign("*"):
                if node.getRight() is not None and node.getRight().isSum():
                    if len(node.getRight().getElement().getSums()) == 1:
                        node.getRight().getElement().getSums()[0].setShowNum(False)
                    else:
                        for summ in node.getRight().getElement().getSums():
                            summ.setShowNum(True)
                if node.getLeft() is not None and node.getLeft().isSum():
                    if len(node.getLeft().getElement().getSums()) == 1:
                        node.getLeft().getElement().getSums()[0].setShowNum(False)
                    else:
                        for summ in node.getLeft().getElement().getSums():
                            summ.setShowNum(True)
                #if node.getRight().isLeaf():
                strx += self.subTreeRepr(node.getRight(), "")
                # else:
                #     strx += "\\(" + self.subTreeRepr(node.getRight(), "") + "\\)"
                # if node.getLeft().isLeaf():
                strx += self.subTreeRepr(node.getLeft(), "")
                # else:
                #     strx += "\\(" + self.subTreeRepr(node.getLeft(), "") + "\\)"
            else:
                if node.getLeft() is not None and node.getLeft().isSum():
                    for summ in node.getLeft().getElement().getSums():
                        summ.setShowNum(True)
                if node.getRight() is not None and node.getRight().isSum():
                    for summ in node.getRight().getElement().getSums():
                        summ.setShowNum(True)
                strx += self.subTreeRepr(node.getRight(), "") + repr(node.getElement()) + self.subTreeRepr(node.getLeft(), "")
            if brac:
                strx += "\\)"
            return strx
        else:
            return ""

    def sortEach(self, node):
        if node.isLeaf():
            node.getElement().sortEach()
        else:
            self.sortEach(node.getRight())
            self.sortEach(node.getLeft())

    def sortTerms(self, node):
        if node.isLeaf():
            node.getElement().sortTerms()
        else:
            self.sortTerms(node.getRight())
            self.sortTerms(node.getLeft())


    def printTreeAsTree(self, list):
        if len(list) > 0:
            for node in list:
                print(repr(node.getElement()), end="; ")
            print()
            newl = copy.deepcopy(list)
            for i in range(len(newl)):
                list.remove(list[0])
                if newl[i].getRight() is not None:
                    list.append(newl[i].getRight())
                if newl[i].getLeft() is not None:
                    list.append(newl[i].getLeft())
            self.printTreeAsTree(list)

    def movePastCommands(self, strx, char):
        delims = [" ", "\\", "}", ")", "]", "{", "(", "[", "_", "^"]
        if strx[char] == "\\":
            i = char+1
            while i < len(strx) and (strx[i] not in delims):
                i += 1
            char = i
        return char

    def getLenFrac(self, strx):
        strx = strx.replace("\\frac", "")
        while strx.startswith(" "):
            strx = strx[1:]
        split = self.finishBracketSet(strx, 0, "{", "}")
        num = strx[:split]
        while num.startswith(" ") or num.startswith("{"):
            num = num[1:]
        while num.endswith(" ") or num.endswith("}"):
            num = num[:len(num)-1]
        den = strx[split+1:]
        while den.startswith(" ") or den.startswith("{"):
            den = den[1:]
        while den.endswith(" ") or den.endswith("}"):
            den = den[:len(den)-1]
        lenDen = self.getVisLen(den)
        lenNum = self.getVisLen(num)
        return max(lenDen, lenNum)

    def getVisLen(self, strx):
        invisChar = ["{", "}", "_", "^"]
        place = visLen = 0
        while place < len(strx):
            if strx[place] in invisChar:
                place += 1
            elif strx[place] == "\\":
                first = place
                place = self.movePastCommands(strx, first)
                if strx[first: place] in self.oneCommands:
                    visLen += 1
            else:
                visLen += 1
                place += 1
        return visLen

    def finishBracketSet(self, strx, first, openB, closeB):
        char = first
        if len(strx) > first:
            done = False
        else:
            done = True
        brackets = list()
        while not done and char < len(strx):
            if strx[char] == openB:
                brackets.append(strx[char])
                char += 1
            elif strx[char] == closeB:
                brackets.pop()
                if len(brackets) == 0:
                    done = True
                else:
                    char += 1
            else:
                char += 1
        last = char
        return last

    def remExtraBrac(self, strx):
        last = 0
        while "(" in strx[last:]:
            first = strx.find("(", last)
            if first < len(strx)-2:
                figs = first +1
                while strx[first+1] == " ":
                    first += 1
                if strx[first+1: first+3] == "\\(":
                    last = self.finishBracketSet(strx, first+2, "(", ")")
                    while strx[last+1] == " ":
                        last += 1
                    if strx[last+1: last+3] == "\\)":
                        strx = strx[:first+1] + strx[first+3:last+1] + strx[last+3:]

                last = figs
            else:
                last = first
        return strx

    def isSurroundedByCurly(self, strx, place):
        last = strx.find("}", place)
        if last == -1:
            return False
        first = self.backFinishBracket(strx, last, "{", "}")
        if first < place:
            return True
        else:
            return False

    def backFinishBracket(self, strx, first, closeB, openB):
        char = first
        if first > 0:
            done = False
        else:
            done = True
        brackets = list()
        while not done and first > 0:
            if strx[char] == openB:
                brackets.append(strx[char])
                char += -1
            elif strx[char] == closeB:
                brackets.pop()
                if len(brackets) == 0:
                    done = True
                else:
                    char += -1
            else:
                char += -1
        last = char
        return last

    ##
    # skip brackets will take in the initial bracket position in a string and output the final bracket position for (), [], {} brackets
    # @param strx the string the brackets need to be skipped over in
    # @param place the (string index) position of the first bracket in the set
    # @param direction if "+" (or no input) traverses the string left to right, if "-" traverses right to left
    # @return the (string index) position of the closing bracket
    #
    def skipBrackets(self, strx, place, direction="+"):
        if direction == "-":  # move right to left, start at "closing" bracket
            # figure out which type of bracket the first is and call backFinishBracket on this type
            if strx[place] == ")":
                place = self.backFinishBracket(strx, place, "(", ")")
            elif strx[place] == "}":
                place = self.backFinishBracket(strx, place, "{", "}")
            elif strx[place] == "]":
                place = self.backFinishBracket(strx, place, "[", "]")
        else:  # move left to right, start at "opening" bracket
            # figure out which type of bracket the first is and call finishBracketSet on this type
            if strx[place] == "(":
                place = self.finishBracketSet(strx, place, "(", ")")
            elif strx[place] == "{":
                place = self.finishBracketSet(strx, place, "{", "}")
            elif strx[place] == "[":
                place = self.finishBracketSet(strx, place, "[", "]")
        return place

    def __repr__(self):
        invisChar = ["{", "}", "_", "^"]
        strx = self.subTreeRepr(self.root, "")
        strx = ' '.join(strx.split())
        strx = strx.replace("+-", "-")
        strx = strx.replace("+ -", "-")
        strx = self.remExtraBrac(strx)
        numVis = place = agedPlace = 0
        while place < len(strx):
            if strx[place] in invisChar:
                place += 1
            elif strx[place] == "\\":
                first = place
                place = self.movePastCommands(strx, first)
                if strx[first: place] in self.oneCommands:
                    numVis += 1
                elif strx[first: place] == "\\frac":
                    if strx[place] == "{":
                        place = self.finishBracketSet(strx, self.finishBracketSet(strx, place, "{", "}")+1, "{", "}")+1
                        numVis += self.getLenFrac(strx[first: place])
                    elif strx[first: place] == "\\(" or "\\)":
                        numVis += 2
                    else:
                        place += 1
                        numVis += 1
            else:
                numVis += 1
                place += 1
            # check if long enough to split
            if numVis > 85 and place < len(strx):
                numVis = 0
                oldPlace = place
                while place > agedPlace and strx[place: place+2] != "\\(":  # get out of brackets
                    place += -1
                if place < agedPlace + 40:
                    place = oldPlace

                while not ((strx[place] == "+" and not self.isSurroundedByCurly(strx, place)) or (strx[place] == "-" and not self.isSurroundedByCurly(strx, place))) and place > agedPlace:
                    if place > 0 and strx[place-1:place+1] == "\\)":
                        place += -1
                    place = self.skipBrackets(strx, place, "-")
                    if place > 0:
                        place += -1
                if place == agedPlace:
                    place = oldPlace
                    while not ((strx[place] == "+" and not self.isSurroundedByCurly(strx, place)) or (strx[place] == "-" and not self.isSurroundedByCurly(strx, place))) and place > 0:
                        place += -1
                        #print(place)
                if place == 0 or ("\\\\" in strx[place - 10: place + 10]):
                    strx = strx[:oldPlace] + " \\\\ \n " + strx[oldPlace:]
                    place = oldPlace + 6
                    #print(strx[place - 20: place + 10])
                else:
                    strx = strx[:place] + " \\\\ \n " + strx[place:]
                    place = place + 6
                    #print(strx[place-20: place+10])
                agedPlace = place
        if self.eqIndicator:
            if "\\\\" in strx:
                strx = "\\begin{multline} \n" + strx + "\n\\end{multline}"
            else:
                strx = "\\begin{equation} \n" + strx + "\n\\end{equation}"
        return strx
