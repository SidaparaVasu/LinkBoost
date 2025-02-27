from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # Landing page Rendering
    path('', indexPage, name='indexPage'), 
    path('home', home_view, name='home_view'), 
    path('register', register, name='register'), 
    path('login', login, name='login'),    
]