from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/search/', views.search_recipe, name='search_recipe'),
    path('api/history/', views.search_history, name='search_history'),
    path('api/health/', views.health_check, name='health_check'),
]
