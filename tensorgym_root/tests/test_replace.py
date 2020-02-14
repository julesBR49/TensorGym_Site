import unittest
from Tensors.Equation import Equation

class SimpleMultiplyTest(unittest.TestCase):
    
    #  replace indices

    def test_rep_ind1(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu"
        replacement_indices = "\\alpha"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha}\\partial_{\\nu}h^{\\alpha \\nu} +Y \\partial_{\\nu}h^{\\alpha \\nu} A^{\\gamma} \\)", '')


    def test_rep_ind2(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\gamma"
        replacement_indices = "\\alpha, \\beta, \\xi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} +Y \\partial_{\\beta}h^{\\alpha \\beta} A^{\\xi} \\)", '')

    def test_rep_ind3(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\xi"
        replacement_indices = "\\alpha, \\beta, \\chi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} +Y \\partial_{\\beta}h^{\\alpha \\beta} A^{\\gamma} \\)", '')

    def test_rep_ind4(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        indices_to_replace = "\\mu, \\nu, \\alpha"
        replacement_indices = "\\alpha, \\beta, \\xi"
        eq.replaceIndices(indices_to_replace, replacement_indices)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\alpha}\\partial_{\\beta}h^{\\alpha \\beta} +Y \\partial_{\\beta}h^{\\alpha \\beta} A^{\\gamma} \\)", '')

    # replace terms

    def test_rep_term1(self):
        eq = Equation("4X \\partial_{\\mu} \\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} A^{\\gamma}")
        term_to_replace = "A^{\\gamma}"
        replacement_term = "B^{\gamma}"
        eq.replaceTerms(term_to_replace, replacement_term)
        self.assertEqual(repr(eq),"\\(4 X \\partial_{\\mu}\\partial_{\\nu}h^{\\mu \\nu} +Y \\partial_{\\nu}h^{\\mu \\nu} B^{\\gamma} \\)", '')

    # def test_rep_term2(self):
    #     eq = Equation("")
    #     indices_to_replace = ""
    #     replacement_indices = ""
    #     eq.replaceIndices(indices_to_replace, replacement_indices)
    #     self.assertEqual(repr(eq),"", '')

    # def test_rep_ind2(self):
    #     eq = Equation("")
    #     indices_to_replace = ""
    #     replacement_indices = ""
    #     eq.replaceIndices(indices_to_replace, replacement_indices)
    #     self.assertEqual(repr(eq),"", '')