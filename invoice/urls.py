from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_invoice, name='create-invoice'),
]