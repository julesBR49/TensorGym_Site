from django import forms
from Tensors import Equation

class EquationForm(forms.Form):
    equation = forms.CharField(label='Equation', help_text='Input Equation')
    foil = forms.BooleanField(required=False)
    distribute_partials = forms.BooleanField(required=False)
    foil_no_distribute = forms.BooleanField(required=False)

    output_equation = forms.CharField(required=False, initial="")

    def compute(self):
        # initial_equation = Equation(self.equation)
        if self.foil:
            self.output_equation = "foiling"
            print("foil")