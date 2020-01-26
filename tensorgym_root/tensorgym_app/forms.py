from django import forms
from Tensors.Equation import Equation

class EquationForm(forms.Form):
    # input
    equation = forms.CharField(label='Equation', help_text='Input Equation')

    text_statements = forms.BooleanField(required=False)
    initial_eq = forms.BooleanField(required=False)
    symmetric_tensors = forms.CharField(required=False)
    # foil
    foil = forms.BooleanField(required=False)
    distribute_partials = forms.BooleanField(required=False)
    foil_no_distribute = forms.BooleanField(required=False)

    # multiply
    contract_both = forms.BooleanField(required=False)
    contract_etas = forms.BooleanField(required=False)
    contract_deltas = forms.BooleanField(required=False)

    # factor
    factor_gcf = forms.BooleanField(required=False)
    factor_term = forms.BooleanField(required=False)
    term_to_factor = forms.CharField(required=False)

    # replace
    replace_indices = forms.BooleanField(required=False)
    indices_to_replace = forms.CharField(required=False)
    replacement_indices = forms.CharField(required=False)
    replace_terms = forms.BooleanField(required=False)
    term_to_replace = forms.CharField(required=False)
    replacement_term = forms.CharField(required=False)

    # sort
    combine_like_terms_num = forms.BooleanField(required=False)
    combine_like_terms = forms.BooleanField(required=False)
    sort_each = forms.BooleanField(required=False)
    sort_terms = forms.BooleanField(required=False)

    # output
    output_equation = forms.CharField(required=False, initial="")

    def compute(self):
        try:
            base_equation = Equation(self.equation, self.symmetric_tensors)
            self.output_equation = ""
            if base_equation.getCov():
                # self.open_pop("../Kivy/images/cov_warning.png")
                self.output_equation += "MAY CONTAIN LOGIC ERRORS DUE TO THE USE OF COVARIANT DERIVATIVES: PROCEED WITH CAUTION \n \n"
            if self.initial_eq:
                if self.text_statements:
                    self.output_equation += "Starting with the equation \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.foil:
                base_equation.getTree().foil(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "multiplying out terms and distributing partial derivatives using the product rule \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.distribute_partials:
                base_equation.getTree().distributePs(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "using the calculus product rule to distribute partial derivatives \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.foil_no_distribute:
                base_equation.getTree().noPfoil(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "multiplying out terms not under a partial derivative \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
        # CONTRACT
            if self.contract_both:
                base_equation.contract(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "contracting etas and deltas "
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.contract_etas:
                base_equation.contract(base_equation.getTree().getRoot(), 'eta')
                if self.text_statements:
                    self.output_equation += "contracting etas \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.contract_deltas:
                base_equation.contract(base_equation.getTree().getRoot(), 'delta')
                if self.text_statements:
                    self.output_equation += "contracting deltas \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
        # FACTOR
            if self.factor_gcf:
                base_equation.factorGCF(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "factoring out the greatest common factor \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.factor_term:
                base_equation.factorUserInputTree(base_equation.getTree().getRoot(), self.term_to_factor)
                if self.text_statements:
                    self.output_equation += "factoring out $ " + self.term_to_factor + " $ \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
        # REPLACE
            if self.replace_indices:
                base_equation.replaceIndices(self.indices_to_replace, self.replacement_indices)
                if self.text_statements:
                    self.output_equation += "replacing indices $ " + self.indices_to_replace + " $ with indices $ " + self.replacement_indices_str + " $ \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"

            if self.replace_terms:
                base_equation.replaceTerms(self.term_to_replace, self.replacement_term)
                if self.text_statements:
                    self.output_equation += "replacing $ " + self.term_to_replace + " $ with $ " + self.replacement_term + " $ \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
        # SORT
            if self.combine_like_terms_num:
                base_equation.combineLikeTermsWithoutSymCo(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "combining like terms \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
            if self.combine_like_terms:
                base_equation.combineLikeTerms(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.output_equation += "combine like terms differing by any (numerical or symbolic) coefficient \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"

            if self.sort_each:
                base_equation.sortEach()
                if self.text_statements:
                    self.output_equation += "organizing the tensors in each term from least to greatest number of partials \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"

            if self.sort_terms:
                base_equation.sortTerms()
                if self.text_statements:
                    self.output_equation += "organizing each term from least to greatest number of partials \n"
                self.output_equation += repr(base_equation)
                self.output_equation += "\n" + "\n"
        except Exception as exceptObj:
            self.output_equation = str(exceptObj) + "\n\nPlease email jbrucero@uwo.ca for if you think this is a bug"
            # self.exception_str = str(exceptObj)
            #tb = sys.exc_info()[-1]
            #stk = traceback.extract_tb(tb, 1)
            #fname = stk[0][2]
            #self.exception_str += " method that produced error: " + fname
            # self.open_except_pop("../Kivy/images/error_popup.png")