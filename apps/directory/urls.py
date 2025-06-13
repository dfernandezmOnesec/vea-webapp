# apps/directory/urls.py

from django.urls import path
from . import views

app_name = 'directory'

urlpatterns = [
    path('', views.contact_list, name='list'),           # Vista principal del directorio
    path('create/', views.contact_create, name='create'), # Vista para crear un nuevo contacto
    path('edit/<int:pk>/', views.contact_edit, name='edit'), # Vista para editar un contacto
    path('delete/<int:pk>/', views.contact_delete, name='delete'), # Vista para eliminar un contacto
]
