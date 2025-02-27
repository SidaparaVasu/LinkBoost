from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # Landing page Rendering
    path('', home, name='home'), 
    path('register', register, name='register'), 
    path('login', login, name='login'),    
]