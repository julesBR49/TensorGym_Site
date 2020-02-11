import unittest
from Tensors.Equation import Equation

class SimpleMultiplyTest(unittest.TestCase):


#  FOIL out terms without distributing derivatives

    def test_mult1(self):
        eq = Equation(" \\(A^{}\\) \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y A^{} \\partial_{\\nu}h^{\\mu \\nu} +X A^{} \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", '')

    def test_mult2(self):
        eq = Equation("\\partial_{\\mu} A \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu}\\(YA \\partial_{\\nu}h^{\\mu \\nu} +XA \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", '')
    
    
    def test_mult3(self):
        eq = Equation(" \\partial_{\\gamma}A^{\\gamma}  \\(Y \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\mu}\\partial^{\\mu} h^{\\nu }_{\\nu}\\)  ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y \\partial_{\\gamma}A^{\\gamma} \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} +X \\partial_{\\gamma}A^{\\gamma} \\partial_{\\mu}\\partial^{\\mu}h_{\\nu}^{\\nu} \\)", '')

    def test_mult4(self):
        eq = Equation("B \\partial_{\\gamma}A^{\\gamma}  \\(Y \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\mu}\\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(BY \\partial_{\\gamma}A^{\\gamma} \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} +BX \\partial_{\\gamma}A^{\\gamma} \\partial_{\\mu}\\partial^{\\mu}h_{\\nu}^{\\nu} \\)", '')
            
    def test_mult5(self):
        eq = Equation("A^{\\zeta} \\partial_{\\mu}  \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A^{\\zeta} \\partial_{\\mu}\\(Y \\partial_{\\nu}h^{\\mu \\nu} +X \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", '')

    # def test_representation(self):
    #     eq = Equation("")
    #     eq.getTree().noPfoil(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq),"", '')

    



