import unittest
from Tensors.Equation import Equation

class SimpleMultiplyTest(unittest.TestCase):


# FOIL out terms, distributing derivatives when necessary (recommended) ------------------------------------------------------

    def test_foil1(self):
        eq = Equation("\\(A^{}\\) \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.getTree().foil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y A^{} \\partial_{\\nu} \\partial_{\\mu} h^{\\mu \\nu} +X A^{} \\partial^{\\mu} \\partial_{\\mu} h_{\\nu}^{\\nu} \\)", '')

# Distribute partial derivatives ------------------------------------------------------
    
    def test_distributep1(self):
        eq = Equation("\\partial_{\\mu} \\(5 \\partial_{\\nu}h^{\\mu \\nu} + 3 \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(5 \\partial_{\\nu} \\partial_{\\mu} h^{\\mu \\nu} +3 \\partial^{\\mu} \\partial_{\\mu} h_{\\nu}^{\\nu} \\)", '')

    def test_distributep2(self):
        eq = Equation("\\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y \\partial_{\\nu} \\partial_{\\mu} h^{\\mu \\nu} +X \\partial^{\\mu} \\partial_{\\mu} h_{\\nu}^{\\nu} \\)", '')

    def test_distributep3(self):
        eq = Equation("\\partial_{\\mu} \\(5 \\partial_{\\nu}h^{\\mu \\nu} + V \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(5 \\partial_{\\nu} \\partial_{\\mu} h^{\\mu \\nu} +V \\partial^{\\mu} \\partial_{\\mu} h_{\\nu}^{\\nu} \\)", '')

# product rule
    def test_distributep4(self):
        eq = Equation("\\partial_{\\mu} \\( A^{\\gamma}B^{\\zeta}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\( \\partial_{\\mu} A^{\\gamma} B^{\\zeta} + \\partial_{\\mu} B^{\\zeta} A^{\\gamma} \\)", '')

# three term product rule
    def test_distributep5(self):
        eq = Equation("\\partial_{\\mu} \\( A^{\\gamma}B^{\\zeta}G^{\\alpha}\\)")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\( \\partial_{\\mu} A^{\\gamma} B^{\\zeta} G^{\\alpha} + \\partial_{\\mu} B^{\\zeta} G^{\\alpha} A^{\\gamma} + \\partial_{\\mu} G^{\\alpha} B^{\\zeta} A^{\\gamma} \\)", '')

# distribute through multiple terms
    def test_distributep6(self):
        eq = Equation("\\partial_{\\mu} \\( A^{\\gamma}B^{\\zeta}\\) \\partial_{\\alpha}\\(A_{\\gamma}\\) + \\partial_{\\alpha}\\(G_{\\mu \\zeta}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\( \\partial_{\\mu} A^{\\gamma} B^{\\zeta} + \\partial_{\\mu} B^{\\zeta} A^{\\gamma} \\)\\( \\partial_{\\alpha} A_{\\gamma} \\)+\\( \\partial_{\\alpha} G_{\\mu \\zeta} \\)", '')

# multiple partials product rule
    def test_distributep7(self):
        eq = Equation("\\partial_{\\alpha}\\partial_{\\gamma} \\( A^{\\alpha} B^{\\gamma}\\) ")
        eq.getTree().distributePs(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\( \\partial_{\\alpha} \\partial_{\\gamma} A^{\\alpha} B^{\\gamma} + \\partial_{\\gamma} B^{\\gamma} \\partial_{\\alpha} A^{\\alpha} + \\partial_{\\alpha} \\partial_{\\gamma} B^{\\gamma} A^{\\alpha} + \\partial_{\\gamma} A^{\\alpha} \\partial_{\\alpha} B^{\\gamma} \\)", '')
    
# product rule with squares
    def test_distributep8(self):
        eq = Equation("\\square \\(A^{\\alpha}B_{\\alpha}\\)")
        eq.getTree().distributePs(eq.getTree().getRoot())
        # self.assertRegex(repr(eq), '\\( \\square A\^\{\\alpha\} B_\{\\alpha\} + \\partial\^\{\\.*\} B_\{\\alpha\} \\partial_\{\\.*\} A\^\{\\alpha\} + \\square B_\{\\\\alpha\} A\^\{\\alpha\} + \\partial\^\{\\\\.*\} A\^\{\\alpha\} \\partial_\{\\.*\} B_\{\\alpha\} \\)', 'product rule with squares')
        # self.assertRegex(repr(eq), '\\\\( \\\\square A\{\\\\alpha} B_{\\\\alpha} \+ \\\\partial\^{\\\\.*} B_{\\\\alpha} \\\\partial_{\\\\.*} A\^{\\\\alpha} \+ \\\\square B_{\\\\alpha} A\^{\\\\alpha} \+ \\\\partial\^{\\\\.*} A\^{\\\\alpha} \\\\partial_{\\\\.*} B_{\\\\alpha} \\\\)', 'product rule with squares')
        self.assertRegex(repr(eq), '\\\\\( \\\\square A\^\{\\\\alpha\} B_\{\\\\alpha\} \+ \\\\partial\^\{\\\\.*\} B_\{\\\\alpha\} \\\\partial_\{\\\\.*\} A\^\{\\\\alpha\} \+ \\\\square B_\{\\\\alpha\} A\^\{\\\\alpha\} \+ \\\\partial\^\{\\\\.*\} A\^\{\\\\alpha\} \\\\partial_\{\\\\.*\} B_\{\\\\alpha\} \\\\\)', 'product rule with squares')


    # def test_distributep1(self):
    #     eq = Equation("")
    #     eq.getTree().distributePs(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq),"", '')




#  FOIL out terms without distributing derivatives ------------------------------------------------------

    def test_noPmult1(self):
        eq = Equation(" \\(A^{}\\) \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y A^{} \\partial_{\\nu} h^{\\mu \\nu} +X A^{} \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')
    
    def test_noPmult2(self):
        eq = Equation(" \\partial_{\\gamma}A^{\\gamma}  \\(Y \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\mu}\\partial^{\\mu} h^{\\nu }_{\\nu}\\)  ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y \\partial_{\\gamma} A^{\\gamma} \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} +X \\partial_{\\gamma} A^{\\gamma} \\partial_{\\mu} \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')
    
    def test_noPmult3(self):
        eq = Equation("\\partial_{\\mu}   A^{\\epsilon} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) + B^{\\epsilon} ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y \\partial_{\\mu} A^{\\epsilon} \\partial_{\\nu} h^{\\mu \\nu} +X \\partial_{\\mu} A^{\\epsilon} \\partial^{\\mu} h_{\\nu}^{\\nu} + B^{\\epsilon} \\)", '')

    def test_noPmult4(self):
        eq = Equation("\\partial_{\\mu}   A^{\\epsilon} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) - B^{\\epsilon} ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(Y \\partial_{\\mu} A^{\\epsilon} \\partial_{\\nu} h^{\\mu \\nu} +X \\partial_{\\mu} A^{\\epsilon} \\partial^{\\mu} h_{\\nu}^{\\nu} - B^{\\epsilon} \\)", '')

    def test_noPmult5(self):
        eq = Equation("B \\partial_{\\gamma}A^{\\gamma}  \\(Y \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\mu}\\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(BY \\partial_{\\gamma} A^{\\gamma} \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} +BX \\partial_{\\gamma} A^{\\gamma} \\partial_{\\mu} \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')
            
    def test_noPmult6(self):
        eq = Equation("A^{\\zeta} \\partial_{\\mu}  \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A^{\\zeta} \\partial_{\\mu} \\(Y \\partial_{\\nu} h^{\\mu \\nu} +X \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')

    def test_noPmult7(self):
        eq = Equation(" \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) +  T^{\\gamma} \\(A_{\\gamma} + B_{\\gamma}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(Y \\partial_{\\nu} h^{\\mu \\nu} +X \\partial^{\\mu} h_{\\nu}^{\\nu} \\)+\\( T^{\\gamma} A_{\\gamma} + T^{\\gamma} B_{\\gamma} \\)", '')

    def test_noPmult8(self):
        eq = Equation("A^{\\epsilon} \\partial_{\\mu}  \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) + B^{\\epsilon}   ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A^{\\epsilon} \\partial_{\\mu} \\(Y \\partial_{\\nu} h^{\\mu \\nu} +X \\partial^{\\mu} h_{\\nu}^{\\nu} \\)+ B^{\\epsilon}", '')

    def test_noPmult9(self):
        eq = Equation("A^{\\epsilon} \\partial_{\\mu}  \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) - B^{\\epsilon}   ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"A^{\\epsilon} \\partial_{\\mu} \\(Y \\partial_{\\nu} h^{\\mu \\nu} +X \\partial^{\\mu} h_{\\nu}^{\\nu} \\)- B^{\\epsilon}", '')

# constants can move through derivatives 

    def test_noPmult10(self):
        eq = Equation("A \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(YA \\partial_{\\nu} h^{\\mu \\nu} +XA \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')

    def test_noPmult11(self):
        eq = Equation("\\partial_{\\mu} A \\(Y \\partial_{\\nu} h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(YA \\partial_{\\nu} h^{\\mu \\nu} +XA \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')
    

    def test_noPmult12(self):
        eq = Equation("4 \\partial_{\\mu}  \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(4 Y \\partial_{\\nu} h^{\\mu \\nu} +4 X \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')

# sum of constants
    def test_noPmult13(self):
        eq = Equation("\\(A + 5B + CD \\) \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(YA \\partial_{\\nu} h^{\\mu \\nu} +5 YB \\partial_{\\nu} h^{\\mu \\nu} +YCD \\partial_{\\nu} h^{\\mu \\nu} +XA \\partial^{\\mu} h_{\\nu}^{\\nu} +5 XB \\partial^{\\mu} h_{\\nu}^{\\nu} +XCD \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')

# etas and deltas
    def test_noPmult14(self):
        eq = Equation("\\delta^{\\gamma}_{\\zeta} \\eta^{\\nu \\alpha} \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\zeta} + X \\partial^{\\mu} h^{\\zeta }_{\\nu}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(Y \\delta_{\\zeta}^{\\gamma} \\eta^{\\nu \\alpha} \\partial_{\\nu} h^{\\mu \\zeta} +X \\delta_{\\zeta}^{\\gamma} \\eta^{\\nu \\alpha} \\partial^{\\mu} h_{\\nu}^{\\zeta} \\)", '')

# sum of mixed constants
    def test_noPmult15(self):
        eq = Equation("\\(A \\eta^{\\gamma \\epsilon} + A5B + 56 \\delta^{\\phi}_{\\xi} \\) \\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\(YA \\eta^{\\gamma \\epsilon} \\partial_{\\nu} h^{\\mu \\nu} +5 YAB \\partial_{\\nu} h^{\\mu \\nu} +56 Y \\delta_{\\xi}^{\\phi} \\partial_{\\nu} h^{\\mu \\nu} +XA \\eta^{\\gamma \\epsilon} \\partial^{\\mu} h_{\\nu}^{\\nu} +5 XAB \\partial^{\\mu} h_{\\nu}^{\\nu}  \\\\ \n +56 X \\delta_{\\xi}^{\\phi} \\partial^{\\mu} h_{\\nu}^{\\nu} \\)", '')

# partials
# def test_mult15(self):
#         eq = Equation("")
#         eq.getTree().noPfoil(eq.getTree().getRoot())
#         self.assertEqual(repr(eq),"", '')

# FOIL - 2 terms
    def test_noPmult16(self):
        eq = Equation("\\(A^{\\epsilon} + B^{\\gamma} \\) \\( \\partial_{\\mu}X^{\\mu} + M^{\\nu \\zeta}_{\\gamma} \\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\( A^{\\epsilon} \\partial_{\\mu} X^{\\mu} + A^{\\epsilon} M_{\\gamma}^{\\nu \\zeta} + B^{\\gamma} \\partial_{\\mu} X^{\\mu} + B^{\\gamma} M_{\\gamma}^{\\nu \\zeta} \\)", '')

# FOIL - 3 terms
    def test_noPmult17(self):
        eq = Equation("H \\(A^{\\epsilon} + B^{\\gamma} \\) \\( \\partial_{\\mu}X^{\\mu} + M^{\\nu \\zeta}_{\\gamma} \\) \\( X + Y\\) ")
        eq.getTree().noPfoil(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\(HX A^{\\epsilon} \\partial_{\\mu} X^{\\mu} +HY A^{\\epsilon} \\partial_{\\mu} X^{\\mu} +HX A^{\\epsilon} M_{\\gamma}^{\\nu \\zeta} +HY A^{\\epsilon} M_{\\gamma}^{\\nu \\zeta} +HX B^{\\gamma} \\partial_{\\mu} X^{\\mu} +HY B^{\\gamma} \\partial_{\\mu} X^{\\mu}  \\\\ \n +HX B^{\\gamma} M_{\\gamma}^{\\nu \\zeta} +HY B^{\\gamma} M_{\\gamma}^{\\nu \\zeta} \\)", '')

    # def test_mult15(self):
    #     eq = Equation("")
    #     eq.getTree().noPfoil(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq),"", '')

    



