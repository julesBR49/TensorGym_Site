from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import EquationForm

# Create your views here.

def home(request):
    if request.method == 'POST':

        form = EquationForm(request.POST)
        if form.is_valid():
            # initial
            form.equation = form.cleaned_data['equation']
            form.text_statements=form.cleaned_data['text_statements']
            form.initial_eq=form.cleaned_data['initial_eq']
            form.symmetric_tensors = form.cleaned_data['symmetric_tensors']
            # multiply
            form.foil = form.cleaned_data['foil']
            form.foil_no_distribute=form.cleaned_data['foil_no_distribute']
            form.distribute_partials=form.cleaned_data['distribute_partials']

            # contract
            form.contract_both=form.cleaned_data['contract_both']
            form.contract_deltas=form.cleaned_data['contract_deltas']
            form.contract_etas=form.cleaned_data['contract_etas']

            # factor
            form.factor_gcf=form.cleaned_data['factor_gcf']
            form.factor_term=form.cleaned_data['factor_term']
            form.term_to_factor=form.cleaned_data['term_to_factor']

            # replace
            form.replace_indices=form.cleaned_data['replace_indices']
            form.replacement_indices=form.cleaned_data['replacement_indices']
            form.indices_to_replace=form.cleaned_data['indices_to_replace']

            form.replace_terms=form.cleaned_data['replace_terms']
            form.term_to_replace=form.cleaned_data['term_to_replace']
            form.replacement_term=form.cleaned_data['replacement_term']

            # sort
            form.combine_like_terms=form.cleaned_data['combine_like_terms']
            form.combine_like_terms_num=form.cleaned_data['combine_like_terms_num']
            form.sort_each=form.cleaned_data['sort_each']
            form.sort_terms=form.cleaned_data['sort_terms']

            form.output_equation = ""
            form.compute()
            output = form.output_equation.replace("\n","<br>")
            html = "<html><body> Equation: %s </body></html>" % output
            return HttpResponse(html)
            # return render(request, 'tensorgym/home.html', {'form': form})
            # return HttpResponseRedirect('')

    else:
        form = EquationForm()
    return render(request, 'tensorgym/home.html', {'form': form})

# def home(request):
#     return render(request, 'tensorgym/home.html')

def about(request):
    return render(request, 'tensorgym/about.html')