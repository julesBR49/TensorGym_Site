import unittest
from Tensors.Equation import Equation

class SimpleRepresentationTest(unittest.TestCase):

    def test_rep1(self):
        eq = Equation("\\(a\\) + \\(b\\)")
        self.assertEqual(repr(eq),"\\(a \\)+\\(b \\)", '')


    def test_rep2(self):
        eq = Equation("\\(a \\)-\\(b \\) ")
        self.assertEqual(repr(eq),"\\(a \\)-\\(b \\)", '')


    def test_rep3(self):
        eq = Equation("b_{\\gamma} - g_{j} ")
        self.assertEqual(repr(eq),"\\( b_{\\gamma} - g_{j} \\)", '')


    def test_rep4(self):
        eq = Equation("A^{\\mu} + \\(A^{\\gamma} - B^{\\zeta}\\)")
        self.assertEqual(repr(eq),"A^{\\mu} +\\( A^{\\gamma} - B^{\\zeta} \\)", '')



    def test_rep5(self):
        eq = Equation("A^{\\mu} - \\(A^{\\gamma} - B^{\\zeta}\\) ")
        self.assertEqual(repr(eq),"A^{\\mu} - \\( A^{\\gamma} - B^{\\zeta} \\)", '')


    def test_rep6(self):
        eq = Equation("\\partial_{\\alpha} \\( a +\\( b_{\\gamma} - g\\)\\) ")
        self.assertEqual(repr(eq),"\\partial_{\\alpha} \\(a +\\( b_{\\gamma} -g \\)\\)", '')


    def test_rep7(self):
        eq = Equation("A^{\\mu} + C^{\\epsilon}\\(A^{\\gamma} - B^{\\zeta}\\)")
        self.assertEqual(repr(eq),"A^{\\mu} + C^{\\epsilon} \\( A^{\\gamma} - B^{\\zeta} \\)", '')


    def test_rep8(self):
        eq = Equation("\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a - d\\) - b\\)")
        self.assertEqual(repr(eq),"\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a -d \\)-b \\)", '')


    def test_rep9(self):
        eq = Equation("\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a^{\\gamma} - d^{\\gamma}\\) - b\\) ")
        self.assertEqual(repr(eq),"\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\( a^{\\gamma} - d^{\\gamma} \\)-b \\)", '')

    # complicated bracket nesting and tensor indices, multiplication, and partials
    def test_rep10(self):
        eq = Equation("\\partial_{\\zeta}\\( G^{\\gamma} \\) \\partial^{\\zeta} \\square \\(\\( A^{} \\)- \\( B_{\\kappa}^{\\kappa} - \\( C^{} \\)\\)\\)+\\(\\( A^{\\gamma} - D^{\\gamma} \\)- B_{\\alpha}^{\\alpha \\gamma} \\)")
        self.assertEqual(repr(eq),"\\partial_{\\zeta}\\( G^{\\gamma} \\) \\partial^{\\zeta} \\square \\(\\( A^{} \\)- \\( B_{\\kappa}^{\\kappa} - \\( C^{} \\)\\)\\)+\\(\\( A^{\\gamma} - D^{\\gamma} \\)- B_{\\alpha}^{\\alpha \\gamma} \\)", '')


    def test_rep(self):
        eq = Equation("\\begin{equation}\n G^{\\mu} =A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{equation}")
        self.assertEqual(repr(eq),"\\begin{equation} G^{\\mu} = \nA^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{equation}", '')


    # def test_rep11(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')


    # def test_rep12(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')


    # def test_rep(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')

