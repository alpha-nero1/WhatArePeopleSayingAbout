from app_auth.views import LoginView, SignupView
from app.sitemaps import StaticSitemap, TopicSitemap
from django.contrib import admin
from django.urls import path, re_path
from app.views import HomeView, SearchView, TopicView, PostView
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static':StaticSitemap,
    'topics': TopicSitemap
}

urlpatterns = [
    re_path(r'^topics/[-\w]+/(?P<id>.+)', PostView.as_view()),
    re_path(r'^topics/(?P<id>[-\w]+)/', TopicView.as_view()),
    re_path(r'^search/', SearchView.as_view()),
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', HomeView.as_view())
]
