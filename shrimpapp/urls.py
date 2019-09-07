from django.conf.urls import url
from .views import *
from . import views
from . import qcweightmentview
from . import productionview
from . import ajaxresponseview
from . import storekeeper


urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^Home', views.Home, name='Home'),
    url(r'^ProductionReport', views.ProductionReport, name='ProductionReport'),
    url(r'^Weightment', views.WeightmentView, name='WeightmentView'),
    url(r'^ListWeightment', views.ListWeightment, name='ListWeightment'),

    url(r'^VWAbstraction', views.VWAbstraction, name='VWAbstraction'),
    url(r'^EdAbstraction', views.EdAbstraction, name='EdAbstraction'),
    url(r'^PrAbstraction', views.PrAbstraction, name='PrAbstraction'),

    url(r'^UpdAbstraction', views.UpdAbstraction, name='UpdAbstraction'),

    url(r'^EditWeightment', views.EditWeightment, name='EditWeightment'),
    url(r'^UpdateWeightment', views.UpdateWeightment, name='UpdateWeightment'),
    url(r'^SaveWeightment', views.SaveWeightment, name='SaveWeightment'),
    url(r'^SupplyerListByFarmer', views.SupplyerListByFarmer, name='SupplyerListByFarmer'),
    url(r'^SItemBySType', views.SItemBySType, name='SItemBySType'),

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
    url(r'^PkgModalTableUpdate', productionview.PkgModalTableUpdate, name='PkgModalTableUpdate'),

    url(r'^SavPrdDetail', productionview.SavPrdDetail, name='SavPrdDetail'),
    url(r'^ListProduction', productionview.ListProduction, name='ListProduction'),
    url(r'^AllPrdListForEdit', productionview.AllPrdListForEdit, name='AllPrdListForEdit'),
    url(r'^EditProduction', productionview.EditProduction, name='EditProduction'),
    url(r'^UpdateProduction', productionview.UpdateProduction, name='UpdateProduction'),

    url(r'^RCresponse', ajaxresponseview.RCresponse, name='RCresponse'),
    url(r'^FarmerListBySupplier', ajaxresponseview.FarmerListBySupplier, name='FarmerListBySupplier'),
    url(r'^FmWeightMentForm', ajaxresponseview.FmWeightMentForm, name='FmWeightMentForm'),
    url(r'^CostDistributionDetailForm', ajaxresponseview.CostDistributionDetailForm, name='CostDistributionDetailForm'),
    url(r'^RecordGRNPrint', ajaxresponseview.RecordGRNPrint, name='RecordGRNPrint'),

    url(r'^GrnPrint', storekeeper.GrnPrint, name='GrnPrint'),
    url(r'^GrnbtnDates', storekeeper.GrnbtnDates, name='GrnbtnDates'),

    url(r'^PriceDistributionCreate', storekeeper.PriceDistributionCreate, name='PriceDistributionCreate'),
    url(r'^SavePriceDistributionCreate', storekeeper.SavePriceDistributionCreate, name='SavePriceDistributionCreate'),
    url(r'^ShowPriceDistributionBTNDate', storekeeper.ShowPriceDistributionBTNDate, name='ShowPriceDistributionBTNDate'),
    url(r'^PDSearchBTNDates', storekeeper.PDSearchBTNDates, name='PDSearchBTNDates'),
    url(r'^EditPriceDistribution', storekeeper.EditPriceDistribution, name='EditPriceDistribution'),

    url(r'^UpdPriceDistribution', storekeeper.UpdPriceDistribution, name='UpdPriceDistribution'),
    url(r'^ShowPdDtl', storekeeper.ShowPdDtl, name='ShowPdDtl'),

    url(r'^Logout', views.Logout, name='Logout'),




]