#urls set up

from django.urls import path
from .views import *


urlpatterns = [
    path('', Home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('projects/', projects, name='projects'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),

    #admin area

    #entrepreneur area

    #investor area


]


