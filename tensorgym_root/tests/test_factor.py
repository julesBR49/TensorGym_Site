import unittest
from Tensors.Equation import Equation

class SimpleFactorTest(unittest.TestCase):  

# factor out GCF

    def test_factor_gcf1(self):
        eq = Equation("\\(3Y \\partial_{\\nu}h^{\\mu \\nu} + Y \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"Y \\(3 \\partial_{\\nu} h^{\\mu \\nu} + \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')


    def test_factor_gcf2(self):
        eq = Equation("\\(X \\partial_{\\nu}h^{\\mu \\nu} + Y \\partial_{\\nu} h^{\\mu \\nu}\\)")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\nu} h^{\\mu \\nu} \\(X +Y \\)", '')


    def test_factor_gcf3(self):
        eq = Equation("\\(X A^{\\alpha}_{\\alpha} + Y A^{\\alpha}_{\\alpha}\\)")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A_{\\alpha}^{\\alpha} \\(X +Y \\)", '')


    def test_factor_gcf4(self):
        eq = Equation("X A^{\\alpha}_{\\alpha} + Y A^{\\alpha}_{\\alpha}")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A_{\\alpha}^{\\alpha} \\(X +Y \\)", '')


    def test_factor_gcf5(self):
        eq = Equation("\\(X \\partial_{\\gamma}h^{\\mu \\gamma} + Y \\partial_{\\nu} h^{\\mu \\nu}\\) ")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\gamma} h^{\\mu \\gamma} \\(X +Y \\)", '')

    def test_factor_gcf6(self):
        eq = Equation("\\(X \\partial_{\\gamma}h^{\\mu \\gamma} A^{\\alpha}_{\\alpha} + Y \\partial_{\\nu} h^{\\mu \\nu}\\)")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\gamma} h^{\\mu \\gamma} \\(X A_{\\alpha}^{\\alpha} +Y \\)", '')


    def test_factor_gcf7(self):
        eq = Equation("\\(X \\partial_{\\gamma}h^{\\mu \\gamma} + Y h^{\\gamma \\nu}\\) ")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(X \\partial_{\\gamma} h^{\\mu \\gamma} +Y h^{\\gamma \\nu} \\)", '')

    def test_factor_gcf8(self):
        eq = Equation("\\(\\frac{1}{2} \\partial_{\\gamma} h^{\\mu \\gamma} + \\frac{1}{4}  h^{\\gamma \\nu}\\) ")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\frac{1}{4} \\(2 \\partial_{\\gamma} h^{\\mu \\gamma} + h^{\\gamma \\nu} \\)", '')

    def test_factor_gcf9(self):
        eq = Equation("\\(X \\partial_{\\nu}h^{\\mu \\nu} + \\partial_{\\nu} h^{\\mu \\nu}\\)")
        eq.factorGCF(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\nu} h^{\\mu \\nu} \\(X +1 \\)", '')