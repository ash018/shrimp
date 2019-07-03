from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^Weightment', views.WeightmentView, name='WeightmentView'),
    url(r'^ListWeightment', views.ListWeightment, name='ListWeightment'),
    url(r'^EditWeightment', views.EditWeightment, name='EditWeightment'),
    url(r'^UpdateWeightment', views.UpdateWeightment, name='UpdateWeightment'),
    url(r'^SaveWeightment', views.SaveWeightment, name='SaveWeightment'),

    url(r'^Logout', views.Logout, name='Logout'),
]