import unittest
from Tensors.Equation import Equation

class SimpleSortTest(unittest.TestCase):
    
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

    # not all terms combine 
    def test_combineLikeTermsNum6(self):
        eq = Equation("3\\partial_{\\gamma}A^{\\gamma} + 4 A^{\\chi}+ \\frac{5}{7} \\partial_{\\beta}A^{\\beta} ")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\frac{26}{7} \\partial_{\\gamma}A^{\\gamma} +4 A^{\\chi} \\)",
        'error in combining like terms differing only by a numerical factor')

    # things that shouldn’t combine
    # different tensors
    def test_combineLikeTermsNum7(self):
        eq = Equation("3A^{\\gamma} + \\frac{5}{7} B^{\\gamma}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3 A^{\\gamma} +\\frac{5}{7} B^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')


    # not differing only by numerical factor
    def test_combineLikeTermsNum8(self):
        eq = Equation("3XA^{\\gamma} + 7 A^{\\gamma}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3 X A^{\\gamma} +7 A^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

    # different free indices
    def test_combineLikeTermsNum9(self):
        eq = Equation("A^{\\beta} + A^{\\alpha}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\( A^{\\beta} + A^{\\alpha} \\)",
        'error in combining like terms differing only by a numerical factor')

    # different number of partials
    def test_combineLikeTermsNum10(self):
        eq = Equation("3\\partial_{\\gamma}A^{\\gamma}_{\\nu} + 7 \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\nu \\zeta}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3 \\partial_{\\gamma}A_{\\nu}^{\\gamma} +7 \\partial_{\\beta}\\partial^{\\zeta}A_{\\nu \\zeta}^{\\beta} \\)",
        'error in combining like terms differing only by a numerical factor')

    # different position of free index
    def test_combineLikeTermsNum11(self):
        eq = Equation("3\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7 \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\zeta \\nu}")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3 \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} +7 \\partial_{\\beta}\\partial^{\\zeta}A_{\\zeta \\nu}^{\\beta} \\)",
        'error in combining like terms differing only by a numerical factor')

    # (Unless A is a symmetric tensor, in which case):
    def test_combineLikeTermsNum12(self):
        eq = Equation("3\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7 \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\zeta \\nu} ", "A")
        eq.combineLikeTermsWithoutSymCo(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(10 \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} \\)",
        'error in combining like terms differing only by a numerical factor')

# combine like terms differing by any (numerical or symbolic) coefficient

    # basic case
    def test_combineLikeTerms1(self):
        eq = Equation("3XA^{\\gamma} + 7 A^{\\gamma}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(3X+7\\) A^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')
    
    # more complicated term
    def test_combineLikeTerms2(self):
        eq = Equation("3B \\partial_{\\gamma}A^{\\gamma} + \\frac{5}{7} V \\partial_{\\beta}A^{\\beta}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(3B+\\frac{5}{7}V\\) \\partial_{\\gamma}A^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')


    def test_combineLikeTerms3(self):
        eq = Equation("3B \\partial_{\\gamma}A^{\\gamma} + \\frac{5}{7} B \\partial_{\\beta}A^{\\beta}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\frac{26}{7}B \\partial_{\\gamma}A^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')


    def test_combineLikeTerms4(self):
        eq = Equation("3M\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7X \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\nu \\zeta}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(3M+7X\\) \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # not all terms combine 
    def test_combineLikeTerms5(self):
        eq = Equation("3V\\partial_{\\gamma}A^{\\gamma} + 4 ZA^{\\chi}+ \\frac{5}{7} N \\partial_{\\beta}A^{\\beta} ")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(3V+\\frac{5}{7}N\\) \\partial_{\\gamma}A^{\\gamma} +4Z A^{\\chi} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # shouldn’t combine

    # differs by a factor that is a tensor
    def test_combineLikeTerms6(self):
        eq = Equation("3B \\partial_{\\gamma}A^{\\gamma} + \\frac{5}{7} V^{\\alpha}_{\\alpha} \\partial_{\\beta}A^{\\beta}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3B \\partial_{\\gamma}A^{\\gamma} +\\frac{5}{7} V_{\\alpha}^{\\alpha} \\partial_{\\beta}A^{\\beta} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # different tensors
    def test_combineLikeTerms7(self):
        eq = Equation("3CA^{\\gamma} + \\frac{5}{7} DB^{\\gamma}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3C A^{\\gamma} +\\frac{5}{7}D B^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # different free indices
    def test_combineLikeTerms8(self):
        eq = Equation("XA^{\\beta} + A^{\\alpha}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(X A^{\\beta} + A^{\\alpha} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # different number of partials
    def test_combineLikeTerms9(self):
        eq = Equation("3\\partial_{\\gamma}A^{\\gamma}_{\\nu} + 7M \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\nu \\zeta}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3 \\partial_{\\gamma}A_{\\nu}^{\\gamma} +7M \\partial_{\\beta}\\partial^{\\zeta}A_{\\nu \\zeta}^{\\beta} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # different position of free index
    def test_combineLikeTerms10(self):
        eq = Equation("3V\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7L \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\zeta \\nu}")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(3V \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} +7L \\partial_{\\beta}\\partial^{\\zeta}A_{\\zeta \\nu}^{\\beta} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

    # (Unless A is a symmetric tensor, in which case)

    def test_combineLikeTerms11(self):
        eq = Equation("3V\\partial_{\\gamma}\\partial^{\\mu}A^{\\gamma}_{\\nu \\mu} + 7L \\partial_{\\beta}\\partial^{\\zeta}A^{\\beta}_{\\zeta \\nu}", "A")
        eq.combineLikeTerms(eq.getTree().getRoot())
        self.assertEqual(repr(eq), "\\(\\(3V+7L\\) \\partial_{\\gamma}\\partial^{\\mu}A_{\\nu \\mu}^{\\gamma} \\)",
        'error in combining like terms differing by any (numerical or symbolic) factor')

# sort the tensors in each term by number of derivatives (least to greatest)

    def test_sortTensors1(self):
        eq = Equation("\\partial_{\\gamma} \\square G^{\\nu \\gamma} \\partial_{\\beta}\\partial^{\\xi} M^{\\beta}_{\\xi}   \\square \\square \\partial_{\\chi} X^{\\kappa \\zeta}_{\\nu}  \\partial_{\\mu}T^{\\mu}")
        eq.sortEach()
        self.assertEqual(repr(eq), "\\partial_{\\mu}T^{\\mu} \\partial_{\\beta}\\partial^{\\xi}M_{\\xi}^{\\beta} \\partial_{\\gamma}\\square G^{\\nu \\gamma} \\partial_{\\chi}\\square \\square X_{\\nu}^{\\kappa \\zeta}",
        'error in sorting the tensors in each term by number of derivatives (least to greatest)')

    # What about with coefficients
    def test_sortTensors2(self):
        eq = Equation("4A\\partial_{\\gamma} \\square G^{\\nu \\gamma} \\partial_{\\beta}\\partial^{\\xi} M^{\\beta}_{\\xi}  \\square \\square \\partial_{\\chi} X^{\\kappa \\zeta}_{\\nu}  \\partial_{\\mu}T^{\\mu}")
        eq.sortEach()
        self.assertEqual(repr(eq), "4 A \\partial_{\\mu}T^{\\mu} \\partial_{\\beta}\\partial^{\\xi}M_{\\xi}^{\\beta} \\partial_{\\gamma}\\square G^{\\nu \\gamma} \\partial_{\\chi}\\square \\square X_{\\nu}^{\\kappa \\zeta}",
        'error in sorting the tensors in each term by number of derivatives (least to greatest)')

    # What about multiple terms and coefficients
    def test_sortTensors3(self):
        eq = Equation("4A\\partial_{\\gamma} \\square G^{\\nu \\gamma} \\partial_{\\beta}\\partial^{\\xi} M^{\\beta}_{\\xi} +\\frac{7}{8} C \\square \\square \\partial_{\\chi} X^{\\kappa \\zeta}_{\\nu}  \\partial_{\\mu}T^{\\mu}")
        eq.sortEach()
        self.assertEqual(repr(eq), "\\(4 A \\partial_{\\beta}\\partial^{\\xi}M_{\\xi}^{\\beta} \\partial_{\\gamma}\\square G^{\\nu \\gamma} +\\frac{7}{8} C \\partial_{\\mu}T^{\\mu} \\partial_{\\chi}\\square \\square X_{\\nu}^{\\kappa \\zeta} \\)",
        'error in sorting the tensors in each term by number of derivatives (least to greatest)')

    # And with brackets 
    def test_sortTensors4(self):
        eq = Equation("\\( 4A\\partial_{\\gamma} \\square G^{\\nu \\gamma} \\partial_{\\beta}\\partial^{\\xi} M^{\\beta}_{\\xi}\\)\\(\\frac{7}{8} C \\square \\square \\partial_{\\chi} X^{\\kappa \\zeta}_{\\nu}  \\partial_{\\mu}T^{\\mu} \\)")
        eq.sortEach()
        self.assertEqual(repr(eq), "\\(4 A \\partial_{\\beta}\\partial^{\\xi}M_{\\xi}^{\\beta} \\partial_{\\gamma}\\square G^{\\nu \\gamma} \\)\\(\\frac{7}{8} C \\partial_{\\mu}T^{\\mu} \\partial_{\\chi}\\square \\square X_{\\nu}^{\\kappa \\zeta} \\)",
        'error in sorting the tensors in each term by number of derivatives (least to greatest)')

# sort terms by number of derivatives (least to greatest)

    def test_sortTerms1(self):
        eq = Equation("\\partial_{\\gamma} \\partial_{\\kappa}A^{\\gamma} + \\partial^{\\chi}B_{\\chi} + C^{} ")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\\( C^{} + \\partial^{\\chi}B_{\\chi} + \\partial_{\\gamma}\\partial_{\\kappa}A^{\\gamma} \\)",
        'error in sorting the terms by number of derivatives (least to greatest)')
    
    # with brackets
    def test_sortTerms2(self):
        eq = Equation("\\(\\partial_{\\gamma} \\partial_{\\kappa}A^{\\gamma} + \\partial^{\\chi}B_{\\chi} + C^{}\\) ")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\( C^{} + \partial^{\chi}B_{\chi} + \partial_{\gamma}\\partial_{\\kappa}A^{\\gamma} \\)",
        'error in sorting the terms by number of derivatives (least to greatest)')
    
    # with coefficients
    def test_sortTerms3(self):
        eq = Equation("\\(  9\\partial^{\\chi}B_{\\chi} +\\frac{1}{2}T \\partial_{\\gamma}\\partial_{\\kappa}A^{\\gamma} +M C^{} \\)")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\\(M C^{} +9 \\partial^{\\chi}B_{\\chi} +\\frac{1}{2} T \\partial_{\\gamma}\\partial_{\\kappa}A^{\\gamma} \\)",
        'error in sorting the terms by number of derivatives (least to greatest)')
    
    # with multiplied terms
    def test_sortTerms4(self):
        eq = Equation("\\(\\partial_{\\gamma} \\partial_{\\kappa}A^{\\gamma}  + \\partial_{\\omega}G^{} \\)\\( \\partial^{\\chi}B_{\\chi} + C^{} \\) ")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\\( \\partial_{\\omega}G^{} + \\partial_{\\gamma}\\partial_{\\kappa}A^{\\gamma} \\)\\( C^{} + \\partial^{\\chi}B_{\\chi} \\)",
        'error in sorting the terms by number of derivatives (least to greatest)')
    
    # with multiple tensors per term
    def test_sortTerms5(self):
        eq = Equation("\\(\\partial_{\\gamma} \\partial_{\\kappa}\\square A^{\\gamma}\\partial_{\\omega}G^{} + \\square \\partial^{\\chi}B_{\\chi} + \\square X_{\\xi}+ \\square V_{}C^{} \\)")
        eq.sortTerms()
        self.assertEqual(repr(eq), "\\( \\square X_{\\xi} + \\square V^{} C^{} + \\partial^{\\chi}\\square B_{\\chi} + \\partial_{\\gamma}\\partial_{\\kappa}\\square A^{\\gamma} \\partial_{\\omega}G^{} \\)",
        'error in sorting the terms by number of derivatives (least to greatest)')