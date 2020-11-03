from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='forms-home'),
    path('create-person/', views.create_person, name='forms-create-person'),
    path('create-household/', views.create_household, name='forms-create-household'),
    path('edit-person/<id>/', views.create_person, name='forms-edit-person'),
    path('edit-household/<id>/', views.create_household, name='forms-edit-household'),
    path('delete/<id>/', views.delete, name='forms-delete'),
    path('about/', views.about, name='forms-about'),
    path('search/', views.search, name='forms-search'),
    path('specify/<id>/', views.specify, name='forms-specify')
]
