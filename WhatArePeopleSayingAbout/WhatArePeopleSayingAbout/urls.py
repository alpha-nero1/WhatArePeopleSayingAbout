from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

handler404 = 'errors.views.handler404'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('app_auth.urls')),
    path('api/', include('api.urls')),
    path('errors/', include('errors.urls')),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('', include('app.urls'))
]
