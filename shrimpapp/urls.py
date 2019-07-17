from django.conf.urls import url
from .views import *
from . import views
from . import qcweightmentview
from . import productionview

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^Weightment', views.WeightmentView, name='WeightmentView'),
    url(r'^ListWeightment', views.ListWeightment, name='ListWeightment'),
    url(r'^EditWeightment', views.EditWeightment, name='EditWeightment'),
    url(r'^UpdateWeightment', views.UpdateWeightment, name='UpdateWeightment'),
    url(r'^SaveWeightment', views.SaveWeightment, name='SaveWeightment'),

    url(r'^ListSearchWeightment', views.ListSearchWeightment, name='ListSearchWeightment'),

    url(r'^QCWeightmentList', qcweightmentview.QCWeightmentList, name='QCWeightmentList'),
    url(r'^QCSearch', qcweightmentview.QCSearch, name='QCSearch'),
    url(r'^ShowDetailForQC', qcweightmentview.ShowDetailForQC, name='ShowDetailForQC'),
    url(r'^QCPassOfWeightment', qcweightmentview.QCPassOfWeightment, name='QCPassOfWeightment'),

    url(r'^SearchWgForProduction', productionview.SearchWgForProduction, name='SearchWgForProduction'),
    url(r'^AllPassWgForProduction', productionview.AllPassWgForProduction, name='AllPassWgForProduction'),
    url(r'^StartProduction', productionview.StartProduction, name='StartProduction'),
    url(r'^PrdItemForm', productionview.PrdItemForm, name='PrdItemForm'),
    url(r'^ModalTableShow', productionview.ModalTableShow, name='ModalTableShow'),

    url(r'^SavPrdDetail', productionview.SavPrdDetail, name='SavPrdDetail'),
    url(r'^ListProduction', productionview.ListProduction, name='ListProduction'),
    url(r'^AllPrdListForEdit', productionview.AllPrdListForEdit, name='AllPrdListForEdit'),
    url(r'^EditProduction', productionview.EditProduction, name='EditProduction'),

    url(r'^Logout', views.Logout, name='Logout'),
]