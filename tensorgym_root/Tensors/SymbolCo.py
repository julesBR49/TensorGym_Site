class SymbolCo:

    def __init__(self, symbol="", coeff=False):
        self.symbolCo = symbol
        self.coeff = coeff

    def getSymbolCo(self):
        return self.symbolCo

    def getCoeff(self):
        return self.coeff

    def __add__(self, other):
        if self.symbolCo != "":
            if self.symbolCo == other.getSymbolCo():
                return SymbolCo("2" + self.symbolCo)
            elif self.symbolCo.endswith("\\)"):
                self.symbolCo = self.symbolCo.replace("\\)", "")
                return SymbolCo(self.symbolCo + " + " + other.getSymbolCo() + "\\)")
            else:
                return SymbolCo("\\(" + self.symbolCo + " + " + other.getSymbolCo() + "\\)", (self.getCoeff() or other.getCoeff()))
        else:
            return other

    def getSymb(self):
        return self.symbolCo

    def __sub__(self, other):
        if self.symbolCo == other.getSymbolCo():
                return SymbolCo("zero")
        if self.symbolCo.endswith("\\)"):
            self.symbolCo = self.symbolCo.replace("\\)", "")
            return SymbolCo(self.symbolCo + " - " + other.getSymbolCo() + "\\)")
        else:
            return SymbolCo("\\(" + self.symbolCo + " - " + other.getSymbolCo() + "\\)", (self.getCoeff() or other.getCoeff()))

    def __mul__(self, other):
        return SymbolCo(self.symbolCo + other.getSymbolCo(), (self.getCoeff() or other.getCoeff()))

    def __truediv__(self, other):
        if other.getSymbolCo() in self.symbolCo:
            return SymbolCo(self.symbolCo.replace(other.getSymbolCo(), ''), (self.getCoeff() or other.getCoeff()))
        else:
            return SymbolCo('\\frac{'+self.symbolCo+'}{'+other.getSymbolCo()+'}', (self.getCoeff() or other.getCoeff()))

    def __repr__(self, addCof=True):
        strx = ''
        if self.getCoeff():
            strx += "\\coeff{"
        strx += self.symbolCo
        if self.getCoeff():
            strx += "}"
        return strx

    def __eq__(self, other):
        return self.symbolCo == other.getSymbolCo()
