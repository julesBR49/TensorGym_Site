import unittest
from Tensors.Equation import Equation

class SimpleContractionTest(unittest.TestCase):  
    
    # contract etas and deltas
    
    def test_contract_etas(self):
        eq = Equation("\\delta^{\\gamma}_{\\beta} \\eta^{\\nu \\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\beta}_{\\gamma}")
        eq.contract(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} h^{\\mu \\nu} \\partial_{\\nu} h_{\\gamma}^{\\gamma}", '')


    # contract only deltas

    def test_contract_deltas(self):
        eq = Equation("\\delta^{\\nu }_{\\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\gamma}_{\\gamma}")
        eq.contract(eq.getTree().getRoot(), 'delta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} h_{\\alpha}^{\\mu} \\partial_{\\alpha} h_{\\gamma}^{\\gamma}", '')

    # contract only etas

    def test_contract_both(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\gamma}_{\\gamma} ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} h^{\\mu \\nu} \\partial_{\\nu} h_{\\gamma}^{\\gamma}", '')