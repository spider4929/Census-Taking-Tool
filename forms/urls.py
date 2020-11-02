from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='forms-home'),
    path('create/', views.create, name='forms-create'),
    path('edit/<id>/', views.create, name='forms-edit'),
    path('delete/<id>/', views.delete, name='forms-delete'),
    path('about/', views.about, name='forms-about'),
    path('search/', views.search, name='forms-search'),
    path('specify/<id>/', views.specify, name='forms-specify')
]
