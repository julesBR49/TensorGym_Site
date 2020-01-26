class Sign:

    def __init__(self, strx=""):
        self.sign = strx

    def getSign(self):
        return self.sign

    def setSign(self, strx):
        self.sign = strx

    def __eq__(self, other):
        if self.getSign() == other.getSign():
            return True
        else:
            return False

    def __repr__(self):
        return self.sign
