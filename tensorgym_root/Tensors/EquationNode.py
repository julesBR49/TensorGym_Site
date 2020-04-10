from Tensors.MultGroup import MultGroup
# from Tensors.Sign import Sign
from enum import Enum

class Sign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"

class EquationNode:

    """
    simple node class
    """

    def __init__(self, sign = Sign.POSITIVE):
        self.sign = sign
        # self.brackets = brackets
        self.children = None

    # def getBrackets(self):
    #     return self.brackets

    # def setBrackets(self, brackets):
    #     self.brackets = brackets

    def getChildren(self):
        return self.children

    def getSign(self):
        return self.sign

    def setSign(self, newSign):
        if not isinstance(newSign, Sign):
            raise TypeError('sign must be an instance of Sign Enum')
        self.sign = newSign

    def isLeaf(self):
        if self.children is None:
            return True
        else:
            return False

class ElementNode(EquationNode):
    # ElementNodes have elements which have getters and setters. They must be leaf nodes
    # so they have no methods to set children

    def __init__(self, element = None, sign = Sign.POSITIVE):
        if element is not None and not isinstance(element, MultGroup):
            raise TypeError('element must be an instance of MultGroup or None')
        self.element = element
        EquationNode.__init__(self, sign)
    
    
    def getElement(self):
        return self.element

    def setElement(self, el):
        if not isinstance(el, MultGroup):
            raise TypeError('element must be an instance of MultGroup')
        self.element = el


class BracketsNode(EquationNode):
    # BracketNodes must be internal nodes. They have no elements but have methods 
    # to set and add children nodes
    def __init__(self, sign = Sign.POSITIVE):
        self.partials = []
        EquationNode.__init__(self, sign)

    def addPartial(self, partial):
        self.partials.append(partial)

    def setPartials(self, partials):
        self.partials = partials

    def removePartial(self, partial):
        if partial in self.partials:
            self.partials.remove(partial)

    def setChildren(self, el):
        self.children = el

    def addChild(self, newChild):
        if not isinstance(newChild, EquationNode):
            raise TypeError('child must be an instance of EquationNode')
        if self.children is None:
            self.children = list()
        self.children.add(newChild)

    def removeChildren(self):
        self.children = None

    def removeChild(self, child):
        if self.children is not None and child in self.children:
            self.children.remove(child)
            return 1
        return 0


class MultBracNode(BracketsNode):
    pass

class SumBracNode(BracketsNode):
    pass


    def distributePartials(self):
        while len(self.partials) > 0:
            partial = self.partials[0]
            self.distributePartial(partial)
            self.removePartial(partial)

    def distributePartial(self, partial):
        if partial is not None:
            for child in self.getChildren():
                if isinstance(child, ElementNode):
                    multiplication = child.getElement()
                    productRuleOfSum = multiplication.distributePartial(copy.deepcopy(partial), copy.deepcopy(multiplication.getTensors()) + copy.deepcopy(multiplication.getVariations()))  # returns a summation object
                    child.setElement(productRuleOfSum)
                if isinstance(child, SumBracNode):
                    child.addPartial(partial)
                    child.distributePartials()
                if isinstance(child, MultBracNode):
                    child.addPartial(partial)


class RootNode(SumBracNode):
    pass
    