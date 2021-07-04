from django.contrib import admin
from django.urls import path, re_path
from django.urls import include


handler404 = 'errors.views.handler404'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('app_auth.urls')),
    path('api/', include('api.urls')),
    path('errors/', include('errors.urls')),
    path('', include('app.urls'))
]
