import unittest
from Tensors.Equation import Equation

class SimpleEquationTest(unittest.TestCase):
    # def setUp(self):
    #     self.eq = Equation('')

    def test_representation(self):
        eq = Equation(" Z \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta}")
        self.assertEqual(repr(eq),"\\(Z \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} +X \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} \\)", 'incorrect representation of equation')

    ## Need to fix logic on FOILing

    # def test_foil(self):
    #     # "\partial_{\mu} \(Y \partial_{\nu}h^{\mu \nu} + X \partial^{\mu} h^{\nu }_{\nu}\)"
    #     eq = Equation(" Z \\(\\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta}\\)")
    #     eq.getTree().foil(self.eq.getTree().getRoot())
    #     self.assertEqual(repr(self.eq),"\\(Z \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} +ZX \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} \\)", 'incorrect FOIL operation')
            
    # def test_distributePs(self):
    #     eq = Equation("\\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
    #     eq.getTree().distributePs(self.eq.getTree().getRoot())
    #     self.assertEqual(repr(self.eq), "\\( \\partial_{\\nu}\\partial_{\\mu}h^{\\mu \\nu} + \\partial^{\\mu}\\partial_{\\mu}h_{\\nu}^{\\nu} \\)", 'error in distributing partial derivatives')

    # def test_noPfoil(self):
    #     eq = Equation("A\\partial_{\\mu} \\(Y \\partial_{\\nu}h^{\\mu \\nu} + X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
    #     self.eq.getTree().noPfoil(self.eq.getTree().getRoot())
    #     self.assertEqual(repr(self.eq), "\\partial_{\\mu} \\( A \\partial_{\\nu}h^{\\mu \\nu} + A \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", 'error in distributing partial derivatives')
     
    # def test_contract(self):
    #     eq.contract(eq.getTree().getRoot())

    # def test_contractEtas(self):
    #     self.eq.contract(self.eq.getTree().getRoot(), 'eta')

    # def test_contractDeltas(self):
    #     self.eq.contract(self.eq.getTree().getRoot(), 'delta')

    # def test_factorGCF(self):
    #     self.eq.factorGCF(self.eq.getTree().getRoot())

    # def test_factorTerm(self):
    #     term_to_factor = ""
    #     self.eq.factorUserInputTree(self.eq.getTree().getRoot(), term_to_factor)
        
    def test_replaceIndices(self):
        eq = Equation(" Z \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta} ")
        indices_to_replace = "\\mu, \\nu, \\alpha, \\beta"
        replacement_indices = "\\gamma, \\zeta, \\chi, \\xi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq), "\\(Z \\partial_{\\gamma}\\partial_{\\zeta}h^{\\gamma \\zeta} +X \\partial_{\\chi}\\partial_{\\xi}h^{\\chi \\xi} \\)",
         'error in replacing indices')

    def test_replaceTerms(self):
        eq = Equation(" Z \\partial_{\mu} \\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta} ")
        term_to_replace = "\\partial_{\\gamma} \\partial_{\\zeta}h^{\\gamma \\zeta}"
        replacement_term = "m^{}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq), "\\(Z m^{} +X m^{} \\)")

    def test_combineLikeTermsNum(self):
        eq = Equation("\\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} + \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta} ")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(2 \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} \\)",
        'error in combining like terms differing only by a numerical factor')

    def test_combineLikeTerms(self):
        eq = Equation(" Z \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} + X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta} ")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(Z+X\\) \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} \\)",
        'error in combining like terms differing by any (numerical or symbolic) coefficient')

    def test_sortEach(self):
        eq = Equation(" Z \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu}\\partial_{\\alpha} h^{\\alpha \\beta} ")
        eq.sortEach()
        self.assertEqual(repr(eq), "Z \\partial_{\\alpha}h^{\\alpha \\beta} \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu}",
        'error in sorting the tensors in each term by number of derivatives (least to greatest)')
        
    def test_sortTerms(self):
        eq = Equation("X \\partial_{\\alpha}\\partial_{\\beta} h^{\\alpha \\beta} + Z \\partial_{\\nu}h^{\\mu \\nu} ")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\\(Z \\partial_{\\nu}h^{\\mu \\nu} +X \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} \\)",
        'error in sorting terms by number of derivatives (least to greatest)')

if __name__ == '__main__':
    unittest.main()