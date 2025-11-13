
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Equipos

# # No implementado aún.

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

#

class ListaEquiposView(ListView):
    model = Equipos
    template_name = 'register_par/lista_equipos.html'

class DetalleEquipoView(DetailView):
    model = Equipos
    template_name = 'register_par/detalle_equipo.html'

def index(request):
    return HttpResponse("Hello, world. You're at the register index.")

# No implementado aún.

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
        else:
            form = NameForm()

        return render(request, 'register_par/name.html', {'form': form})