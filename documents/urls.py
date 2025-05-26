# documents/urls.py
from django.urls import path, include

urlpatterns = [
    path('login/', include('login.urls')),          
    path('conversion/', include('conversion.urls')), 
]
