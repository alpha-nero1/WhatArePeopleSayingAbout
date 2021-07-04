from django.contrib import admin
from django.urls import path, re_path, include
from .views import Login, logout, Signup, UserViewSet
from rest_framework import routers

# Django rest framework router.
router = routers.DefaultRouter()

urlpatterns = [  
    re_path(r'^login', Login.as_view()),
    re_path(r'^signup/', Signup.as_view()),
    re_path(r'^logout/', logout),
    re_path(r'api/users', UserViewSet.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
