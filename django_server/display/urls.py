from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path('', views.home, name='display-home'),
    path('search/', views.SearchView.as_view(), name='search-results'),
    re_path('firms/$', views.firms, name='display-firms'),
    re_path('firms/(?P<name>.*)', views.firm_page, name='display-firm_page'),
]