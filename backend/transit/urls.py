from django.urls import path
from . import views

urlpatterns = [
    path('cities/', views.get_cities_list_view, name='get_cities_list'),
    path('search/', views.search_connections_view, name='search_connections')
]