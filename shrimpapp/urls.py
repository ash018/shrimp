from django.conf.urls import url
from .views import *
from . import views
from . import qcweightmentview

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^Weightment', views.WeightmentView, name='WeightmentView'),
    url(r'^ListWeightment', views.ListWeightment, name='ListWeightment'),
    url(r'^EditWeightment', views.EditWeightment, name='EditWeightment'),
    url(r'^UpdateWeightment', views.UpdateWeightment, name='UpdateWeightment'),
    url(r'^SaveWeightment', views.SaveWeightment, name='SaveWeightment'),

    url(r'^QCWeightmentList', qcweightmentview.QCWeightmentList, name='QCWeightmentList'),
    url(r'^QCSearch', qcweightmentview.QCSearch, name='QCSearch'),
    url(r'^ShowDetailForQC', qcweightmentview.ShowDetailForQC, name='ShowDetailForQC'),
    url(r'^QCPassOfWeightment', qcweightmentview.QCPassOfWeightment, name='QCPassOfWeightment'),


    url(r'^Logout', views.Logout, name='Logout'),
]