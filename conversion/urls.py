# conversion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversion_view, name='conversion'),
    path('pdf-to-word/', views.pdf_to_word, name='pdf_to_word'),
]
