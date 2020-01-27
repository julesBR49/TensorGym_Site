import kivy
kivy.require('1.10.1')
from kivy.config import Config
kivy.config.Config.set('kivy','desktop', 1)
kivy.config.Config.set('graphics', 'resizable', False)
kivy.config.Config.set('graphics', 'position', 'custom')
kivy.config.Config.set('graphics', 'top', 40)
kivy.config.Config.set('graphics', 'left', 160)
Config.set('kivy', 'window_icon', '../Kivy/images/TensorGym1024-1x.png')
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from Equation import Equation
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ../Kivy import TensorGym.kv
import os, sys, traceback

"""
This is for the desktop application, implemented in kivy - not used for web

"""

class InfoPop(ModalView):
    text = StringProperty()

    def get_view(self):
        return self.view

    def set_text(self, text):
        self.text = text

    def reinitialize_text(self):
        self.text = self.text

class ExceptPop(ModalView):
    text = StringProperty()
    ref = ObjectProperty()

    def set_ref(self, ref):
        self.ref = ref

    def set_text(self, text):
        self.text = text

    def reinitialize_text(self):
        self.text = self.text

    def send_error_mssg(self, text):
        self.ref.send_error_mssg(text)

class MssgPop(ModalView):
    text = StringProperty()

    def get_view(self):
        return self.view


    def set_text(self, text):
        self.text = text

    def reinitialize_text(self):
        self.text = self.text


class ActionChoices(BoxLayout):

    latex_text_input = ObjectProperty()
    latex_text_output = ObjectProperty()
    term_to_factor_str = ObjectProperty()
    term_to_replace_str = ObjectProperty()
    replacement_term_str = ObjectProperty()
    indices_to_replace_str = ObjectProperty()
    replacement_indices_str = ObjectProperty()
    symmetric_tensors_str = ObjectProperty()
    exception_str = StringProperty()
    user_comments = ObjectProperty()


    # radio buttons
    deltas = ObjectProperty()
    etas = ObjectProperty()
    contract = ObjectProperty()
    combine = ObjectProperty()
    combine_num = ObjectProperty()
    gcf = ObjectProperty()

    #both = ObjectProperty(True)

    checkbox_is_active = ObjectProperty(False)
    # checkbox
    initial_eq = False
    text_statements = False

    foil = False
    dist_part = False
    foil_no_dist = False

    contract_both = False
    contract_deltas = False
    contract_etas = False

    factor_gcf = False
    factor_term = False

    replace_indices = False
    replace_terms = False

    combine_like_terms = False
    combine_like_terms_num = False
    sort_each = False
    sort_terms = False


    def compute(self):
        try:
            base_equation = Equation(self.latex_text_input.text, self.symmetric_tensors_str.text)
            self.latex_text_output.text = ""
            if base_equation.getCov():
                self.open_pop("../Kivy/images/cov_warning.png")
                self.latex_text_output.text += "MAY CONTAIN LOGIC ERRORS DUE TO THE USE OF COVARIANT DERIVATIVES: PROCEED WITH CAUTION \n \n"
            if self.initial_eq:
                if self.text_statements:
                    self.latex_text_output.text += "Starting with the equation \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.foil:
                base_equation.getTree().foil(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "multiplying out terms and distributing partial derivatives using the product rule \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.dist_part:
                base_equation.getTree().distributePs(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "using the calculus product rule to distribute partial derivatives \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.foil_no_dist:
                base_equation.getTree().noPfoil(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "multiplying out terms not under a partial derivative \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.contract_both:
                base_equation.contract(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "contracting etas and deltas "
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.etas:
                base_equation.contract(base_equation.getTree().getRoot(), 'eta')
                if self.text_statements:
                    self.latex_text_output.text += "contracting etas \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.deltas:
                base_equation.contract(base_equation.getTree().getRoot(), 'delta')
                if self.text_statements:
                    self.latex_text_output.text += "contracting deltas \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.factor_gcf:
                base_equation.factorGCF(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "factoring out the greatest common factor \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.factor_term:
                base_equation.factorUserInputTree(base_equation.getTree().getRoot(), self.term_to_factor_str.text)
                if self.text_statements:
                    self.latex_text_output.text += "factoring out $ " + self.term_to_factor_str.text + " $ \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"

            if self.replace_indices:
                base_equation.replaceIndices(self.indices_to_replace_str.text, self.replacement_indices_str.text)
                if self.text_statements:
                    self.latex_text_output.text += "replacing indices $ " + self.indices_to_replace_str.text + " $ with indices $ " + self.replacement_indices_str.text + " $ \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"

            if self.replace_terms:
                base_equation.replaceTerms(self.term_to_replace_str.text, self.replacement_term_str.text)
                if self.text_statements:
                    self.latex_text_output.text += "replacing $ " + self.term_to_replace_str.text + " $ with $ " + self.replacement_term_str.text + " $ \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"

            if self.combine_like_terms_num:
                base_equation.combineLikeTermsWithoutSymCo(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "combining like terms \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
            if self.combine_like_terms:
                base_equation.combineLikeTerms(base_equation.getTree().getRoot())
                if self.text_statements:
                    self.latex_text_output.text += "combine like terms differing by any (numerical or symbolic) coefficient \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"

            if self.sort_each:
                base_equation.sortEach()
                if self.text_statements:
                    self.latex_text_output.text += "organizing the tensors in each term from least to greatest number of partials \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"

            if self.sort_terms:
                base_equation.sortTerms()
                if self.text_statements:
                    self.latex_text_output.text += "organizing each term from least to greatest number of partials \n"
                self.latex_text_output.text += repr(base_equation)
                self.latex_text_output.text += "\n" + "\n"
        except Exception as exceptObj:
            self.exception_str = str(exceptObj)
            #tb = sys.exc_info()[-1]
            #stk = traceback.extract_tb(tb, 1)
            #fname = stk[0][2]
            #self.exception_str += " method that produced error: " + fname
            self.open_except_pop("../Kivy/images/error_popup.png")

    def send_error_mssg(self, user_comments):
        print("entering send error mssg")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("tensorgym@gmail.com", "classicalfieldtheory8")
        msg = MIMEMultipart()
        fromaddr = "tensorgym@gmail.com"
        toaddr = "jbrucero@uwo.ca"
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'TensorGym Error Report'
        body = "Input code: '" + self.latex_text_input.text + "' \n \n"
        body += ("Error message: '" + self.exception_str + "' \n \n")
        body += ("User comments: '" + user_comments + "' \n \n")
        body += "Checkbox states: \n"
        body += ("include initial equation in output?: " + str(self.initial_eq) + "\n")
        body += ("include short dexcription in output?: " + str(self.text_statements) + "\n")
        body += ("symmetric tensors list: " + self.symmetric_tensors_str.text + "\n \n")
        body += ("FOIL out with product rule: " + str(self.foil) + "\n")
        body += ("distribute partials: " + str(self.dist_part) + "\n")
        body += ("FOIL no partials: " + str(self.foil_no_dist) + "\n")
        body += ("contract both: " + str(self.contract) + "\n")
        body += ("contract deltas: " + str(self.contract_deltas) + "\n")
        body += ("contract etas: " + str(self.contract_etas) + "\n")
        body += ("factor GCF: " + str(self.factor_gcf) + "\n")
        body += ("factor user specified term: " + str(self.factor_term) + "      term: '" + self.term_to_factor_str.text + "' \n")
        body += ("replace indices: " + str(self.replace_indices) + "    indices to replace: '" + self.indices_to_replace_str.text + "'    replacement indices: '" + self.replacement_indices_str.text + "' \n")
        body += ("replace terms: " + str(self.replace_terms) + "    terms to replace: '" + self.term_to_replace_str.text + "'   replacement term: '" + self.replacement_term_str.text + "' \n")
        body += ("combine like terms differing by just numerical factor: " + str(self.combine_like_terms_num) + "\n")
        body += ("combine like terms differing by numerical or symbolic coefficient: " + str(self.combine_like_terms) + "\n")
        body += ("sort tensors in each term: " + str(self.sort_each) + "\n")
        body += ("sort terms: " + str(self.sort_terms) + "\n")
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        self.open_mssg_pop()
        print("sent!!!")

    def clicked_include_eq(self, value):
        self.initial_eq = value

    def clicked_include_text(self, value):
        self.text_statements = value

    def clicked_foil(self, value):
        self.foil = value

    def clicked_dist_part(self, value):
        self.dist_part = value

    def clicked_foil_no_dist(self, value):
        self.foil_no_dist = value

    def clicked_contract(self, value):
        self.contract_both = value

    def clicked_deltas(self, value):
        self.deltas = value

    def clicked_etas(self, value):
        self.etas = value

    def clicked_factor_gcf(self, value):
        self.factor_gcf = value

    def clicked_factor_term(self, value):
        self.factor_term = value

    def clicked_replace_indices(self, value):
        self.replace_indices = value

    def clicked_replace_terms(self, value):
        self.replace_terms = value

    def clicked_combine_like_terms(self, value):
        self.combine_like_terms = value

    def clicked_combine_like_terms_num(self, value):
        self.combine_like_terms_num = value

    def clicked_sort_each(self, value):
        self.sort_each = value

    def clicked_sort_terms(self, value):
        self.sort_terms = value

    def checkbox_clicked(self, instance, value):
        pass

    def open_mssg_pop(self):
        pop = MssgPop()
        pop.set_text("message sent!")
        pop.open()

    def open_pop(self, text):
        pop = InfoPop()
        pop.set_text(text)
        pop.open()

    def open_except_pop(self, text):
        pop = ExceptPop()
        pop.set_text(text)
        pop.set_ref(self)
        pop.open()

    def compute_clicked(self, instance, value):
        pass

class TensorGymApp(App):

    def build(self):
        KIVY_DPI = 320
        KIVY_METRICS_DENSITY = 2
        self.icon = "../Kivy/images/TensorGym1024-1x.png"
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (650, 700)
        return ActionChoices()


if __name__ == "__main__":
    TensorGymApp().run()

