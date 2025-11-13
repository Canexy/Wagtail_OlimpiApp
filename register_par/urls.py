
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('equipos/', views.ListaEquiposView.as_view(), name='lista_equipos'),
    path('equipos/<int:pk>/', views.DetalleEquipoView.as_view(), name='detalle_equipo'),

    # No implementado aún.

    path('name/', views.get_name, name='name'),
]
