from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='forms-home'),
    path('about/', views.about, name='forms-about'),
]
