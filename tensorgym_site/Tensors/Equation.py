from Tensors.SymmetryProperties import SymmetryProperties
from Tensors.IndexException import IndexException
from Tensors.SymbolCo import SymbolCo
from Tensors.Fraction import Fraction
from Tensors.Delta import Delta
from Tensors.Eta import Eta
from Tensors.Index import Index
from Tensors.Partial import Partial
from Tensors.Tensor import Tensor
from Tensors.Variation import Variation
from Tensors.MultGroup import MultGroup
from Tensors.Summation import Summation
from Tensors.EquationTree import EquationTree
from Tensors.EquationNode import EquationNode
from Tensors.Sign import Sign
import copy
class Equation:
    ##
    # creates an equation from an input latex style equation
    # @param latex the RHS of a latex equation: must be a full equation with closing brackets for each opening, etc
    #
    def __init__(self, latex, symTens=''):
        self.delims = [" ", "\\", "}",")","]", "{", "(", "[", "^", "_"]  # indicate places which latex might see as a break
        self.latex = ' '.join(latex.split())  # give max one space - no more is needed
        self.eqIndicator = False
        self.cov = False
        if ("\\begin{multline}" in self.latex) and ("\\end{multline}" in self.latex):
            self.eqIndicator = True
            self.latex = self.latex.replace("\\begin{multline}", "")
            self.latex = self.latex.replace("\\end{multline}", "")
        if ("\\begin{equation}" in self.latex) and ("\\end{equation}" in self.latex):
            self.eqIndicator = True
            self.latex = self.latex.replace("\\begin{equation}", "")
            self.latex = self.latex.replace("\\end{equation}", "")
        if ("\\nabla_" in self.latex) or ("\\nabla^" in self.latex) or ("\\nabla _" in self.latex) or ("\\nabla ^" in self.latex):
            self.cov = True
        sides = self.latex.split("=")
        self.lhs = ""
        if len(sides) > 1:
            self.lhs = sides[0] + "="
            sides.pop(0)
            self.latex = ''.join(sides)
        self.latex = ' '.join(self.latex.split("\\\\"))  # remove any multline line delimiters - they will be re-added in repr
        self.latex = ' '.join(self.latex.split())
        symTens = ''.join(symTens.split())
        self.symTens = symTens.split(",")
        self.tree = EquationTree(self.createExpTree(self.latex))  # store the equation in the form of a binary equation tree
        self.tree.setEqIndicator(self.eqIndicator)

    def getDel(self):
        return self.delims

    def getCov(self):
        return self.cov

    def setEqIndicator(self, newInd):
        self.eqIndicator = newInd
        self.tree.setEqIndicator(self.eqIndicator)

    def __repr__(self):
        strx = repr(self.tree)
        if strx.startswith("\\begin{equation}"):
            strx = "\\begin{equation}" + self.lhs + strx.replace("\\begin{equation}", "")
        elif strx.startswith("\\begin{multline}"):
            strx = "\\begin{multline}" + self.lhs + strx.replace("\\begin{multline}", "")
        return strx


    def getTree(self):
        return self.tree
    ##
    # createExpTree creates a binary expression tree which holds summation objects as leaves and algebraic symbols as non-leaf nodes
    # RECURSIVE
    # @param right string that is dealt with as right leaf, or as root if left is None
    # @param left string that is dealt with as left leaf unless None
    # @param sign a string which is dealt with as root (Sign object) unless None
    # at return the ROOT of an expression tree containing the right and left nodes (and any children they have)
    #
    def createExpTree(self, right, brac = False, left=None, sign=None):
        summationSign = "+"
        # deal with right
        if self.additionBetweenBrackets(right):  # check if bracket sets are added (ie +/- outside closed brackets)
            plPos = self.findAddBetweenBrackets(right)  # the position of the FIRST +/- b/w brackets in right
            summationSign = right[plPos]  # + or -
            subSign = "+"
            if summationSign == "-":
                l = right[plPos:]
            else:
                l = right[plPos+1: len(right)]  # what comes after the +/-
            r = right[0:plPos]  # what comes before the +/-
            l = ' '.join(l.split())
            r = ' '.join(r.split())
            rightNode = self.createExpTree(r, False, l, subSign)  # recursive call to deal with info in r and l
        elif self.multBetweenBrackets(right):  # check if bracket sets are multiplied
            m2Pos = self.findMultBetweenBrackets(right)  # position of "\\" of the "\\(" after FIRST multiplication between brackets
            subSign = "*"
            r = right[0:m2Pos]  # what comes before the multiplication
            l = right[m2Pos: len(right)]  # what comes after the multiplication
            l = ' '.join(l.split())
            r = ' '.join(r.split())
            rightNode = self.createExpTree(r, False, l, subSign)  # recursive call to deal with info in r and l
        elif self.inBrackets(right):  # check if right is surrounded by multbrackets
            r = self.removeBrackets(right)  # remove outside brackets
            l = None
            subSign = None
            r = ' '.join(r.split())
            rightNode = self.createExpTree(r, True)  # recursive call to deal with info in r
        else:  # BASE CASE: no recursive call
            rightNode = EquationNode(self.dealWithSummation(right, brac))  # create an equation node out of summation object with info from right
        # deal with left
        if left is None and sign is None:
            rightNode.setBrackets(brac)
            return rightNode  # use rightNode as the root of the equation tree
        if self.additionBetweenBrackets(left):  # check if bracket sets are added (ie +/- outside closed brackets)
            plPos = self.findAddBetweenBrackets(left)  # the position of the FIRST +/- b/w brackets in left
            summationSign = left[plPos]  # + or -
            subSign = "+"
            r = left[0:plPos]  # what comes before the +/-
            if summationSign == "-":
                l = left[plPos:]
            else:
                l = left[plPos + 1: len(left)]  # what comes after the +/-
            l = ' '.join(l.split())
            r = ' '.join(r.split())
            leftNode = self.createExpTree(r, False, l, subSign)  # recursive call to deal with info in r and l
        elif self.multBetweenBrackets(left):  # check if bracket sets are multiplied
            m2Pos = self.findMultBetweenBrackets(left)  # position of "\\" of the "\\(" after FIRST multiplication between brackets
            subSign = "*"
            r = left[0:m2Pos]  # what comes before the multiplication
            l = left[m2Pos: len(left)]  # what comes after the multiplication
            l = ' '.join(l.split())
            r = ' '.join(r.split())
            leftNode = self.createExpTree(r, False, l, subSign)  # recursive call to deal with info in r and l
        elif self.inBrackets(left):  # check if right is surrounded by multbrackets
            r = self.removeBrackets(left)  # remove outside brackets
            r = ' '.join(r.split())
            leftNode = self.createExpTree(r, True)  # recursive call to deal with info in r
        else:  # BASE CASE: no recursive call
            leftNode = EquationNode(self.dealWithSummation(left, brac))  # create an equation node out of summation object with info from left
        # create tree
        root = EquationNode(Sign(sign), brac)  # only called if left not None
        root.setRight(rightNode)  # can be leaf or have children
        root.setLeft(leftNode)  # can be leaf or have children
        #return
        return root  # return the ROOT (so can act as child node later, or accessor for tree)
    ##
    # dealWithSummation takes in latex with info for one summation object and interprets it
    # @param strx a string which is just one summation
    # @return a Summation object from the string
    #
    def dealWithSummation(self, strx, brac = False, signage = "+"):
        sign = signage
        sums = Summation()
        sums.setBrackets(brac)
        while strx.startswith(" "):  # remove any leading spaces
            strx = strx[1:]
        while strx.endswith(" "):
            strx = strx[:len(strx)-1]
        if strx == "-":  # deal with case where summation object is just negative sign
            negSum = [MultGroup("-")]
            return Summation(negSum)
        if strx.startswith("-\\(") or strx.startswith("-\\partial") or strx.startswith("-\\square"):
            sign = "-"
            strx = strx[1:]
        elif strx.startswith("- \\(") or strx.startswith("- \\partial") or strx.startswith("- \\square"):
            sign = "-"
            strx = strx[2:]
        sums.changeSign(sign)
        while strx.startswith(" "):
            strx = strx[1:]
        #add any preceding partials
        camryn = 's'
        while (strx.startswith("\\partial") or strx.startswith("\\square")) and "\\(" in strx:
            sums.setBrackets(True)  # if there are preceding partials, must have brackets
            if strx.startswith("\\square"):
                strx = strx.replace("\\square", "", 1)
                sums.addPartials(Partial(Index("\\square" + camryn, 0)))
                sums.addPartials(Partial(Index("\\square" + camryn, 1)))
                camryn = camryn + "s"
            else:
                sums.addPartials(self.dealWithPartial(strx, 0)[0])
                strx = strx.replace(strx[0:self.dealWithPartial(strx, 0)[1]+1], "", 1)  # replace at most once
            while strx.startswith(" "):  # remove any initial spaces
                strx = strx[1:]
        if strx.startswith("\\(") and strx.endswith("\\)"):  # check if there are brackets
            strx = strx[2:len(strx)-2]  # remove brackets
            sums.setBrackets(True)  # define object to be printed with brackets
        elif strx.startswith("\\(") or strx.endswith("\\)"):
            raise TypeError  # brackets must match
        # break into chucks of information containing multgroups
        g1 = g2 = 0
        parts = list()
        done = False
        while not done:
            while g2 < (len(strx)-1) and strx[g2] != "+" and strx[g2] != "-":
                g2 = self.skipBrackets(strx, g2)  # don't check for +/- inside brackets
                g2 += 1
            if g2 == len(strx) - 1:  # end case (from loop), no +/- but still have to add
                parts.append(strx[g1:g2+1])
                done = True
            if g2 == len(strx):  # end case (from finish brac), no +/- but still have to add
                parts.append(strx[g1:g2])
                done = True
            elif strx[g2] == "+" or strx[g2] == "-":
                parts.append(strx[g1:g2])
                g1 = g2  # position of the +/-
                g2 += 1  # move past so loop can continue
        for el in parts:
            if not (el == " " or el == ""):
                mult = self.dealWithMultGroup(el)
                sums.addTerm(mult)
        return sums

    ##
    # dealWithMultGroup takes in information in a string and picks it apart to create a Multgroup object
    # @param strx the string with the information
    # @return a Multgroup object containing the same information
    #
    def dealWithMultGroup(self, strx):
        cassiopea = 1
        while strx.startswith(" "):# remove any leading spaces
            strx = strx[1:]
        while strx.endswith(" "):
            strx = strx[: len(strx)-1]
        if len(strx) > 0 and strx[0] == "-":
            sign = "-"  # deal with sign
            strx = strx.replace("-", "", 1)
        else:
            sign = "+"  # default is plus, even if no sign (for first terms)
        if len(strx) > 0 and strx.startswith("+"):
            strx = strx.replace("+", "", 1)
        while strx.startswith(" "):# remove any leading spaces
            strx = strx[1:]
            if strx.startswith("\\(") and strx.endswith("\\)"):
                strx = strx[2:len(strx)-2]  # remove multbrackets
        # **************************************************************
        # deal with command coefficients
        symCos = SymbolCo()
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        while "\\coeff" in strx:
            initPos = pos = strx.find("\\coeff")
            while pos < len(strx) and strx[pos] != "{":
                pos += 1
            if pos == len(strx):
                raise TypeError("the coefficient command must have an arguement")
            endPos = self.finishBracketSet(strx, pos, "{", "}")
            coeff = strx[pos+1: endPos]  # the part inside the brackets
            strx = strx[:initPos] + strx[endPos+1:]
            symCos = symCos * SymbolCo(coeff, True)
            strx = ' '.join(strx.split())  # reinitialize max one space condition
        # **************************************************************
        # deal with variations
        variations = list()
        if "\\frac" in strx:
            pos = strx.find("\\frac")
            while self.hasTensorFrac(strx):  # while there are tensor fractions, keep going
                brac = self.movePastSpace(strx, pos + 5)  # get to first information index after end of \\frac
                if strx[brac] != "{":
                    pos = strx.find("\\frac", brac)  # pos is position of the first TENSOR \\frac
                elif ''.join(strx[brac+1: self.finishBracketSet(strx, brac, "{", "}")].split()).isnumeric():  # if not tensor, move past
                    pos = strx.find("\\frac", brac)
                else:
                    end = self.movePastSpace(strx, self.finishBracketSet(strx, brac, "{", "}")+1)
                    end = self.movePastSpace(strx, self.finishBracketSet(strx, end, "{", "}")+1)  # get to the end of both sets of brackets in \\frac{}{}
                    # end is the first meaningful index AFTER }
                    if end <= len(strx) - 1:
                        if strx[end:end+2] == "\\)":  # check if surrounded by brackets
                            end += 2
                    if pos >= 2 and strx[pos-2:pos] == "\\(":
                        pos += -2
                    partialInds = self.getPrecedingDerivativesPos(strx, pos)
                    if partialInds[0] != partialInds[1]:
                        initial = partialInds[0]
                    else:
                        initial = pos
                    variations.append(self.dealWithTensorFrac(strx[initial: end]))  # feed variation information to var method
                    strx = strx.replace(strx[initial: end], "", 1)
        # **************************************************************
        # deal with any numerical fractions
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        numCos = Fraction(1)
        while "\\frac" in strx:
            first = strx.find("\\frac")
            past = self.movePastSpace(strx, first+5)
            if strx[past] == "{":# check if bracket fraction or two num frac
                last = self.finishBracketSet(strx, self.movePastSpace(strx, self.finishBracketSet(strx, first+past, "{", "}") + 1), "{", "}")
            else:
                last = past+1  # position of denominator in a fraction without {}
            frac = strx[first:last+1]
            strx = strx.replace(frac, "", 1)
            co = self.dealWithFrac(frac)
            numCos = numCos*co
        # **************************************************************
        # deal with any other numerical coefficients
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        char = 0
        while char < len(strx):
            if strx[char].isnumeric():
                if (char == 0) or (char >= 1 and (not strx[char-1] == "_") and (not strx[char-1] == "^") and (not self.isSurroundedByCurly(strx, char))):
                    first = char
                    while char < len(strx) and strx[char].isnumeric():
                        char += 1
                    last = char  # is first index AFTER end of numeric
                    num = strx[first: last]
                    strx = strx.replace(num, "", 1)
                    char = 0
                    numCos = numCos * Fraction(int(num))
                else:
                    char += 1
            else:
                char += 1
        # **************************************************************
        # deal with deltas
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        deltas = list()
        while "\\delta" in strx:
            beg = strx.find("\\delta")
            indices = self.dealWithTensorIndex(strx, self.movePastSpace(strx, beg+6))[0]
            endDel = self.dealWithTensorIndex(strx, self.movePastSpace(strx, beg+6))[1]
            deltas.append(Delta(SymmetryProperties(indices)))
            strx = strx[:beg] + strx[endDel:]
        # **************************************************************
        # deal with etas
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        etas = list()
        while "\\eta" in strx:
            beg = strx.find("\\eta")
            indices = self.dealWithTensorIndex(strx, self.movePastSpace(strx, beg+4))[0]
            endEta = self.dealWithTensorIndex(strx, self.movePastSpace(strx, beg+4))[1]
            etas.append(Eta(SymmetryProperties(indices)))
            strx = strx[:beg] + strx[endEta:]

        # **************************************************************
        # deal with tensors
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        tensors = list()
        place = 0
        while ("_" in strx[place:]) or ("^" in strx[place:]):
            strx = ' '.join(strx.split())  # reinitialize max one space condition
            down = strx.find("_", place)
            up = strx.find("^", place)
            if up < 0:
                pos = down
            elif (down >= 0) and (down < up):
                    pos = down
            else:
                pos = up
            # pos is index of beginning of FIRST index set in strx
            if (strx[:pos].endswith("\\partial")) or (strx[:pos].endswith("\\partial ")):  # if the ^/_ is attached to a partial, keep searching
                place = pos+1  # if index set does not belong to a tensor, keep searching
            else:  # FIRST tensor has been found
                endTensor = self.dealWithTensorIndex(strx, pos)[1]  # first index after end of indices
                indices = self.dealWithTensorIndex(strx, pos)[0]
                endSymb = pos  # first index after the tensor symbol
                if strx[endSymb-1] == " ":  # move back if space
                    endSymb += -1
                test = endSymb - 1
                while test >= 0 and not(strx[test] in self.getDel()):
                    test += -1
                if strx[test] == "\\":  # if we first ran into \\, from test to endSymb must all be tensor symbol
                    begSymb = test  # first index of tensor symbol
                else:
                    begSymb = endSymb - 1  # if not \\, assume tensor Symbol is only one character
                tensorSymbol = strx[begSymb:endSymb]  # save the symbol part of the tensor
                strx = strx[0:begSymb] + strx[endTensor:len(strx)]  # cut both symbol and indices from strx
                partialsT = list()  # holds and partial objects attached to the tensor
                # TREAT ANY PARTIAL PRECEDING A TENSOR AS ATTACHED TO THAT TENSOR
                while "\\partial" in strx[:begSymb]:
                    firstP = strx.find("\\partial")  # the index of the first partial attached to the tensor
                    partialsT.append(self.dealWithPartial(strx, firstP)[0])
                    lastP = self.dealWithPartial(strx, firstP)[1]+1
                    strx = strx[:firstP] + strx[lastP:]  # remove partial information
                    subtracted = lastP - firstP  # the length that has been removed from strx
                    begSymb += -subtracted  # decrease begSymb so it still references the same (information) position in strx
                while "\\square" in strx[:begSymb]:
                    strx = strx.replace("\\square", "", 1)
                    partialsT.append(Partial(Index("\\square" + str(cassiopea), 0)))
                    partialsT.append(Partial(Index("\\square" + str(cassiopea), 1)))
                    cassiopea += 1
                    begSymb += -len("\\square")
                tensors.append(Tensor(tensorSymbol, SymmetryProperties(indices), partialsT, "+", False, self.symTens))
                place = begSymb
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        strx = strx.replace("\\(\\)", "")  # get rid of any empty brackets
        strx = strx.replace("\\( \\)", "")

        # **************************************************************
        # deal with OUTER PARTIALS (ie any partials that are left)
        partials = list()
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        while "\\partial" in strx:
            ps = strx.find("\\partial")
            pm = self.movePastSpace(strx, self.dealWithPartial(strx, ps)[1]+1)  # first important index after last index of the partial
            while strx[pm:].startswith("\\partial"):
                pm = self.movePastSpace(strx, self.dealWithPartial(strx, pm)[1]+1)  # first important index after last index of the partial
            opartials = self.dealWithPartialList(strx[ps:pm])
            strx = strx[:ps] + strx[pm:]
            for el in opartials:
                partials.append(el)
        while "\\square" in strx:
            strx = strx.replace("\\square", "", 1)
            partials.append(Partial(Index("\\square" + str(cassiopea), 0)))
            partials.append(Partial(Index("\\square" + str(cassiopea), 1)))
            cassiopea += 1
        # **************************************************************
        # deal with anything that's left
        strx = ' '.join(strx.split())  # reinitialize max one space condition
        if strx.startswith(" "):
            strx = strx[1:]
        if len(strx) > 0:
            symCos = symCos * SymbolCo(strx)
        return MultGroup(sign, numCos, symCos, tensors, variations, etas, deltas, partials)

    # BRACKET HELPER METHODS

    ##
    # helper method: find matching closing bracket position given opening position!!!
    # @param strx whats left of latex string
    # @param first the index of the opening bracket
    # @param openB the type of opening bracket (ie (,[,{...)
    # @param closeB the type of closing bracket (ie ),],}...)
    # @return the index of the last bracket
    #
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
                if len(brackets) == 0:  # makes sure it is not the first closing bracket, but the closing bracket that matches the opening one
                    done = True
                else:
                    char += 1
            else:
                char += 1
        last = char
        return last
    ##
    # helper method: find matching OPENING bracket position given CLOSING position!!!
    # @param strx whats left of latex string
    # @param last the index of the closing bracket
    # @param closeB the type of closing bracket (ie ),],}...)
    # @param openB the type of opening bracket (ie (,[,{...)
    # @return the index of the first bracket
    #
    def backFinishBracket(self, strx, last, closeB, openB):
        char = last
        if last > 0:
            done = False
        else:
            done = True
        brackets = list()
        while not done and last > 0:
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
        first = char
        return first
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
    ##
    # isSurroundedByCurly helper method that check if a certain index in a string is surrounded by curly brackets {}
    # @param strx the string that contains the index
    # @param place the index to be checked
    # @return boolean True or False
    #
    def isSurroundedByCurly(self, strx, place):
        last = strx.find("}", place)  # find the first instance of a closing bracket AFTER index
        if last == -1:  # not found
            return False
        first = self.backFinishBracket(strx, last, "{", "}")
        if first < place:
            return True
        else:
            return False

    # OTHER SIMPLE IMPORTANT HELPER METHODS

    ##
    # movePastSpace helper method that finds index after whitespace
    # @param strx the string we're moving in
    # @param pos the index that might contain whitespace
    # @return the first index following the whitespace (if there was whitespace, else the initial index)
    #
    def movePastSpace(self, strx, pos):
        while (pos < len(strx)) and (strx[pos] == " "):
            pos += 1
        return pos

    # HELPER METHODS FOR CREATE EXPRESSION TREE

    ##
    # additionBetweenBrackets checks if there is a +/- sign outside closed brackets (excepting leading negatives)
    # @param strx the string to check for add in
    # @return boolean True or False
    #
    def additionBetweenBrackets(self, strx):
        if not "\\(" in strx:
            return False
        if strx.startswith(" "):
            strx = strx[1: len(strx)]
        if strx.endswith(" "):
            strx = strx[0: len(strx)-1]
        if strx.startswith("-"):  # deal with leading negatives - which are NOT add b/w brackets
            strx = strx[1: len(strx)]
        i = strx.find("\\(")  # check if any summation before first bracket
        pm = i  # plus or minus position
        while pm >= 0 and strx[pm] != "+" and strx[pm] != "-":
            pm += -1
            pm = self.skipBrackets(strx, pm, "-")
        if pm != -1:  # must be +/-
            return True
        i = self.finishBracketSet(strx, i+1, "(", ")")  # if no +/- before first bracket set, check after
        while i < len(strx) and strx[i] != "-" and strx[i] != "+":  # move until end, find +/- or next bracket set
            i = self.skipBrackets(strx, i)
            i += 1
        if i == len(strx):
            return False
        else:
            return True

    ##
    # assuming there IS a b/w bracs +/-, find it's position
    # @param strx the string we're searching in
    # @return the position of the +/-
    #
    def findAddBetweenBrackets(self, strx):
        i = self.movePastSpace(strx, 0)
        if strx[i] == "-":  # ignore leading -
            i += 1
        i = self.movePastSpace(strx, i)
        if not strx[i:i+2] == "\\(":  # check if any summation before first bracket
            b = strx.find("\\(")
            pm = b  # pm will be the position of the +/-
            while pm >= i and strx[pm] != "+" and strx[pm] != "-":
                pm += -1
                pm = self.skipBrackets(strx, pm, "-")  # going left
            if pm != i-1:  # must be +/-
                return pm
        i = self.finishBracketSet(strx, i+1, "(", ")")  # check for summation after brackets
        done = False
        while not done:
            while i < len(strx) and strx[i] != "-" and strx[i] != "+":
                i = self.skipBrackets(strx, i)
                i += 1
            if i == len(strx):  # indicates problem, can be dealt with elsewhere
                return -1
            else:
                return i

    ##
    # multBetweenBrackets checks if bracket sets multiply with eachother
    # @param strx the string we're checking for this in
    # @return boolean True or False
    #
    def multBetweenBrackets(self, strx):
        if "\\(" not in strx or "\\)" not in strx:
            return False
        while strx.startswith(" "):
            strx = strx[1: len(strx)]
        while strx.endswith(" "):
            strx = strx[:len(strx)-1]
        #if strx.startswith("-"):  # treat leading negatives as a multgroup multiplying with brackets
        #    return True
        if strx.startswith("\\(") and strx.endswith("\\)") and ("\\(" not in strx[2:len(strx)-2]):
            return False
        if strx.startswith("\\("):
            i = self.finishBracketSet(strx, 1, "(", ")")  # move past brackets
            if i+1 == len(strx) or (i+1 < len(strx) and strx[i+1] == " " and i+2 == len(strx)):
                return False
            else:  # if there is anything after the brackets, it must be multiplied, since this is checked AFTER removing any +/- b/w brackets
                return True
        else:  # if has brackets and doesn't start with brackets, MUST be multiplied by something in front
            openBracPos = strx.find("\\(")
            closeBracPos = self.finishBracketSet(strx, openBracPos+1, "(", ")")
            if self.movePastSpace(strx, closeBracPos + 1) != len(strx):
                return True
            if "\\(" in strx[openBracPos+2:closeBracPos]:
                #if self.multBetweenBrackets(strx[openBracPos+2:closeBracPos]):
                #    return True
                return True
            derTup = self.getPrecedingDerivativesPos(strx, openBracPos)
            if derTup[0] != 0 and (derTup[0] > 1 or strx[derTup[0]-1] != "-"):
                return True
        return False

    ##
    # findMultBetweenBrackets finds first instance of brackets sets being multiplied
    # @param strx the string we're checking in
    # @return i is the index of the first character in the second multiplication set!
    #
    def findMultBetweenBrackets(self, strx):
        i = 0
        while strx[i] == " ":
            i += 1
        while strx.endswith(" "):
            strx = strx[:len(strx)-1]
        #if strx[i] == "-":
        #    i += 1
        #    return i
        if strx[i:i+2] == "\\(":  # must come after the bracket set
            i = self.finishBracketSet(strx, i+1, "(", ")") + 1  # first position after closing bracket
        else:
            while not strx[i:i+2] == "\\(":
                i += 1
            derTup = self.getPrecedingDerivativesPos(strx, i)
            j = derTup[0]
            if j > 0 and not(j == 1 and strx.startswith("-")):  # there is something multiplied before the derivatives
                i = j
            else:
                endBrack = self.finishBracketSet(strx, i+1, "(", ")")
                if endBrack < len(strx)-1:
                    i = endBrack + 1
                elif "\\(" not in strx[i+2: endBrack]:  # if no inner brackets, mult must come after
                #if not self.multBetweenBrackets(strx[i+2: endBrack]):
                    #i = self.finishBracketSet(strx, i+1, "(", ")") + 1
                    i = endBrack + 1
                #else:

                    # i = i+2 + self.findMultBetweenBrackets(strx[i+2: endBrack])
        return i

    ##
    # in Brackets helper method checks if ALL the information in a string is enclosed by mult brackets("\(, \)")
    # @param strx the string to check
    # @return boolean True or False
    #
    def inBrackets(self, strx):
        while strx.startswith(" "):
            strx = strx[1: len(strx)]
        while strx.endswith(" "):
            strx = strx[0: len(strx)-1]
        if strx.startswith("\\(") and strx.endswith("\\)"):
            return True
        else:
            return False

    ##
    # removeBrackets helper method takes in a string and removes the any outermost surrounding brackets
    # (can deal with spaces before and after brackets, but otherwise must start and end in b to be removed)
    # @param strx the string to be stripped of brackets
    # @return the string without the brackets (only if started and ended with brackets)
    #
    def removeBrackets(self, strx):
        while strx.startswith(" "):
            strx = strx[1: len(strx)]
        while strx.endswith(" "):
            strx = strx[0: len(strx)-1]
        if strx.startswith("\\(") and strx.endswith("\\)"):
            strx = strx[2:len(strx)-2]
        return strx

    # HELPER METHODS FOR MULTLINE

    ##
    # helper method: deal with numerical fractions
    # @param strx a string containing ONLY the fraction info (ie from "\\frac" to second "}" (or to end of number))
    # @return the fraction object created from strx
    #
    def dealWithFrac(self, strx):
        strx = strx.replace("\\frac", "")
        if "{" in strx:
            parts = strx.split("}{")
            num = int(parts[0].replace("{", ""))
            den = int(parts[1].replace("}", ""))
        else:  # if no { then frac only has two numbers, num and den
            num = int(strx[0])
            den = int(strx[1])
        co = Fraction(num, den)
        return co

    def hasTensor(self, strx):
        if "\\partial" in strx: return True
        if ("_" in strx) and not((strx[:strx.find("_")].endswith("\\eta")) and (strx[:strx.find("_")].endswith("\\delta"))):
            return True
        if ("^" in strx) and not((strx[:strx.find("^")].endswith("\\eta")) and (strx[:strx.find("^")].endswith("\\delta"))):
            return True
        else: return False

    ##
    # dealWithPartial helper method takes a string and position which MUST HAVE A PARTIAL starting at position and finds partial information
    # @param strx the string with the partial
    # @param start the index of the "\" in the "\partial" in strx
    # @return a TUPLE with tup[0] = Partial object, tup[1] = index of last character in partial (ie. "}" if index in brackets)
    #
    def dealWithPartial(self, strx, start):
        if "\\partial" not in strx:  # MUST CONTAIN A PARTIAL
            raise TypeError("This substring does not contain a partial derivative!!!!")
        hPlace = self.movePastSpace(strx, start + 8)  # move past "\partial" to find "^" or "_" to specify height
        if strx[hPlace] == "_":
            height = 0  # down
        elif strx[hPlace] == "^":
            height = 1  # up
        else: raise IndexException("must specify height of index (partial derivative)")
        ind = self.movePastSpace(strx, hPlace+1)
        if strx[ind] == "{":
            last = self.finishBracketSet(strx, ind, "{", "}")
            indexStr = strx[ind+1:last]  # create indexStr from what is INSIDE {}, (only contains one index for partial)
        elif strx[ind] == "\\":  # deal with case where index is command (starts with \) not enclosed in brackets {}
            last = ind+1  # move past "\" so not included in delims
            while (last < len(strx)) and (strx[last] not in self.getDel()):  # move until reach some deliminator
                last += 1
            if not last == len(strx):
                last += -1  # after delim is reached, move back one index so last is pos of last index in partial
            indexStr = strx[ind:last+1]
        else:  # deal with case where index is just one character
            last = ind
            indexStr = strx[ind:last+1]
        indexStr = ''.join(indexStr.split())
        index = Index(indexStr, height)
        return Partial(index), last

    ##
    # dealWithPartialList helper method that takes in a string and splits it up into partials
    # @param the string containing ONLY partial derivatives
    # @ return a list of Partial objects from information in string
    def dealWithPartialList(self, strx):
        strx = strx.replace(" ", "")  # don't need spaces here, since will be split
        strx = strx.replace("\\partial", "%\\partial")  # add separator character
        strxS = strx.split("%")  # split into chunks containing partial information
        partials = list()
        if len(strxS) > 0:  # if contained partials
            for el in strxS:
                if el != "" and "\\partial" in el:
                    partials.append(self.dealWithPartial(el, 0)[0])
            return partials

    ##
    #  dealWithTensorIndex helper method that takes in a string with a tensor and extracts the part containing index information
    # @param strx the string with the indices (whole string)
    # @param first the (string index) position of the FIRST "^" or "_" after the tensor symbol
    # @return TUPLE with tup[0] = substring of strx from beginning of index info (_/^) to end (eg }) and tup[1] = first index AFTER last index of tensor info
    def dealWithTensorIndex(self, strx, first):
        endTensor = first
        while endTensor < len(strx) and (strx[endTensor] == "^" or strx[endTensor] == "_"):
            endTensor = self.movePastSpace(strx, endTensor+1)
            if strx[endTensor] == "{":  # deal with case where indices are enclosed by {}
                endTensor = self.finishBracketSet(strx, endTensor, "{", "}") + 1  # end on position after } to check if "^" or "_"
            elif strx[endTensor] == "\\":  # deal with case where only one index and it is a command
                endTensor += 1
                while endTensor < len(strx) and strx[endTensor] not in self.getDel():  # move until reach a delimiter
                    endTensor += 1
            else:  # deal with case where index is just one character
                endTensor += 1
            endTensor = self.movePastSpace(strx, endTensor)
        return strx[first:endTensor], endTensor

    ##
    # dealWithTensorFrac takes in a string that contains the information for a Variation Object and outputs a Variation Object
    # @param strx the string with (just) the variation information
    # @return a variation object
    #
    def dealWithTensorFrac(self, strx):
        partials = list()
        while strx.startswith(" "):
            strx = strx[1:]
        candid = 1
        while strx.startswith("\\partial") or strx.startswith("\\square"):  # if starts with a partial, partial must be attached to variation
            if strx.startswith("\\square"):
                partials.append(Partial(Index("\\square" + str(candid), 0)))
                partials.append(Partial(Index("\\square" + str(candid), 1)))
                candid += 1
            else:
                partials.append(self.dealWithPartial(strx, 0)[0])
                strx = strx.replace(strx[:self.dealWithPartial(strx, 0)[1]+1], "", 1)  # remove that part of the string, at most once
                while strx.startswith(" "):
                    strx = strx[1:]
        if strx.startswith("\\(") and strx.endswith("\\)"):
            strx = strx[2:len(strx)-2]
            brackets = True
        else:
            brackets = False
        strx = strx.replace("\\frac", "")  # remove the frac symbol to be left just with info in {}{}
        while strx.startswith(" "):
            strx = strx[1:]
        mid = self.finishBracketSet(strx, 0, "{", "}")  # variation must be enclosed in {}
        last = self.finishBracketSet(strx, self.movePastSpace(strx, mid+1), "{", "}")
        strx = [strx[:mid], strx[self.movePastSpace(strx, mid+1):]]  # split into numerator (strx[0]) and denominator (strx[1])
        if strx[1].startswith("{"):
            strx[1] = strx[1][1:]
        if "\\partialv" in strx[0] and "\\partialv" in strx[1]:
            type = "\\partialv"
            strx[0] = strx[0].replace("\\partialv", "")
            strx[1] = strx[1].replace("\\partialv", "")
        elif "\\deltav" in strx[0] and "\\deltav" in strx[1]:
            type = "\\deltav"
            strx[0] = strx[0].replace("\\deltav", "")
            strx[1] = strx[1].replace("\\deltav", "")
        else:
            type = ""
        strx[0] = strx[0].replace("{", "", 1)  # only replace the first bracket, then left with info in num
        strx[0] = ' '.join(strx[0].split())
        if strx[0].startswith(" "):
            strx[0] = strx[0][1:]
        if strx[0].endswith(" "):
            strx[0] = strx[0][:len(strx[0])-1]
        if strx[0].startswith("(") and strx[0].endswith(")"):  # if total is enclosed by brackets (), remove them
            strx[0] = strx[0][1:len(strx[0])-1]
        strx[1] = strx[1][::-1].replace("}", "", 1)[::-1]  # remove only the LAST bracket, the left with info in den
        strx[1] = ' '.join(strx[1].split())
        if strx[1].startswith(" "):
            strx[1] = strx[1][1:]
        if strx[1].endswith(" "):
            strx[1] = strx[1][:len(strx[1])-1]
        if strx[1].startswith("(") and strx[1].endswith(")"):  # if total is enclosed by brackets (), remove them
            strx[1] = strx[1][1:len(strx[1])-1]
        top = self.dealWithSummation(strx[0])  # treat numerator and denominator as summation objects

        bottom = self.dealWithSummation(strx[1])
        return Variation(top, bottom, type, partials, "+", brackets)

    ##
    # check if a string contains and variations
    # @param strx the string to check for var in
    # @return boolean True or False
    #
    def hasTensorFrac(self, strx):
        place = 0
        while "\\frac" in strx[place:]:
            cam = strx.find("\\frac", place)  # find first instance of frac after place (so don't recheck)
            groggy = self.movePastSpace(strx, cam+5)  # len of \frac is 5
            if strx[groggy] != "{":  # cannot be a tensor fraction
                place = cam + 5  # start checking again
            elif strx[groggy+1: self.finishBracketSet(strx, groggy, "{", "}")].isnumeric():  # if it's a number, it's not a tensor
                place = cam + 5  # start checking again
            else: return True
        return False

    ##
    # determines if the whole of strx (ie MORE THAN ONE TENSOR) has a derivative or more (OUT FRONT OF MULTBRACKETS)
    # @param strx the string to check for derivatives in
    # @return boolean True or False
    #
    def hasDerivatives(self, strx):
        if "\\(" not in strx:  # der must be outside multbrackets
            return False
        if ("\\partial" not in strx) and ("\\square" not in strx):  # only checking for partial derivatives
            return False
        pos = self.movePastSpace(strx, 0)
        while strx[pos:].startswith("\\partial") or strx[pos:].startswith("\\square"):  # move past all partials
            if strx.startswith("\\square"):
                pos += 7
            else:
                pos = self.dealWithPartial(strx, pos)[1]
            pos = self.movePastSpace(strx, pos)
        if strx[pos:].startswith("\\("):
            return True
        else:
            return False

    ##
    # getPrecedingDerivativesPos helper method finds the beginning position of some number of preceding derivatives
    # @param strx the string which contains the object and derivatives
    # @param first the position of beginning of object with preceding derivatives: ie either symbol or "\\("
    # @return tuple where tup[0] = position of "\" in "\partial" of first preceding derivative and tup[1] = position after last index of derivatives
    #
    def getPrecedingDerivativesPos(self, strx, first):
        if not (first > 2 and ("\\partial" in strx[:first] or "\\square" in strx[:first])):
            return first, first
        else:
            last = first
            first += -7  # move back to first place that partial could potentially occur
            while first >= 0 and not (strx[first:first+8] == "\\partial" or strx[first:first+7] == "\\square"):  # move back until find closest partial
                first += -1
            if first == -1:
                return last, last
            if strx[first:].startswith("\\square"):
                end = self.movePastSpace(strx, first+7)
            else:
                end = self.movePastSpace(strx, self.dealWithPartial(strx, first)[1] + 1)
            if not end == last:  # partial was not right before!
                return last, last
            tup = self.getPrecedingDerivativesPos(strx, first)
            while not tup[0] == tup[1]:
            #while not self.getPrecedingDerivativesPos(strx, first)[0] == self.getPrecedingDerivativesPos(strx, first)[1]:
                #first = self.getPrecedingDerivativesPos(strx, first)[0]
                first = tup[0]
                tup = self.getPrecedingDerivativesPos(strx, first)
            return first, last
    ##
    # hasNumbers helper method checks if there are any numbers in the string
    # @param inputString the string to check
    # @return boolean True or False
    #
    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    # METHODS CALLED BY MAIN

    ##
    # contract contracts all the etas and deltas in equation if no type given, otherwise just all of the given type
    # @param node, the node of the tree to start traversal: SHOULD BE THE ROOT
    # @param type if given specifies whether to contract etas or deltas
    #
    def contract(self, node, contractionType=""):
        if node is not None:
            self.contract(node.getLeft(), contractionType)
            if node.isSum():  # only contract summation objects
                if contractionType == "delta":
                    node.setElement(self.contractDeltas(node.getElement()))
                elif contractionType == "eta":
                    node.setElement(self.contractEtas(node.getElement()))
                elif contractionType == "":  # if type not specified, contract both
                    newElDel = self.contractDeltas(node.getElement())
                    node.setElement(newElDel)
                    #self.contractDeltas(node.getElement())
                    self.contractDeltas(node.getElement())
                    manny = self.contractEtas(node.getElement())
                    node.setElement(manny)
            self.contract(node.getRight(), contractionType)
    ##
    # contractDeltas helper method contracts all deltas in a Summation object
    # @param sum the Summation object to be contracted
    # @return the Summation object with contractions performed
    #
    def contractDeltas(self, sumantha):
        for s in range(len(sumantha.getSums())):
            sumantha.getSums()[s].contractDeltas()
        return sumantha

    ##
    # contractEtas helper method contracts all etas in a Summation object
    # @param sum the Summation object to be contracted
    # @return the Summation object with contractions performed
    #
    def contractEtas(self, summy):
        for s in range(len(summy.getSums())):
            summy.getSums()[s].contractEtas()
        return summy

    ##
    # sortEach goes through tree and sorts the tensors in each MultGroup object from least to greatest number of partials
    #
    def sortEach(self):
        self.tree.sortEach(self.tree.getRoot())

    ##
    # sort Terms goes through the tree and sorts the MultGroup objects in each Summation object from least to greatest number of partials (attached to tensor with least partials in MultGroup)
    #
    def sortTerms(self):
        self.tree.sortTerms(self.tree.getRoot())

    ##
    # combineLikeTerms iterates through the subtree of the given node and combines any like terms (terms differing ONLY BY COEFFICIENTS) in the summation object of the nodes of the subtree
    # @param node, the node that is the root of the (sub)tree for which like terms are to be combined (generally the root node)
    #
    def combineLikeTerms(self, node):
        if node is not None:
            self.combineLikeTerms(node.getLeft())
            self.combineLikeTerms(node.getRight())
            if node.isSum():
                node.getElement().combineLikeTerms()

    ##
    # combineLikeTermsWithoutSymCo iterates through the subtree of the given node and combines any terms differing only by NUMERICAL coefficients in the summation object of the nodes of the subtree
    # @param node, the node that is the root of the (sub)tree for which like terms are to be combined (generally the root node)
    #
    def combineLikeTermsWithoutSymCo(self, node):
        if node is not None:
            self.combineLikeTermsWithoutSymCo(node.getLeft())
            self.combineLikeTermsWithoutSymCo(node.getRight())
            if node.isSum():
                node.getElement().combineLikeTermsWithoutSymCo()

    ##
    # factorGCF iterates through the (sub)tree of the given node and if the summation object of a node in the (sub)tree has a GCF it will be factored
    # @param node, the node that is the root of the (sub)tree for which like terms are to be combined (generally the root node)
    #
    def factorGCF(self, node):
        if node is not None:
            self.factorGCF(node.getRight())
            self.factorGCF(node.getLeft())
            if node.isSum():
                self.tree.gcf(node)

    ##
    # factorUserInput factors a term out of any MultGroup objects in the summation object that includes that term (note for tensors to be factored they must be exact matches, not pattern eq)
    # note that tensors cannot be factored out if the summation object is under partials
    # @param node the node to be factored
    # @param term the term to be factored, a (LaTeX formatted) string
    #
    def factorUserInput(self, node, term):
        if not node.isSum():
            return
        sums = node.getElement().getSums()
        if len(sums) == 1 or len(sums) == 0:
            return
        for summy in sums:
            summy.factorNumFromTensorCo()
            summy.factorSymFromTensorCo()
        factored = Summation()
        added = False
        term = self.dealWithMultGroup(term)  # should be multgroup object now
        if (len(term.getTensors()) != 0 or len(term.getVariations()) != 0) and len(node.getElement().getPartials()) != 0:
            return  # don't factor if it messes with the product rule
        i = 0
        while i < len(sums):
            summy = sums[i]
            if summy.includes(term):
                added = True
                summy.removeTerm(term)  # we're changing and moving the actual object!
                factored.addTerm(copy.deepcopy(summy))
                node.getElement().removeTerm(summy)
                #sums.pop(i)  # i now references the next object in the list
            else:
                i += 1  # if term not removed, have to move i
        if added:  # if the term was factored out of any MultGroups
            factored.setBrackets(True)
            if len(sums) == 0:  # every MultGroup got factored: only create two (multiplied) nodes
                node.setRight(EquationNode(Summation([copy.deepcopy(term)])))
                node.setLeft(EquationNode(factored))
                node.setElement(Sign("*"))
            else:  # not every MultGroup got factored: add the factored terms sum multiplied by the factored term together with the unfactored terms sum
                factoredNode = EquationNode(Sign("*"))
                factoredNode.setRight(EquationNode(Summation([copy.deepcopy(term)])))
                factoredNode.setLeft(EquationNode(factored))
                node.setRight(factoredNode)
                node.setLeft(EquationNode(node.getElement()))
                node.setElement(Sign("+"))

    ##
    # factorUserInputTree iterates the (sub)tree of the given node and calls factorUserInput on each sum node in the (sub)tree
    # @ param node the node that is the root of the (sub)tree
    # @param term the term to be factored, a (LaTeX formatted) string
    #
    def factorUserInputTree(self, node, term):
        if node is not None:
            self.factorUserInputTree(node.getRight(), term)
            self.factorUserInputTree(node.getLeft(), term)
            if node.isSum():
                self.factorUserInput(node, term)

    ##
    # replaceTerms iterates the whole tree and replaces any of the (old) terms with the (new) term
    # @param old the term to be replaced, a (LaTeX formatted) string
    # @param new the term to replace with, a (LaTeX formatted) string
    #
    def replaceTerms(self, old, new):
        old = self.dealWithSummation(old)
        new = self.dealWithSummation(new)
        if old != Summation() and new != Summation():
            self.getTree().replace(self.getTree().getRoot(), old, new)

    ##
    #
    def replaceIndices(self, old, new):
        if old != "" and new != "":
            old = ''.join(old.split())
            new = ''.join(new.split())
            old = old.split(",")
            new = new.split(",")
            oldList = list()
            newList = list()
            for el in old:
                oldList.append(Index(el))
            for el in new:
                newList.append(Index(el))
            self.getTree().replaceInds(self.getTree().getRoot(), oldList, newList)




