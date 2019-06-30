from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^Weightment', views.Weightment, name='Weightment'),
    url(r'^SaveWeightment', views.Weightment, name='SaveWeightment'),
    url(r'^Logout', views.Logout, name='Logout'),
]