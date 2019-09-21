from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import EquationForm

# Create your views here.

def home(request):
    if request.method == 'POST':

        form = EquationForm(request.POST)
        if form.is_valid():
            form.equation = form.cleaned_data['equation']
            form.foil = form.cleaned_data['foil']
            form.output_equation = ""
            form.compute()
            html = "<html><body> Equation: %s </body></html>" % form.output_equation
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