from Tensors.Fraction import Fraction
from Tensors.Tensor import Tensor
from Tensors.SymbolCo import SymbolCo
from Tensors.Delta import Delta
from Tensors.Eta import Eta
from Tensors.Partial import Partial
from Tensors.Variation import Variation
from Tensors.Summation import Summation
from Tensors.TensorCoefficients import TensorCoefficients
from Tensors.Coefficient import Coefficient
from Tensors.Gemma import Gemma
import copy
class MultGroup:
    ##
    # constructor for class MultGroup
    # @param sign defines if the multiplication group is positive or negative
    # @param numCo the number that that the multiplication group is multiplied by (Fraction class)
    # @param symbolCo any coefficients of the multiplication group that are not numbers (SymbolCo class)
    # @param tensors a list of all the tensors in the multiplication group (contains objects of Tensor class)
    # @param variations a list of all the variations in the multiplication group (contains objects of Variation class)
    # @param etas a list of all the etas the multiplication group is multiplied by (contains objects of Eta class)
    # @param deltas a list of all the deltas the multiplication group is multiplied by (contains objects of Delta class)
    # @param partials a list of all the partials acting on the WHOLE multiplication group (contains objects of Partial class)
    # @param outerPartials special case where multiplication group is just partials and constants - not tensors or variations, a list containing Partial objects
    # @param things a list that can contain tensors OR variations OR summations and get sorted into the correct types
    #
    def __init__(self, sign, numCo=None, symbolCo=None, tensors=None, variations=None, etas=None, deltas=None, partials=None, tensorCos=None, things=None):
        self.showNum = True
        self.sign = sign
        if self.sign == "-":
            self.showSign = True
        else:
            self.showSign = False
        if tensorCos is None:
            self.tensorCos = TensorCoefficients([Coefficient()])
        elif type(tensorCos) is TensorCoefficients:
            self.tensorCos = tensorCos
        else:
            raise TypeError("NOT A TENSOR COEFFICIENT. type is: ", type(tensorCos))
        self.tensors = list()
        if tensors is not None:
            for tensor in tensors:
                if type(tensor) is Tensor:
                    tensor.setSums()
                    self.tensors.append(tensor)
                else:
                    raise TypeError()
        self.variations = list()
        if variations is not None:
            for el in variations:
                if type(el) is Variation:
                    el.setSums()
                    self.variations.append(el)
                else:
                    raise TypeError
        self.etas = list()
        if etas is not None:
            for eta in etas:
                if type(eta) is Eta:
                    for ind in eta.getIndices():
                        ind.setOwner("e")
                    self.etas.append(eta)
                else:
                    raise TypeError()
        self.deltas = list()
        if deltas is not None:
            for delta in deltas:
                if type(delta) is Delta:
                    for ind in delta.getIndices():
                        ind.setOwner("d")
                    self.deltas.append(delta)
                else:
                    raise TypeError()
        if numCo is None:
            self.numCo = Fraction(1)
        elif type(numCo) is Fraction:
            self.numCo = copy.deepcopy(numCo)
        else:
            raise TypeError()
        if symbolCo is None:
            self.symbolCo = SymbolCo()
        elif type(symbolCo) is SymbolCo:
            self.symbolCo = symbolCo
        else:
            raise TypeError
        self.partials = list()
        if partials is not None:
            for el in partials:
                if type(el) is Partial:
                    self.partials.append(el)
                else:
                    raise TypeError
        if things is not None:
            for el in things:
                if type(el) is Tensor:
                    tHash = tensor.getOwnerHash()
                    for ind in tensor.getIndices():
                        ind.setOwner("t"+tHash)
                    for p in tensor.getPartials():
                        p.getIndex().setOwner("tp"+tHash)
                    self.tensors.append(tensor)
                elif type(el) is Variation:
                    for topSum in el.getNum().getSums():
                        for topInd in topSum.getIndices():
                            topInd.addOwner("vn")
                    for botSum in el.getDen().getSums():
                        for botInd in botSum.getIndices():
                            botInd.addOwner("vd")
                        for p in el.getPartials():
                            p.getIndex().addOwner("vp")
                    hashy = el.getOwnerHash()
                    for index in el.getFullIndices():
                        index.addOwner(hashy)
                    self.variations.append(el)
                else:
                    raise TypeError(" 'things' must only contain tensors and variations")
        if len(self.tensors) == 0 and len(self.variations) == 0 and len(self.etas) == 0 and len(self.deltas) == 0 and self.numCo == Fraction(1) and self.symbolCo == SymbolCo() and len(self.partials) != 0:
            self.isPartials = True
        else:
            self.isPartials = False
        if len(self.tensors) == 0 and len(self.variations) == 0 and len(self.etas) == 0 and len(self.deltas) == 0 and len(self.partials) != 0:
            self.isPartialsAndCos = True
        else:
            self.isPartialsAndCos = False
        mlp = list()
        for tensor in self.tensors:
            mlp.append(len(tensor.getPartials()))
        if len(mlp) == 0:  # no tensors
            self.minLenP = -1
        else:
            num = ""
            mlp.sort()
            for el in mlp:
                num += repr(el)
            self.minLenP = int(num)
        self.setSums(True)

    def setShowNum(self, bool):
        self.showNum = bool

    def sort(self):
        self.tensors.sort()

    def setShowSign(self, bool):
        self.showSign = bool

    def getTensors(self):
        return self.tensors

    def getVariations(self):
        return self.variations

    def getSign(self):
        return self.sign

    def getEtas(self):
        return self.etas

    def getDeltas(self):
        return self.deltas

    def getNumCo(self):
        return self.numCo

    def getSymbolCo(self):
        return self.symbolCo

    def getSymCo(self):
        return self.symbolCo

    def getTensorCos(self):
        if not type(self.tensorCos) is TensorCoefficients:
            raise TypeError("not type in get")
        return self.tensorCos

    def getTensorCo(self):
        if not type(self.tensorCos) is TensorCoefficients:
            raise TypeError("not type in get")
        return self.tensorCos

    def getPartials(self):
        return self.partials

    def getMinLenP(self):
        return self.minLenP

    def hasEtas(self):
        if len(self.etas) > 0:
            return True
        else:
            return False

    def hasDeltas(self):
        if len(self.deltas) > 0:
            return True
        else:
            return False

    def hasPartials(self):
        if len(self.partials) > 0:
            return True
        else:
            return False

    def hasTensors(self):
        if len(self.tensors) > 0:
            return True
        else:
            return False

    def hasVariations(self):
        if len(self.variations) > 0:
            return True
        else: return False

    def changeSign(self, newSign):
        self.sign = newSign

    def swapSign(self):
        if self.sign == "-":
            self.sign = "+"
        else:
            self.sign = "-"

    def setNumCo(self, newCo):
        self.numCo = copy.deepcopy(newCo)

    def setSymCo(self, newCo):
        self.symbolCo = copy.deepcopy(newCo)

    def setTensorCos(self, newCo):
        if not type(newCo) is TensorCoefficients:
            raise TypeError("not type in get")
        self.tensorCos = newCo
        if not type(self.tensorCos) is TensorCoefficients:
            raise TypeError("not type in get")

    # @param newCo is number
    def addNumCo(self, newCo):
        self.numCo = copy.deepcopy(self.numCo)*copy.deepcopy(newCo)

    # @param newCo is string
    def addSymbolCo(self, newCo):
        if newCo is SymbolCo:
            self.symbolCo = self.symbolCo*newCo

    def addSymCo(self, newCo):
        if newCo is SymbolCo:
            self.symbolCo = self.symbolCo*newCo

    def addPartials(self, newP):
        newP.getIndex().setSums(False)
        newP.getIndex().setSumType(Gemma())
        self.partials.append(newP)
        self.setSums(True)

    def setPartials(self, pList):
        for newP in pList:
            newP.getIndex().setSums(False)
            newP.getIndex().setSumType(Gemma())
        self.partials = pList
        self.setSums(True)

    def addTensors(self, newTensor):
        newTensor.setSums()
        if newTensor.getSign() != self.sign:
            self.changeSign("-")
        elif newTensor.getSign() == self.sign:
            self.changeSign("+")
        newTensor.changeSign("+")
        self.tensors.append(newTensor)
        tenHash = newTensor.getOwnerHash()
        for ind in newTensor.getIndices():
            ind.setOwner("t"+tenHash)
        for p in newTensor.getPartials():
            p.getIndex().setOwner("tp"+tenHash)
        self.setSums(True)

    def addVariations(self, var):
        var.setSums()
        if var.getSign() != self.sign:
            self.changeSign("-")
        elif var.getSign() == self.sign:
            self.changeSign("+")
        var.setSign("+")
        for topSum in var.getNum().getSums():
            for topInd in topSum.getIndices():
                topInd.addOwner("vn")
        for botSum in var.getDen().getSums():
            for botInd in botSum.getIndices():
                botInd.addOwner("vd")
        for p in var.getPartials():
            p.getIndex().addOwner("vp")
        hashy = var.getOwnerHash()
        for index in var.getFullIndices():
            index.addOwner(hashy)
        self.variations.append(var)
        self.setSums(True)

    def addEtas(self, etaList):
        if type(etaList) is list:
            for eta in etaList:
                self.addEta(eta)
        else:
            self.addEta(etaList)

    def addEta(self, eta):
        self.etas.append(eta)
        self.setSums(True)

    def addDeltas(self, deltaList):
        if type(deltaList) is list:
            for delta in deltaList:
                self.addDelta(delta)
        else:
            self.addDelta(deltaList)

    def addDelta(self, delta):
        self.deltas.append(delta)
        self.setSums(True)

    def addTensorCos(self, newCo):
        if not type(self.tensorCos) is TensorCoefficients:
            raise TypeError("not type in get")
        if not type(newCo) is TensorCoefficients:
            raise TypeError("not type in get")
        return self.getTensorCos()+newCo

    def __lt__(self, other):
        return self.getMinLenP() < other.getMinLenP()

    def removeTensor(self, tensor):
        tenCop = copy.deepcopy(tensor)
        tenCop.setSums()
        for i in range(len(self.tensors)):
            ten2Check = copy.deepcopy(self.tensors[i])
            ten2Check.setSums()
            if ten2Check == tenCop:
                self.tensors.pop(i)
                self.setSums(True)
                return
        #if tensor in self.getTensors():
            #self.getTensors().remove(tensor)


    def removeTensorRef(self, tensor):
        for i in range(len(self.tensors)):
            if self.tensors[i] is tensor:
                self.tensors.pop(i)
                self.setSums(True)
                return

    def removeVar(self, var):
        varCop = copy.deepcopy(var)
        varCop.setSums()
        for v in range(len(self.variations)):
            var2Check = copy.deepcopy(self.variations[v])
            var2Check.setSums()
            if varCop == var2Check:
                self.variations.pop(v)
                self.setSums(True)
                return
            #self.setSums(True)

    def removeVarRef(self, var):
        for i in range(len(self.variations)):
            if self.variations[i] is var:
                self.variations.pop(i)
                self.setSums(True)
                return

    def removeDelta(self, remDel):
        if remDel in self.getDeltas():
            self.deltas.remove(remDel)
            self.setSums(True)


    def removeDeltaRef(self, remDel):
        for d in range(len(self.deltas)):
            if self.deltas[d] is remDel:
                self.deltas.pop(d)
                self.setSums(True)
                return
    ##
    # getIndices collects all the indices associated with a MultGroup object
    # @return a list of the indices
    #
    def getIndices(self):
        indices = list()
        for d in self.getDeltas():
            for ind in d.getIndices():
                indices.append(ind)
        for e in self.getEtas():
            for ind in e.getIndices():
                indices.append(ind)
        for p in self.getDeltas():
            for ind in p.getPartials():
                indices.append(ind)
        for t in self.getTensors():
            for tp in t.getPartials():
                indices.append(tp.getIndex())
            for ind in t.getIndices():
                indices.append(ind)
        for v in self.getVariations():
            for vp in v.getPartials():
                indices.append(vp.getIndex())
            for s in range(len(v.getNum().getSums())):
                for i in range(len(v.getNum().getSums()[s].getIndices())):
                    indices.append(v.getNum().getSums()[s].getIndices()[i])
            for s in range(len(v.getDen().getSums())):
                for i in range(len(v.getDen().getSums()[s].getIndices())):
                    indices.append(v.getDen().getSums()[s].getIndices()[i])
        return indices

    ##
    # setSums goes through each index in the MultGroup object and set its sumType
    #
    def setSums(self, full=True):
        indices = self.getIndices()
        for itt in range(len(indices)):
            indices[itt].setSum(False)
            indices[itt].setSumType(Gemma())
        for i in range(len(indices)):
            possSum = copy.deepcopy(indices[i])
            #print(possSum)
            for j in range(i+1, len(indices)):
                if indices[j].sumsWith(possSum):
                    #print(indices[j], "sums with ", indices[i])
                    indices[i].setSum(True, indices[j])
                    indices[j].setSum(True, indices[i])
                    sumType = Gemma()
                    sumType.add(indices[i].getOwner())
                    sumType.add(indices[j].getOwner())
                    indices[i].setSumType(copy.deepcopy(sumType))
                    indices[j].setSumType(copy.deepcopy(sumType))
        if full:
            for d in self.getDeltas():
                numSums = 0
                otherOwners = list()
                for ind in d.getIndices():
                    if ind.hasSum():
                        numSums += 1
                        part = ind.getPartnerInCrime()
                        if part is not None:
                            otherOwners.append(part.getOwner())  # should be adding strings
                otherOwners.sort()
                for indy in d.getIndices():
                    indy.addOwner(str(numSums))
                    for el in otherOwners:
                        indy.addOwner(el)
            for e in self.getEtas():
                numSums = 0
                otherOwners = list()
                for ind in e.getIndices():
                    if ind.hasSum():
                        numSums += 1
                        part = ind.getPartnerInCrime()
                        if part is not None:
                            otherOwners.append(part.getOwner())
                otherOwners.sort()
                for indy in e.getIndices():
                    indy.addOwner(str(numSums))
                    for el in otherOwners:
                        indy.addOwner(el)
            self.setSums(False)

    ##
    # contract Deltas iterates through the deltas of the Multline object and and for each delta iterates through all
    # the other tensors (including other deltas and variations) and checks if any are contractible with the delta.
    # The first contractible one will be contracted and the delta removed
    # @return a multline object with the original information if no contraction happened, else with "contracted information"
    #
    def contractDeltas(self):
        # contraction is done by replacing any index that sums with one of the delta indices with the other delta index
        copyDels = copy.deepcopy(self.deltas)
        realDel = -1
        for d in range(len(copyDels)):
            realDel += 1
            delta = copyDels[d]
            inds = delta.getIndices()
            first = inds[0]  # a delta should have exactly two indices
            second = inds[1]
            done = False  # create a switch to flip if contraction occurs, so contraction occurs once at most
            for d in range(len(self.deltas)):
                if self.deltas[d] != delta:  # CAN'T CONTRACT WITH SELF
                    if not done:
                        for dindex in self.deltas[d].getIndices():
                            if not done and first.sumsWith(dindex):
                                self.deltas[d].getSym().changeIndex(dindex, second)
                                done = True
                            elif not done and second.sumsWith(dindex):
                                self.deltas[d].getSym().changeIndex(dindex, first)
                                done = True
            for e in range(len(self.etas)):
                if not done:
                    for eindex in self.etas[e].getIndices():
                        if not done and first.sumsWith(eindex):
                            self.etas[e].getSym().changeIndex(eindex, second)
                            done = True
                        elif not done and second.sumsWith(eindex):
                            self.etas[e].getSym().changeIndex(eindex, first)
                            done = True
            for t in range(len(self.tensors)):
                if not done:
                    for tp in range(len(self.tensors[t].getPartials())):
                        if not done and self.tensors[t].getPartials()[tp].getIndex().sumsWith(first):
                            self.tensors[t].getPartials()[tp].setIndex(second)
                            done = True
                        elif not done and self.tensors[t].getPartials()[tp].getIndex().sumsWith(second):
                            self.tensors[t].getPartials()[tp].setIndex(first)
                            done = True
                    for tindex in self.tensors[t].getIndices():
                        if not done and first.sumsWith(tindex):
                            self.tensors[t].getSym().changeIndex(tindex, second)
                            done = True
                        elif not done and second.sumsWith(tindex):
                            self.tensors[t].getSym().changeIndex(tindex, first)
                            done = True
            for p in range(len(self.partials)):  # deal with partials
                if not done and first.sumsWith(self.partials[p].getIndex()):
                    self.partials[p].setIndex(second)
                    done = True
                elif not done and second.sumsWith(self.partials[p].getIndex()):
                    self.partials[p].setIndex(first)
                    done = True
            for v in range(len(self.variations)):  # deal with variations
                for m in range(len(self.variations[v].getNum().getSums())):  # first contract any deltas already in variation
                    # self.variations[v].getNum().replaceTerm(self.variations[v].getNum().getSums()[m], self.variations[v].getNum().getSums()[m].contractDeltas())
                    self.variations[v].getNum().getSums()[m].contractDeltas()
                if not done:
                    for vp in range(len(self.variations[v].getPartials())):
                        if (not done) and self.variations[v].getPartials()[vp].getIndex().sumsWith(first):
                            self.variations[v].getPartials()[vp].setIndex(second)
                            done = True
                        elif (not done) and self.variations[v].getPartials()[vp].getIndex().sumsWith(second):
                            self.variations[v].getPartials()[vp].setIndex(first)
                            done = True
                # if not done:
                #     # contracting the numerator with delta
                #     multIn = False  # create var to see if test (are any Multlines in numerator contractible) passed
                #     for mn in self.variations[v].getNum().getSums():  # iterate through the Multline objects in the Summation
                #         yn = copy.deepcopy(mn)  # create a copy of the Multline object, so original is not affected by test
                #         yn.addDeltas(delta)  # multiply delta into numerator
                #         zn = copy.deepcopy(yn)  # create another copy which will be contracted
                #         zn = zn.contractDeltas()  # try contracting, returns original if no contraction
                #         if not yn == zn:  # check if the contraction changed anything
                #             multIn = True  # if it did, then the numerator is contractible
                #     if multIn:
                #         done = True
                #         for m in range(len(self.variations[v].getNum().getSums())):
                #             self.variations[v].getNum().getSums()[m].addDeltas(delta)
                #             #self.variations[v].getNum().replaceTerm(self.variations[v].getNum().getSums()[m], self.variations[v].getNum().getSums()[m].contractDeltas())
                #             self.variations[v].getNum().getSums()[m].contractDeltas()
                # if not done:
                #     # contracting the denominator (note the use of the denominator with switched heights, following
                #     # tensor logic) with delta - code uses same logic as code for numerator
                #     multIn = False
                #     for md in self.variations[v].getDen().getSums():  # use denominator with height switched for accurate logic!
                #         yd = copy.deepcopy(md)
                #         yd.addDeltas(delta)
                #         zd = copy.deepcopy(yd)
                #         zd = zd.contractDeltas()
                #         if yd != zd:
                #             multIn = True
                #     if multIn:
                #         done = True
                #         for m in range(len(self.variations[v].getDen().getSums())):
                #             self.variations[v].getDen().getSums()[m].addDeltas(delta)
                #             #self.variations[v].getNum().replaceTerm(self.variations[v].getDen().getSums()[m], self.variations[v].getDen().getSums()[m].contractDeltas())
                #             self.variations[v].getDen().getSums()[m].contractDeltas()
                #         self.variations[v].changeTrueDen(self.variations[v].getDen())  # change the TRUE version of the denominator too!
            if done:  # means the delta was contracted (used up essentially) at some point and must be gotten rid of
                self.removeDeltaRef(self.deltas[realDel])
                realDel += -1
        self.setSums(True)
        return MultGroup(self.sign, self.numCo, self.symbolCo, self.tensors, self.variations, self.etas, self.deltas, self.partials)

    def removeEta(self, remEt):
        if remEt in self.getEtas():
            self.etas.remove(remEt)
            self.setSums(True)

    def removeEtaRef(self, remEt):
        for e in range(len(self.etas)):
            if self.etas[e] is remEt:
                self.etas.pop(e)
                self.setSums(True)
                return
    ##
    # contract Etas iterates through the etas of the MultGroup object and and for each eta iterates through all
    # the other tensors (including other etas but NOT variations) and checks if any are contractible with the eta.
    # The first contractible one will be contracted and the eta removed
    # @return a multline object with the original information if no contraction happened, else with "contracted information"
    #
    def contractEtas(self):
        copyEts = copy.deepcopy(self.etas)
        realEt = -1
        for eta in copyEts:
            realEt += 1
            inds = eta.getIndices()
            first = inds[0]
            second = inds[1]
            done = False
            for e in range(len(self.etas)):
                if self.etas[e] != eta:
                    for eindex in self.etas[e].getIndices():
                        if (not done) and first.sumsWith(eindex):
                            self.etas[e].getSym().changeIndex(eindex, second)
                            done = True
                        elif (not done) and second.sumsWith(eindex):
                            self.etas[e].getSym().changeIndex(eindex, first)
                            done = True
            for d in range(len(self.deltas)):
                if not done:
                    for dindex in self.deltas[d].getIndices():
                        if (not done) and first.sumsWith(dindex):
                            self.deltas[d].getSym().changeIndex(dindex, second)
                            done = True
                        elif (not done) and second.sumsWith(dindex):
                            self.deltas[d].getSym().changeIndex(dindex, first)
                            done = True
            for t in range(len(self.tensors)):
                if not done:
                    for tp in range(len(self.tensors[t].getPartials())):
                        if (not done) and self.tensors[t].getPartials()[tp].getIndex().sumsWith(first):
                            self.tensors[t].getPartials()[tp].setIndex(second)
                            done = True
                        elif (not done) and self.tensors[t].getPartials()[tp].getIndex().sumsWith(second):
                            self.tensors[t].getPartials()[tp].setIndex(first)
                            done = True
                    for tindex in self.tensors[t].getIndices():
                        if (not done) and first.sumsWith(tindex):
                            self.tensors[t].getSym().changeIndex(tindex, second)
                            done = True
                        elif (not done) and second.sumsWith(tindex):
                            self.tensors[t].getSym().changeIndex(tindex, first)
                            done = True
            for p in range(len(self.partials)):  # deal with partials
                if not done and first.sumsWith(self.partials[p].getIndex()):
                    self.partials[p].setIndex(second)
                    done = True
                elif not done and second.sumsWith(self.partials[p].getIndex()):
                    self.partials[p].setIndex(first)
                    done = True
            for v in range(len(self.variations)):  # deal with variations
                for m in range(len(self.variations[v].getNum().getSums())):  # first contract any etas already in variation
                    #self.variations[v].getNum().replaceTerm(self.variations[v].getNum().getSums()[m], self.variations[v].getNum().getSums()[m].contractDeltas())
                    self.variations[v].getNum().getSums()[m].contractEtas()
                if not done:
                    for vp in range(len(self.variations[v].getPartials())):
                        if (not done) and self.variations[v].getPartials()[vp].getIndex().sumsWith(first):
                            self.variations[v].getPartials()[vp].setIndex(second)
                            done = True
                        elif (not done) and self.variations[v].getPartials()[vp].getIndex().sumsWith(second):
                            self.variations[v].getPartials()[vp].setIndex(first)
                            done = True
            if done:
                self.removeEtaRef(self.etas[realEt])
                realEt += -1
        self.setSums(True)
        return MultGroup(self.sign, self.numCo, self.symbolCo, self.tensors, self.variations, self.etas, self.deltas, self.partials)

    ##
    # removePartial will remove 1 partial from the list, IF that partial is in the list
    # @param the partial to be removed
    # @param partial the partial derivative to be removed
    #
    def removePartial(self, partial):
        if partial in self.partials:
            self.partials.remove(partial)
            self.setSums(True)

    def removePartialRef(self, part):
        for i in range(len(self.partials)):
            if self.partials[i] is part:
                self.partials.pop(i)
                self.setSums(True)
                return

    ##
    # distributePartial performs the product rule on a list of tensors/ variations where each element in the list is assumed to be multiplied
    # @param partial the partial derivative to perform the product rule with
    # @param listy the list of tensors and variations from the MultGroup
    # @return the summation object that is the result of the product rule
    #
    def distributePartial(self, partial, listy):
        if self.isOnlyPartials():  # there are no tensors, but the result is not zero
            return Summation([self.addPartials(partial)])
        if len(listy) == 0:
            return Summation([MultGroup("+", Fraction(0))])  # if there are no tensors and no variations, everything is a constant, and the derivative is zero
        if len(listy) == 1:
            first = listy[0]
            derFirst = copy.deepcopy(first)
            derFirst.addPartials(copy.deepcopy(partial))
            multFirst = MultGroup(self.getSign())
            multFirst.addThing(derFirst)  # multGroup object
            self.addConstantAttributes(multFirst)
            return Summation([multFirst])  # summation object
        if len(listy) == 2:
            sums = Summation()
            first = listy[0]
            derFirst = copy.deepcopy(first)
            derFirst.addPartials(copy.deepcopy(partial))
            second = listy[1]
            derSecond = copy.deepcopy(second)
            derSecond.addPartials(copy.deepcopy(partial))
            derFirstTimesSecond = MultGroup(copy.deepcopy(self.sign))
            derFirstTimesSecond.addThing(derFirst)
            derFirstTimesSecond.addThing(second)
            self.addConstantAttributes(derFirstTimesSecond)
            derSecondTimesFirst = MultGroup(copy.deepcopy(self.sign))
            derSecondTimesFirst.addThing(derSecond)
            derSecondTimesFirst.addThing(first)
            self.addConstantAttributes(derSecondTimesFirst)
            sums.addTerm(derFirstTimesSecond)
            sums.addTerm(derSecondTimesFirst)
            return sums  # summation object
        else:
            sums = Summation()  # initialize EMPTY summation - to be returned
            first = listy[0]
            derFirst = copy.deepcopy(first)
            derFirst.addPartials(copy.deepcopy(partial))
            second = listy[1:]  # the rest of the terms in the list, treated as one
            derSecond = self.distributePartial(copy.deepcopy(partial), second)  # summation object, with product rule performed to find derivative
            derFirstTimesSecond = MultGroup(copy.deepcopy(self.sign))
            derFirstTimesSecond.addThing(derFirst)
            for el in second:
                derFirstTimesSecond.addThing(el)
            self.addConstantAttributes(derFirstTimesSecond)
            sums.addTerm(derFirstTimesSecond)
            derSecondTimesFirst = copy.deepcopy(derSecond)
            for el in derSecondTimesFirst.getSums():
                el.addThing(first)
            sums = sums+derSecondTimesFirst
            return sums  # summation object

    ##
    # addConstantAttributes adds all the terms which are constants from the MultGroup object it is called on to the parameter MultGroup object
    # @param multGroup the multgroup obejct to add the constant attributes to
    #
    def addConstantAttributes(self, multGroup):
        multGroup.addNumCo(copy.deepcopy(self.getNumCo()))
        multGroup.addSymbolCo(copy.deepcopy(self.getSymbolCo()))
        multGroup.addEtas(copy.deepcopy(self.getEtas()))
        multGroup.addDeltas(copy.deepcopy(self.getDeltas()))
        multGroup.addTensorCos(copy.deepcopy(self.getTensorCos()))

    ##
    # addThing allows one to add a non-constant attribute without knowing if it is a Tensor object or Variation object
    # @param thing the object to be added to the multgroup
    #
    def addThing(self, thing):
        if type(thing) is Tensor:
            self.addTensors(thing)
            self.setSums(True)
        elif type(thing) is Variation:
            self.addVariations(thing)
            self.setSums(True)
        else:
            raise TypeError("thing must be tensor or variation to be added!")

    ##
    # setZero creates a MultGroup object with a value of zero
    # @return a multGroup object with a value of zero
    #
    def setZero(self):
        return MultGroup("+", Fraction(0))

    ##
    # combineCoefficients multiplies both the numerical and symbolic coefficients into the TensorCo object and sets numCo and symCo to 1 and empty, respectively
    #
    def combineCoefficients(self):
        cosToMultIn = TensorCoefficients([Coefficient("+", self.getNumCo(), self.getSymbolCo())])
        self.setTensorCos(self.getTensorCos()*cosToMultIn)
        self.setNumCo(Fraction(1))
        self.setSymCo(SymbolCo())

    def multWith(self, other):
        for el in other.getEtas():
            self.addEtas(el)
        for el in other.getDeltas():
            self.addDeltas(el)
        for el in other.getTenosrs():
            self.addTensors(el)
        self.addNumCo(other.getNumCo())
        self.addSymbolCo(other.getSymbolCo())
        if self.sign == other.getSign():
            self.changeSign("+")
        else:
            self.changeSign("-")
        self.setSums(True)

    ##
    # isOnlyPartials checks if the MultGroup contains only partials (and constant attributes)
    # @return boolean True or False
    #
    def isOnlyPartials(self):
        if len(self.partials) > 0:
            if len(self.tensors) == 0 and len(self.variations) == 0:
                return True
            else:
                raise TypeError(" cannot have partials and tensors!")
        else:
            return False

    def __mul__(self, other):
        if self.getNumCo() == Fraction(0) or other.getNumCo() == Fraction(0):
            return MultGroup("+", Fraction(0))
        if self.isOnlyPartials() and other.isOnlyPartials():
            partials = copy.deepcopy(self.getPartials()+other.getPartials())  # add lists together
        elif self.isOnlyPartials() or other.isOnlyPartials():
            raise TypeError("can't multiply multgroup with partials!")
        else:
            partials = list()
        if self.sign == other.getSign():
            sign = "+"
        else:
            sign = "-"
        numCo = copy.deepcopy(self.getNumCo())*copy.deepcopy(other.getNumCo())  # has multiplication method
        symCo = copy.deepcopy(self.getSymbolCo())*copy.deepcopy(other.getSymbolCo())  # has multiplication method
        tensorCo = copy.deepcopy(self.getTensorCos())*copy.deepcopy(other.getTensorCos())  # has multiplication method
        tensors = copy.deepcopy(self.getTensors())+copy.deepcopy(other.getTensors())  # add lists together
        variations = copy.deepcopy(self.getVariations())+copy.deepcopy(other.getVariations())  # add lists together
        etas = copy.deepcopy(self.getEtas())+copy.deepcopy(other.getEtas())  # add lists together
        deltas = copy.deepcopy(self.getDeltas())+copy.deepcopy(other.getDeltas())  # add lists together
        return MultGroup(sign, numCo, symCo, tensors, variations, etas, deltas, partials, tensorCo)

    ##
    # multList multiplies out all the elements in a list, using the multiplication methods attached to the elements
    # @param list the list to be multiplied
    # @param return the return object of the multiplication method
    #
    def multList(self, list):
        if len(list) == 0:
            raise TypeError("list MUST HAVE ELEMENTS!!!")
        if (len(list) == 1):
            return list[0]
        elif len(list) == 2:
            return list[0]*list[1]
        else:
            return list[0]*self.multList(list[1:])
    ##
    # testSETListEquality tests if one list contains all the same elements as a second, without considering order
    # @param l1 the first list
    # @param l2 the second list
    # @return boolean True or False
    #
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

    ##
    # combEq tests the equality of the tensor portion of the MultGroup, ignoring sign and coefficients
    # @param other the MultGroup object to be tested against
    # @return Boolean True or False
    #
    def combEq(self, other):
        if not self.testSETListEquality(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testSETListEquality(self.getEtas(), other.getEtas()):
            return False
        if not self.testSETListEquality(self.getTensors(), other.getTensors()):
            return False
        if not self.testSETListEquality(self.getVariations(), other.getVariations()):
            return False
        if not self.testSETListEquality(self.getPartials(), other.getPartials()):
            return False
        return True
    ##
    # isOnyTensor checks if the MultGroup object contains exaclty one tensor and nothing else
    # @return boolean True or False
    #
    def isOnlyTensor(self):
        if len(self.tensors) == 1 and len(self.variations) == 0 and len(self.partials) == 0 and len(self.etas) == 0 and len(self.deltas) == 0 and self.tensorCos == TensorCoefficients([Coefficient()]) and self.symbolCo == SymbolCo() and self.numCo == Fraction(1):
            return True
        else:
            return False

    def isOnlyVar(self):
        if len(self.tensors) == 0 and len(self.variations) == 1 and len(self.partials) == 0 and len(self.etas) == 0 and len(self.deltas) == 0 and self.tensorCos == TensorCoefficients([Coefficient()]) and self.symbolCo == SymbolCo() and self.numCo == Fraction(1):
            return True
        else:
            return False

    def patternEq(self, other):
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        self.factorNumFromTensorCo()
        other.factorNumFromTensorCo()
        if not self.sign == other.getSign():
            return False
        if not self.numCo == other.getNumCo():
            return False
        if not self.getSymbolCo() == other.getSymbolCo():
            return False
        if not self.getTensorCos() == other.getTensorCos():
            return False
        if not self.testPatternSETListEquality(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testPatternSETListEquality(self.getEtas(), other.getEtas()):
            return False
        if not self.testPatternSETListEquality(self.getTensors(), other.getTensors()):
            return False
        if not self.testPatternSETListEquality(self.getVariations(), other.getVariations()):
            return False
        if not self.testPatternSETListEquality(self.getPartials(), other.getPartials()):
            return False
        return True

    def patternEqH(self, other):
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        self.factorNumFromTensorCo()
        other.factorNumFromTensorCo()
        if not self.sign == other.getSign():
            return False
        if not self.numCo == other.getNumCo():
            return False
        if not self.getSymbolCo() == other.getSymbolCo():
            return False
        if not self.getTensorCos() == other.getTensorCos():
            return False
        if not self.testPatternSETListEqualityH(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testPatternSETListEqualityH(self.getEtas(), other.getEtas()):
            return False
        if not self.testPatternSETListEqualityH(self.getTensors(), other.getTensors()):
            return False
        if not self.testPatternSETListEqualityH(self.getVariations(), other.getVariations()):
            return False
        if not self.testPatternSETListEqualityH(self.getPartials(), other.getPartials()):
            return False
        return True

    def patternEqIncludes(self, other):
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        if not repr(other.getSymbolCo()) in repr(self.getSymbolCo()):
            return False
        if (other.getTensorCos() != TensorCoefficients([Coefficient()])) and (other.getTensorCos() != self.getTensorCos()):
            return False
        if not self.testPatternSETListEquality(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testPatternSETListEquality(self.getEtas(), other.getEtas()):
            return False
        if not self.testPatternSETListEquality(self.getTensors(), other.getTensors()):
            return False
        if not self.testPatternSETListEquality(self.getVariations(), other.getVariations()):
            return False
        if not self.testPatternSETListEquality(self.getPartials(), other.getPartials()):
            return False
        return True

    def patternEqIncludesH(self, other):
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        if not repr(other.getSymbolCo()) in repr(self.getSymbolCo()):
            return False
        if (other.getTensorCos() != TensorCoefficients([Coefficient()])) and (other.getTensorCos() != self.getTensorCos()):
            return False
        if not self.testPatternSETListEqualityH(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testPatternSETListEqualityH(self.getEtas(), other.getEtas()):
            return False
        if not self.testPatternSETListEqualityH(self.getTensors(), other.getTensors()):
            return False
        if not self.testPatternSETListEqualityH(self.getVariations(), other.getVariations()):
            return False
        if not self.testPatternSETListEqualityH(self.getPartials(), other.getPartials()):
            return False
        return True
    ##
    # getEqualIndices creates a list of all the indices in the MultGroup object which are equal to an input index
    # @param index the input index to check equality against
    # @return the list of the equal indices
    #
    def getEqualIndices(self, index):
        pointer = list()
        for t in self.getTensors():
            pointer += t.getEqualIndices(index)
        for v in self.getVariations():
            pointer += v.getEqualIndices(index)
        for p in self.getPartials():
            if p.getIndex().basicEquals(index):
                pointer.append(p.getIndex())
        for delt in self.getDeltas():
            for dind in delt.getIndices():
                if dind.basicEquals(index):
                    pointer.append(dind)
        for et in self.getEtas():
            for eind in et.getIndices():
                if eind.basicEquals(index):
                    pointer.append(eind)
        return pointer

    def getEqualIndicesH(self, index):
        pointer = list()
        for t in self.getTensors():
            pointer += t.getEqualIndicesH(index)
        for v in self.getVariations():
            pointer += v.getEqualIndicesH(index)
        for p in self.getPartials():
            if p.getIndex().basicEqualsH(index):
                pointer.append(p.getIndex())
        for delt in self.getDeltas():
            for dind in delt.getIndices():
                if dind.basicEqualsH(index):
                    pointer.append(dind)
        for et in self.getEtas():
            for eind in et.getIndices():
                if eind.basicEqualsH(index):
                    pointer.append(eind)
        return pointer
    ##
    # findTensor returns a pointer to a tensor in the MultGroup object, if the MultGroup contains that tensor
    # @param tensor the tensor to be searched for
    # @return a reference to the tensor, if found, otherwise None
    #
    def findTensor(self, tensor):
        i = len(self.tensors)-1
        while i >= 0:
        #for ten in self.tensors:
            ten = copy.deepcopy(self.tensors[i])
            ten.setSums()
            #reinMult = MultGroup("+")
            #reinMult.addTensors(ten2)
            if ten.patternEqNotAllPs(tensor):
                return self.tensors[i]
            i += -1
        return None

    ##
    # findVariation returns a pointer to a variation in the MultGroup object, if the MultGroup contains that variation
    # @param variation the variation to be searched for
    # @return a reference to the variation, if found, otherwise None
    #
    def findVariation(self, variation):
        numDer = len(variation.getPartials())
        i = len(self.variations) - 1
        #for var in self.variations:
        while i >= 0:
            var = self.variations[i]
            var2 = copy.deepcopy(var)
            reinMult = MultGroup("+")
            reinMult.addVariations(var2)
            varNew = reinMult.getVariations()[0]
            if varNew.patternEqH(variation):
                return var
            else:
                if len(var.getPartials()) >= numDer:
                    varNewP = copy.deepcopy(varNew.getPartials())
                    variationP = copy.deepcopy(variation.getPartials())
                    allIn = True
                    for pNew in varNewP:
                        found = False
                        for p in variationP:
                            if pNew.patternEqH(p) and not found:
                                variationP.remove(p)
                                found = True
                        if not found:
                            allIn = False
                    if allIn:
                        variation2 = copy.deepcopy(variation)
                        variation2.setPartials([])
                        var2 = copy.deepcopy(var)
                        var2.setPartials([])
                        if var2.patternEqH(variation2):
                            return var
            i += -1
        return None

    ##
    # includes tests if the MultGroup object includes (exaclty, not as patterns) another MultGroup object
    # @param other the object to check if included
    # @ return boolean True or False
    #
    def includes(self, other):
        copyList = copy.deepcopy(self.getTensors())
        for el in copyList:
            el.setSums()
        for tensor in other.getTensors():
            copyTen = copy.deepcopy(tensor)
            copyTen.setSums()
            if copyTen not in copyList:
                return False
        copyList = copy.deepcopy(self.getVariations())
        for el in copyList:
            el.setSums()
        for var in other.getVariations():
            copyVar = copy.deepcopy(var)
            copyVar.setSums()
            if copyVar not in copyList:
                return False
        for eta in other.getEtas():
            if eta not in self.getEtas():
                return False
        for delt in other.getDeltas():
            if delt not in self.getDeltas():
                return False
        for partial in other.getPartials():
            if partial not in self.getPartials():
                return False
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        if not repr(other.getSymbolCo()) in repr(self.getSymbolCo()):
            return False
        if (other.getTensorCos() != TensorCoefficients([Coefficient()])) and (other.getTensorCos() != self.getTensorCos()):
            return False
        return True

    ##
    # remove term will remove a portion of the MultGroup object, if the MultGroup object contains that portion
    # @param other the portion to be removed (a MultGroup object)
    #
    def removeTerm(self, other):
        if not self.includes(other):
            return
        for tensor in other.getTensors():
            self.removeTensor(tensor)
        for var in other.getVariations():
            self.removeVar(var)
        for eta in other.getEtas():
            self.removeEta(eta)
        for delta in other.getDeltas():
            self.removeDelta(delta)
        for partial in other.getPartials():
            self.removePartial(partial)
        self.setNumCo(copy.deepcopy(self.getNumCo())/copy.deepcopy(other.getNumCo()))
        self.setSymCo(copy.deepcopy(self.getSymbolCo())/copy.deepcopy(other.getSymbolCo()))
        if other.getTensorCos() != TensorCoefficients([Coefficient()]):
            self.setTensorCos(TensorCoefficients([Coefficient()]))
        self.setSums(True)

    ##
    # isOnlyNum checks if the MultGroup contains only a numerical coefficient
    # @return boolean True or False
    def isOnlyNum(self):
        if (len(self.tensors) == 0) and (len(self.variations) == 0) and (len(self.etas) == 0) and (len(self.deltas) == 0) and (len(self.partials) == 0) and (self.tensorCos == TensorCoefficients([Coefficient()])) and (self.symbolCo == SymbolCo()):
            return True
        else:
            return False
    ##
    # factorNumCoFromTensorCo factors any numerical common factors from the tensorCo to numCo instance variables
    #
    def factorNumFromTensorCo(self):
        numbers = list()
        for el in self.getTensorCos().getCos():
            numbers.append(el.getNumCo())
        check = min(numbers)
        div = True
        for num in numbers:
            if num % check != Fraction(0):
                div = False
        if not div:
            if check.getDen() == 1:
                while (check > Fraction(1)) and not div:
                    check = check - 1
                    div2 = True
                    for num in numbers:
                        if num % check != 0:
                            div2 = False
                    if div2:
                        div = True
        if div:
            for co in self.getTensorCos().getCos():
                co.setNumCo(co.getNumCo()/check)
            self.numCo = self.numCo*check

    ##
    # factorSymFromTensorCo moves any symbol coefficients which are factorable from the tensorCo to the symbolCo  instance variable
    #
    def factorSymFromTensorCo(self):
        if len(self.getTensorCos().getCos()) > 0:
            sym = self.getTensorCos().getCos()[0].getSymCo()
            same = True
            for co in self.getTensorCos().getCos():
                if co.getSymCo() != sym:
                    same = False
            if same:
                for co in self.getTensorCos().getCos():
                    co.setSymCo(SymbolCo())
                self.symbolCo = self.symbolCo*sym

    def getSortedIndicesList(self):
        indsList = list()
        for eta in self.getEtas():
            indsList.append(eta.getIndices())
        for delta in self.getDeltas():
            indsList.append(delta.getIndices())
        for partial in self.getPartials():
            indsList.append([partial.getIndex()])
        for el in indsList:
            el = sorted(el)
        for tensor in self.getTensors():
            indsList.append(tensor.getFullIndices())
        for variation in self.getVariations():
            indsList.append(variation.getFullIndices())
        indsList = sorted(indsList)
        retList = list()
        for el in indsList:
            for el2 in el:
                retList.append(el2)
        return retList

    def changeIndicesMult(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesList(fromMultList, toMultList)

    def changeIndicesMultHNOSUMS(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesListHNOSUMS(fromMultList, toMultList)

    def changeIndicesMultH(self, fromMult, toMult):
        fromMultList = fromMult.getSortedIndicesList()
        toMultList = toMult.getSortedIndicesList()
        self.changeIndicesListH(fromMultList, toMultList)


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
        self.setSums(True)

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
        self.setSums(True)

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
        self.setSums(True)

    def __truediv__(self, other):
        if not self.includes(other):
            return
        ans = copy.deepcopy(self)
        for tensor in other.getTensors():
            ans.removeTensor(tensor)
        for var in other.getVariations():
            ans.removeVar(var)
        for eta in other.getEtas():
            ans.removeEta(eta)
        for delta in other.getDeltas():
            ans.removeDelta(delta)
        for partial in other.getPartials():
            ans.removePartial(partial)
        ans.setNumCo(ans.getNumCo()/other.getNumCo())
        ans.setSymCo(ans.getSymbolCo()/other.getSymbolCo())
        if other.getTensorCos() != TensorCoefficients([Coefficient()]):
            ans.setTensorCos(TensorCoefficients([Coefficient()]))
        if ans.getSign() != other.getSign():
            ans.changeSign("-")
        else:
            ans.changeSign("+")
        return ans

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
    ##
    # equals method tests for exact equality
    # @param other the MultGroup you're testing against
    # @return boolean True or False
    #
    def __eq__(self, other):
        self.factorSymFromTensorCo()
        other.factorSymFromTensorCo()
        self.factorNumFromTensorCo()
        other.factorNumFromTensorCo()
        if not self.sign == other.getSign():
            return False
        if not self.numCo == other.getNumCo():
            return False
        if not self.getSymbolCo() == other.getSymbolCo():
            return False
        if not self.getTensorCos() == other.getTensorCos():
            return False
        if not self.testSETListEquality(self.getDeltas(), other.getDeltas()):
            return False
        if not self.testSETListEquality(self.getEtas(), other.getEtas()):
            return False
        if not self.testSETListEquality(self.getTensors(), other.getTensors()):
            return False
        if not self.testSETListEquality(self.getVariations(), other.getVariations()):
            return False
        if not self.testSETListEquality(self.getPartials(), other.getPartials()):
            return False
        return True

    ##
    # repr returns a string representation of the MultGroup, in LaTeX syntex
    # if sign is set to false, it only adds the sign if it's a negative (to deal with leading negatives)
    # @return the string representation
    #
    def __repr__(self):
        strx = ""
        if self.showSign:
            strx += self.sign
        elif self.sign == "-":
            strx += self.sign
        if (self.numCo != Fraction(1)) or (self.isOnlyNum() and self.showNum):
            strx += repr(self.numCo) + " "
        if self.symbolCo != SymbolCo():
            strx += repr(self.symbolCo) + " "
        strx += repr(self.tensorCos) + " "
        for el in self.deltas:
            strx += repr(el) + " "
        for el in self.etas:
            strx += repr(el) + " "
        for el in self.tensors:
            strx += repr(el) + " "
        for el in self.variations:
            strx += repr(el) + " "
        for el in self.partials:
            strx += repr(el) + " "
        return strx
