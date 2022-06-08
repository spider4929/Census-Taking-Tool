from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='forms-home'),
    path('create-person/', views.create_person, name='forms-create-person'),
    path('edit-person/<int:id>/', views.edit_person, name='forms-edit-person'),
    path('delete-person/<int:id>/', views.delete_person, name='forms-delete-person'),
    path('create-household/', views.create_household, name='forms-create-household'),
    path('edit-household/<int:id>/', views.edit_household, name='forms-edit-household'),
    path('delete-household/<int:id>/', views.delete_household, name='forms-delete-household'),
    path('about/', views.about, name='forms-about'),
    path('search/', views.search, name='forms-search'),
    path('specify/<int:id>/', views.specify, name='forms-specify'),
    path('analytics/', views.analytics_view, name='forms-analytics')
    #path('analytics/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    #path('data/', views.pivot_data, name='pivot-data'),
]
