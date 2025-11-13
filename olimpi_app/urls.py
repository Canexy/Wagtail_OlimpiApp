from django.contrib import admin
from django.urls import include, path, re_path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('register_par/', include('register_par.urls')),
    path('admin/', admin.site.urls),
    path('wadmin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    # Optional URL for including your own vanilla Django urls/views
    re_path(r'', include('register_par.urls')),
    # For anything not caught by a more specific rule above, hand over to Wagtail's serving mechanism
    # re_path(r'', include(wagtail_urls)),
]