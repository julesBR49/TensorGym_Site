from Tensors.Summation import Summation
from Tensors.Sign import Sign
class EquationNode:

    def __init__(self, element=None, brackets=False):
        self.element = element
        self.brackets = brackets
        self.rightChild = None
        self.leftChild = None

    def getElement(self):
        return self.element

    def getBrackets(self):
        return self.brackets

    def setBrackets(self, brackets):
        self.brackets = brackets

    def setElement(self, newEl):
        self.element = newEl

    def getRight(self):
        return self.rightChild

    def getLeft(self):
        return self.leftChild

    def setRight(self, el):
        self.rightChild = el

    def setLeft(self, el):
        self.leftChild = el

    def isSum(self):
        if type(self.element) is Summation:
            return True
        else:
            return False

    def isAlgOpp(self):

        if type(self.element) is Sign:
            return True
        else:
            return False

    def isLeaf(self):
        if self.leftChild is None and self.rightChild is None:
            return True
        else:
            return False

