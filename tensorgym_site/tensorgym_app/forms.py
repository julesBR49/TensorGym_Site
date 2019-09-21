from django import forms
from Tensors import Equation

class EquationForm(forms.Form):
    equation = forms.CharField(label='Equation' initial='Input Equation' required=False)
    foil = forms.BooleanField(required=False)
    distribute_partials = forms.BooleanField(required=False)
    foil_no_distribute = forms.BooleanField(required=False)

    def compute(self):
        initial_equation = Equation(self.equation)
