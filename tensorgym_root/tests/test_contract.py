import unittest
from Tensors.Equation import Equation

class SimpleContractionTest(unittest.TestCase):  
    
    # contract etas and deltas
    
    def test_contract_both(self):
        eq = Equation("\\delta^{\\gamma}_{\\beta} \\eta^{\\nu \\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\beta}_{\\gamma}", "h")
        eq.contract(eq.getTree().getRoot())
        self.assertEqual(repr(eq),"\\partial_{\\mu} h^{\\mu \\nu} \\partial_{\\nu} h_{\\gamma}^{\\gamma}", '')


    # contract only deltas

    def test_contract_deltas(self):
        eq = Equation("\\delta^{\\nu }_{\\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\gamma}_{\\gamma}", "h")
        eq.contract(eq.getTree().getRoot(), 'delta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} h_{\\alpha}^{\\mu} \\partial_{\\alpha} h_{\\gamma}^{\\gamma}", '')

    # contract only etas

    # with a symmetric tensor
    def test_contract_etas1(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} h^{\\mu}_{\\alpha}\\partial_{\\nu} h^{\\gamma}_{\\gamma} ", "h")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} h^{\\mu \\nu} \\partial_{\\nu} h_{\\gamma}^{\\gamma}", '')

    # same level
    def test_contract_etas2(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial^{\\mu} d_{\\mu \\alpha}\\partial_{\\nu} d^{\\ \\gamma}_{\\gamma} ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial^{\\mu} d_{\\mu \\ }^{\\ \\nu} \\partial_{\\nu} d_{\\gamma}^{\\ \\gamma}", '')


    # simply appends
    def test_contract_etas3(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} d^{\\mu}_{\\ \\alpha}\\partial_{\\nu} d^{\\ \\gamma}_{\\gamma} ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} d^{\\mu \\nu} \\partial_{\\nu} d_{\\gamma}^{\\ \\gamma}", '')

    # replaces space
    def test_contract_etas4(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} d^{\\ \\mu}_{\\alpha}\\partial_{\\nu} d^{\\ \\gamma}_{\\gamma} ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} d^{\\nu \\mu} \\partial_{\\nu} d_{\\gamma}^{\\ \\gamma}", '')

    # has to append space
    def test_contract_etas5(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} d^{\\mu}_{\\ \\zeta \\alpha}  ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} d_{\\ \\zeta \\ }^{\\mu \\ \\nu}", '')

    # replaces space in middle
    def test_contract_etas6(self):
        eq = Equation("\\eta^{\\nu \\alpha} \\partial_{\\mu} d^{\\mu \\  \\zeta}_{\\ \\alpha} ")
        eq.contract(eq.getTree().getRoot(), 'eta')
        self.assertEqual(repr(eq),"\\partial_{\\mu} d^{\\mu \\nu \\zeta}", '')