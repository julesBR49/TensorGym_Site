import unittest
from Tensors.Equation import Equation

class SimpleReplaceTest(unittest.TestCase):
    
    #  replace indices

    def test_rep_ind1(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu"
        replacement_indices = "\\alpha"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha} \\partial_{\\nu} h^{\\alpha \\nu} +Y \\partial_{\\nu} h^{\\alpha \\nu} A^{\\gamma} \\)", '')


    def test_rep_ind2(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\gamma"
        replacement_indices = "\\alpha, \\beta, \\xi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha} \\partial_{\\beta} h^{\\alpha \\beta} +Y \\partial_{\\beta} h^{\\alpha \\beta} A^{\\xi} \\)", '')

    def test_rep_ind3(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\xi"
        replacement_indices = "\\alpha, \\beta, \\chi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha} \\partial_{\\beta} h^{\\alpha \\beta} +Y \\partial_{\\beta} h^{\\alpha \\beta} A^{\\gamma} \\)", '')

    def test_rep_ind4(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} +Y \\partial_{\\nu} h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\alpha"
        replacement_indices = "\\alpha, \\beta, \\xi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha} \\partial_{\\beta} h^{\\alpha \\beta} +Y \\partial_{\\beta} h^{\\alpha \\beta} A^{\\gamma} \\)", '')


    # def test_rep_ind2(self):
    #     eq = Equation("")
    #     indices_to_replace = ""
    #     replacement_indices = ""
    #     eq.replaceIndices(indices_to_replace, replacement_indices)
    #     self.assertEqual(repr(eq),"", '')


    # replace terms

    def test_rep_term1(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        term_to_replace = "A^{\\gamma}"
        replacement_term = "B^{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} +Y \\partial_{\\nu} h^{\\mu \\nu} B^{\\gamma} \\)", '')

    # tensor -> tensor, replacing a tensor on its own
    def test_rep_term2(self):
        eq = Equation("A^{\\alpha \\gamma} +  A^{\\gamma}  + C^{} ")
        term_to_replace = "A^{\\gamma}"
        replacement_term = "B^{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( A^{\\alpha \\gamma} + B^{\\gamma} + C^{} \\)", 
        'tensor -> tensor, replacing a tensor on its own')

    # # tensor -> tensor, replacing a tensor that is multiplied by other elements
    # def test_rep_term3(self):
    #     eq = Equation("4 X \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} B^{\\alpha \\gamma} +Y \\partial_{\\nu} h^{\\alpha \\nu} A^{\\gamma}")
    #     term_to_replace = "A^{\\gamma}"
    #     replacement_term = "B^{\\gamma}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"\\(4 X \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} B^{\\alpha \\gamma} +Y \\partial_{\\nu} h^{\\alpha \\nu} B^{\\gamma} \\)",
    #      'tensor -> tensor, replacing a tensor that is multiplied by other elements')


    # tensor -> tensor, replacing a tensor that has partial derivatives with just a tensor
    def test_rep_term4(self):
        eq = Equation("\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = "\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} "
        replacement_term = "B^{\\gamma}_{\\gamma} "
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( B_{\\gamma}^{\\gamma} +\\frac{3}{4} Y \\)", 
        'tensor -> tensor, replacing a tensor that has partial derivatives with just a tensor')


    # tensor -> tensor, replacing a tensor that has partial derivatives with a partial and tensor
    def test_rep_term5(self):
        eq = Equation("\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = "\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} "
        replacement_term = "\\partial_{\\gamma} B^{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( \\partial_{\\gamma} B^{\\gamma} +\\frac{3}{4} Y \\)", 
        'tensor -> tensor, replacing a tensor that has partial derivatives with a partial and tensor')


    # tensor -> tensor, replacing a tensor that has partial derivatives, includes a term that shouldn't be replaced
    def test_rep_term6(self):
        eq = Equation("\\(\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} \\) \\(\\partial_{\\xi} \\partial_{\\beta} h^{\\chi \\beta} \\)")
        term_to_replace = " \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} "
        replacement_term = "\\partial_{\\gamma}B^{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( \\partial_{\\gamma} B^{\\gamma} \\)\\( \\partial_{\\xi} \\partial_{\\beta} h^{\\chi \\beta} \\)", 
        "tensor -> tensor, replacing a tensor that has partial derivatives, includes a term that shouldn't be replaced")


    # # tensor -> tensor, replacing a tensor and some of its partial derivatives: can replace either derivative
    # def test_rep_term7(self):
    #     eq = Equation("\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
    #     term_to_replace = ""
    #     replacement_term = ""
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> tensor, replacing a tensor and some of its partial derivatives: can replace either derivative')


    # tensor -> tensor, replacing a tensor and some of its partial derivatives: must replace the derivative with the sum
    def test_rep_term8(self):
        eq = Equation("\\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = "\\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = "B^{\\mu}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( \\partial_{\\gamma} B^{\\mu} +\\frac{3}{4} Y \\)", 
        'tensor -> tensor, replacing a tensor and some of its partial derivatives: must replace the derivative with the sum')


    # tensor -> tensor, replacing a tensor and some of its partial derivatives: must replace the derivative without the sum
    def test_rep_term9(self):
        eq = Equation("\\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = "\\partial_{\\gamma} h^{\\mu \\nu} "
        replacement_term = "B^{\\mu \\nu}_{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( \\partial_{\\nu} B_{\\gamma}^{\\mu \\nu} +\\frac{3}{4} Y \\)", 
        'tensor -> tensor, replacing a tensor and some of its partial derivatives: must replace the derivative without the sum')


    # # tensor -> tensor, replacing a tensor and some of its partial derivatives: replacing a number of derivatives
    # def test_rep_term10(self):
    #     eq = Equation("\\partial_{\\gamma} \\partial_{\\nu} \\partial^{\\epsilon}  h^{\\mu \\nu} + \\frac{3}{4} Y")
    #     term_to_replace = " \\partial_{\\nu} \\partial^{\\epsilon} h^{\\mu \\nu}"
    #     replacement_term = "B^{\\mu \\epsilon}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> tensor, replacing a tensor and some of its partial derivatives: replacing a number of derivatives')


    # # tensor -> tensor, replacing a tensor and some of its partial derivatives: including square
    # def test_rep_term11(self):
    #     eq = Equation("\\partial_{\\gamma} \\partial_{\\nu} \\partial^{\\epsilon} \\square h^{\\mu \\nu} + \\frac{3}{4} Y")
    #     term_to_replace = "\\square h^{\\mu \\nu} "
    #     replacement_term = "B^{\\mu \\epsilon}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> tensor, replacing a tensor and some of its partial derivatives: including square')


    # tensor -> tensor, replacing a tensor that has partial derivatives and is multiplied by other elements
    def test_rep_term12(self):
        eq = Equation("A^{\\zeta} \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
        term_to_replace = "\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = "B^{\\mu}_{\\mu}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"A^{\\zeta} \\square M_{\\zeta} B_{\\mu}^{\\mu}",
         'tensor -> tensor, replacing a tensor that has partial derivatives and is multiplied by other elements')


    # # tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: can replace either derivative
    # def test_rep_term13(self):
    #     eq = Equation("A^{\\zeta} \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
    #     term_to_replace = "\\partial_{\\nu} h^{\\mu \\nu}"
    #     replacement_term = "B^{\\mu}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: can replace either derivative')


    # tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: must replace the derivative with the sum
    def test_rep_term14(self):
        eq = Equation("A^{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
        term_to_replace = "\\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = " B^{\\mu}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"A^{\\zeta} \\square M_{\\zeta} \\partial_{\\gamma} B^{\\mu}", 
        'tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: must replace the derivative with the sum')

    # tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: must replace the derivative without the sum
    def test_rep_term15(self):
        eq = Equation("A^{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
        term_to_replace = "\\partial_{\\gamma} h^{\\mu \\nu} "
        replacement_term = " B^{\\mu \\nu}_{\\gamma} "
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"A^{\\zeta} \\square M_{\\zeta} \\partial_{\\nu} B_{\\gamma}^{\\mu \\nu}", 
        'tensor -> tensor, replacing a tensor and some of its partial derivatives when it is multiplied by other elements: must replace the derivative without the sum')

    # tensor -> tensor, replacing a tensor in a multgroup with derivatives
    def test_rep_term16(self):
        eq = Equation("\\partial_{\\mu} \\partial^{\\gamma}\\(A^{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}\\)")
        term_to_replace = "h^{\\mu \\nu}"
        replacement_term = "B^{\\mu \\nu} "
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\partial_{\\mu} \\partial^{\\gamma} \\( A^{\\zeta} \\square M_{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} B^{\\mu \\nu} \\)", 
        'tensor -> tensor, replacing a tensor in a multgroup with derivatives')


    # tensor -> sum, replacing just a tensor
    def test_rep_term17(self):
        eq = Equation("A^{\\alpha \\gamma} +  A^{\\gamma}  + C^{} ")
        term_to_replace = "A^{\\gamma}"
        replacement_term = "B^{\\gamma} + 8fG^{\\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\( A^{\\alpha \\gamma} + C^{} \\)+\\( B^{\\gamma} +8 f G^{\\gamma} \\)", 
        'tensor -> sum, replacing just a tensor')

    # # tensor -> sum, replacing a tensor that is multiplied by other elements
    # def test_rep_term18(self):
    #     eq = Equation("4 X \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} B^{\\alpha \\gamma} +Y \\partial_{\\nu} h^{\\alpha \\nu} A^{\\gamma}")
    #     term_to_replace = "A^{\\gamma} $ with $ B^{\\gamma}"
    #     replacement_term = "B^{\\gamma} + 8fG^{\\gamma}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> sum, replacing a tensor that is multiplied by other elements')


    # tensor -> sum, replacing a tensor that has partial derivatives
    def test_rep_term19(self):
        eq = Equation("\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = "\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = "\\partial_{\\gamma} B^{\\gamma} + 5 + G^{\\mu}_{\\mu} "
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\(\\frac{3}{4} Y \\)+\\( \\partial_{\\gamma} B^{\\gamma} +5 + G_{\\mu}^{\\mu} \\)", 
        'tensor -> sum, replacing a tensor that has partial derivatives')


    # tensor -> sum, replacing a tensor and some of its partial derivatives
    def test_rep_term20(self):
        eq = Equation("\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} + \\frac{3}{4} Y")
        term_to_replace = " \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = "B^{\\gamma}_{\\gamma} + \\frac{5}{4}V"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\(\\frac{3}{4} Y \\)+\\( B_{\\gamma}^{\\gamma} +\\frac{5}{4} V \\)", 
        'tensor -> sum, replacing a tensor and some of its partial derivatives')


    # tensor -> sum, replacing a tensor that has partial derivatives and is multiplied by other elements
    def test_rep_term21(self):
        eq = Equation("A^{\\zeta} \\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
        term_to_replace = "\\partial_{\\mu} \\partial_{\\nu} h^{\\mu \\nu}"
        replacement_term = "B^{\\mu}_{\\mu} + 16\\square B^{}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"A^{\\zeta} \\square M_{\\zeta} \\( B_{\\mu}^{\\mu} +16 \\square B^{} \\)", 
        'tensor -> sum, replacing a tensor that has partial derivatives and is multiplied by other elements')


    # tensor -> sum, replacing a tensor and some of its partial derivatives when it is multiplied by other elements
    def test_rep_term22(self):
        eq = Equation("A^{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}")
        term_to_replace = "\\partial_{\\nu} h^{\\mu \\nu} "
        replacement_term = "B^{\\mu} + C^{\\mu}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"A^{\\zeta} \\square M_{\\zeta} \\partial_{\\gamma} \\( B^{\\mu} + C^{\\mu} \\)", 
        'tensor -> sum, replacing a tensor and some of its partial derivatives when it is multiplied by other elements')


    # # tensor -> sum, replacing a tensor in a multgroup with derivatives
    # def test_rep_term23(self):
    #     eq = Equation("\\partial_{\\mu} \\partial^{\\gamma}\\(A^{\\zeta} \\partial_{\\gamma} \\partial_{\\nu} h^{\\mu \\nu} \\square M_{\\zeta}\\)")
    #     term_to_replace = " h^{\\mu \\nu} "
    #     replacement_term = "B^{\\mu \\nu} + C^{\\mu \\nu}"
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", 
    #     'tensor -> sum, replacing a tensor in a multgroup with derivatives')


    # tensor -> sum, 
    def test_rep_term24(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')


    # tensor -> sum, 
    def test_rep_term25(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')


    # tensor -> sum, 
    def test_rep_term26(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')


    # tensor -> sum, 
    def test_rep_term27(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')


    # tensor -> sum, 
    def test_rep_term28(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')

    # tensor -> sum, 
    def test_rep_term29(self):
        eq = Equation("")
        term_to_replace = ""
        replacement_term = ""
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"", 
        'tensor -> sum, ')


    # def test_rep_term29(self):
    #     eq = Equation("")
    #     term_to_replace = ""
    #     replacement_term = ""
    #     eq.replaceTerms(term_to_replace, replacement_term)
    #     self.assertEqual(repr(eq),"", '')


