import unittest
from Tensors.Equation import Equation

class SimpleRepresentationTest(unittest.TestCase):

    # reading in signs between brackets
    def test_rep1(self):
        eq = Equation("\\(a\\) + \\(b\\)")
        self.assertEqual(repr(eq),"\\(a \\)+\\(b \\)", 'reading in signs between brackets, +')

    def test_rep2(self):
        eq = Equation("\\(a \\)-\\(b \\) ")
        self.assertEqual(repr(eq),"\\(a \\)-\\(b \\)", 'reading in signs between brackets, -')

    # basic reading in signs inside brackets
    def test_rep3(self):
        eq = Equation("b_{\\gamma} - g_{j} ")
        self.assertEqual(repr(eq),"\\( b_{\\gamma} - g_{j} \\)", 'basic reading in signs inside brackets')

    # inside and outside brackets
    def test_rep4(self):
        eq = Equation("A^{\\mu} + \\(A^{\\gamma} - B^{\\zeta}\\)")
        self.assertEqual(repr(eq),"A^{\\mu} +\\( A^{\\gamma} - B^{\\zeta} \\)", 'inside and outside brackets, +')

    def test_rep5(self):
        eq = Equation("A^{\\mu} - \\(A^{\\gamma} - B^{\\zeta}\\) ")
        self.assertEqual(repr(eq),"A^{\\mu} - \\( A^{\\gamma} - B^{\\zeta} \\)", 'inside and outside brackets, -')

    # with partial derivatives
    def test_rep6(self):
        eq = Equation("\\partial_{\\alpha} \\( a +\\( b_{\\gamma} - g\\)\\) ")
        self.assertEqual(repr(eq),"\\partial_{\\alpha} \\(a +\\( b_{\\gamma} -g \\)\\)", 'with partial derivatives')

    # multiplied by a tensor
    def test_rep7(self):
        eq = Equation("A^{\\mu} + C^{\\epsilon}\\(A^{\\gamma} - B^{\\zeta}\\)")
        self.assertEqual(repr(eq),"A^{\\mu} + C^{\\epsilon} \\( A^{\\gamma} - B^{\\zeta} \\)", 'multiplied by a tensor')

    # complicated bracket nesting
    def test_rep8(self):
        eq = Equation("\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a - d\\) - b\\)")
        self.assertEqual(repr(eq),"\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a -d \\)-b \\)", 
        'complicated bracket nesting')

    # complicated bracket nesting and tensor indices
    def test_rep9(self):
        eq = Equation("\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\(a^{\\gamma} - d^{\\gamma}\\) - b\\) ")
        self.assertEqual(repr(eq),"\\(\\(a \\)- \\(b - \\(c \\)\\)\\)+\\(\\( a^{\\gamma} - d^{\\gamma} \\)-b \\)", 
        'complicated bracket nesting and tensor indices')

    # complicated bracket nesting and tensor indices, multiplication, and partials
    def test_rep10(self):
        eq = Equation("\\partial_{\\zeta}\\( G^{\\gamma} \\) \\partial^{\\zeta} \\square \\(\\( A^{} \\)- \\( B_{\\kappa}^{\\kappa} - \\( C^{} \\)\\)\\)+\\(\\( A^{\\gamma} - D^{\\gamma} \\)- B_{\\alpha}^{\\alpha \\gamma} \\)")
        self.assertEqual(repr(eq),"\\partial_{\\zeta}\\( G^{\\gamma} \\) \\partial^{\\zeta} \\square \\(\\( A^{} \\)- \\( B_{\\kappa}^{\\kappa} - \\( C^{} \\)\\)\\)+\\(\\( A^{\\gamma} - D^{\\gamma} \\)- B_{\\alpha}^{\\alpha \\gamma} \\)",
         'complicated bracket nesting and tensor indices, multiplication, and partials')

    # with equals sign
    def test_rep11(self):
        eq = Equation("G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\)")
        self.assertEqual(repr(eq),"G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)", 
        'with equals sign')

    # with begin equation command
    def test_rep12(self):
        eq = Equation("\\begin{equation}\n G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{equation}")
        self.assertEqual(repr(eq),"\\begin{equation} \n G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{equation}", 
        'with begin equation command')

    # with begin multine command (but short so it changes to equation)
    def test_rep13(self):
        eq = Equation("\\begin{multline} \n G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) \n\\end{multline}")
        self.assertEqual(repr(eq),"\\begin{equation} \n G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{equation}", 
        'with begin multine command (but short so it changes to equation)')

    # with begin multine command and long enough to stay multline
    def test_rep14(self):
        eq = Equation("\\begin{multline}G^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} \
            - B_{\\epsilon}\\)  + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\)  \
                + A^{\\mu} +\\\\ C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} \
                    + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\mu} \
                        +\\\\ C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) + A^{\\mu} \
                            + C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) \\end{multline}")
        self.assertEqual(repr(eq),"\\begin{multline} \nG^{\\mu} = A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu}  \\\\ \n + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu}  \\\\ \n + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu}  \\\\ \n + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)+ A^{\\mu} + C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)\n\\end{multline}", '')

    # with etas and deltas and fractions
    def test_rep15(self):
        eq = Equation("7X\\eta_{\\mu \\nu} \\delta_{\\nu}^{\\gamma}\\square A^{\\mu} + \\frac{1}{3}\\delta_{\\mu}^{\\gamma}C^{\\mu \\epsilon}\\(A_{\\epsilon} - B_{\\epsilon}\\) ")
        self.assertEqual(repr(eq),"7 X \\delta_{\\nu}^{\\gamma} \\eta_{\\mu \\nu} \\square A^{\\mu} +\\frac{1}{3} \\delta_{\\mu}^{\\gamma} C^{\\mu \\epsilon} \\( A_{\\epsilon} - B_{\\epsilon} \\)", 
        'with etas and deltas and fractions')

    # multiple coefficients 
    def test_rep16(self):
        eq = Equation("\\(XY Z \\partial_{\\nu}h^{\\mu \\nu} + 6bX \\partial^{\\mu} h^{\\nu }_{\\nu}\\) ")
        self.assertEqual(repr(eq),"\\(XY Z \\partial_{\\nu}h^{\\mu \\nu} +6 bX \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", 
        'multiple coefficients')

    # multiple coefficients in unusual order
    def test_rep17(self):
        eq = Equation("\\(XY \\partial_{\\nu}h^{\\mu \\nu}Z + b6X \\partial^{\\mu} h^{\\nu }_{\\nu}\\)")
        self.assertEqual(repr(eq),"\\(XY Z \\partial_{\\nu}h^{\\mu \\nu} +6 bX \\partial^{\\mu}h_{\\nu}^{\\nu} \\)", 
        'multiple coefficients in unusual order')


    # def test_rep(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')


    # def test_rep(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')

    # def test_rep(self):
    #     eq = Equation("")
    #     self.assertEqual(repr(eq),"", '')

