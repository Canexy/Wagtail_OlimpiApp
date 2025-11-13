from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('register_par/', include('register_par.urls')),
    path('admin/', admin.site.urls)
]