import copy

class Gemma:

    def __init__(self, callie=None):
        if callie is None:
            self.stype = []
        else:
            self.stype = callie

    def add(self, other):
        self.stype.append(other)

    def getType(self):
        return self.stype

    def setType(self, stype):
        self.stype = stype

    def __eq__(self, other):
        return self.testSETListEquality(self.getType(), other.getType())

    def __lt__(self, other):
        return self.getType() < other.getType()

    def sort(self):
        self.stype.sort()

    def __repr__(self):
        strx = ''
        self.sort()
        for el in self.stype:
            strx += el
        return strx
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
