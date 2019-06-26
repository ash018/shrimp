from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^Logout', views.Logout, name='Logout'),
]