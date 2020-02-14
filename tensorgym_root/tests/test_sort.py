import unittest
from Tensors.Equation import Equation

class SimpleMultiplyTest(unittest.TestCase):
    
    #  combine like terms differing only by a numerical factor

    def test_combineLikeTermsNum1(self):
        eq = Equation("3A^{\\gamma} + \\frac{5}{7} A^{\\gamma} ")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\frac{26}{7} A^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

    def test_combineLikeTermsNum2(self):
        eq = Equation("3A^{\\gamma} + \\frac{4}{2} A^{\\gamma} ")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(5 A^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

    def test_combineLikeTermsNum3(self):
        eq = Equation("A^{\\gamma} + A^{\\gamma} ")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(2 A^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

    def test_combineLikeTermsNum4(self):
        eq = Equation("3\\partial_{\\gamma}A^{\\gamma} + \\frac{5}{7} \\partial_{\\beta}A^{\\beta}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\frac{26}{7} \\partial_{\\gamma}A^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')


    def test_combineLikeTermsNum5(self):
        eq = Equation("3\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7 \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\nu \\zeta}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(10 \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

    # def test_combineLikeTermsNum1(self):
    #     eq = Equation("")
    #     eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq), "",
    #     'error in combining like terms differing only by a numerical factor')

    # def test_combineLikeTermsNum1(self):
    #     eq = Equation("")
    #     eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq), "",
    #     'error in combining like terms differing only by a numerical factor')

    # def test_combineLikeTermsNum1(self):
    #     eq = Equation("")
    #     eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq), "",
    #     'error in combining like terms differing only by a numerical factor')

    # def test_combineLikeTermsNum1(self):
    #     eq = Equation("")
    #     eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq), "",
    #     'error in combining like terms differing only by a numerical factor')

    # def test_combineLikeTermsNum1(self):
    #     eq = Equation("")
    #     eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
    #     self.assertEqual(repr(eq), "",
    #     'error in combining like terms differing only by a numerical factor')


    # combine like terms differing by any (numerical or symbolic) coefficient


    # sort the tensors in each term by number of derivatives (least to greatest)


    # sort terms by number of derivatives (least to greatest)