from errors.views import NotFoundView, UnverifiedView
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('unverified/', UnverifiedView.as_view()),
    path('notfound/', NotFoundView.as_view())
]
