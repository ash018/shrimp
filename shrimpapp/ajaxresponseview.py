from django.shortcuts import render
from django.db import connection, connections
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import re
import csv
import requests
import time
import sys
from .models import *
from .inventorymodel import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import urllib.request
from django.views.generic import FormView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
import numpy as np
import datetime
from decimal import Decimal
from django.db.models import F, Sum, Subquery, OuterRef
from django.template.loader import render_to_string
from django.http import JsonResponse
from collections import defaultdict
SESSION_ID = "ABC"


#@csrf_exempt
def RCresponse(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        rcType = request.GET.get('RcType')


        frObj = ReceiveType.objects.filter(pk=int(rcType)).first()
        supplierList = ''
        if int(rcType) == 1:
            supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')
        if int(rcType) == 2:
            supplierList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')

        context = {'supplierList': supplierList,'param':'CascadingSupplier','rcType':int(rcType)}
        template = 'shrimpapp/Suppliers.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })


#@csrf_exempt
def FarmerListBySupplier(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        supler = request.GET.get('Supplier')
        farmerList= ''
        if str(supler) == 0:
            farmerList = Supplier.objects.all().values('FarmerId__Id', 'FarmerId__FarmerName',
                                                                       'FarmerId__FarmerCode')
        else:
            farmerList = Supplier.objects.filter(pk=int(supler)).values('FarmerId__Id', 'FarmerId__FarmerName',
                                                                        'FarmerId__FarmerCode')

        #farmerList = Supplier.objects.filter(pk=int(supler)).values('FarmerId__Id','FarmerId__FarmerName','FarmerId__FarmerCode')

        context = {'farmerList': farmerList,'param':'CascadingFarmer'}
        template = 'shrimpapp/Suppliers.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })

def FmWeightMentForm(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmer = request.GET.get('Farmer')

        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')
        farmerData = Farmer.objects.filter(pk=int(farmer)).values('Id','FarmerName','FarmerCode','FarmerMobile','Address').first()
        sItemList = ShrimpItem.objects.filter(ShrimpTypeId__Id=int(1)).values('Id', 'Name')

        gradingtype = GradingType.objects.all().values('Id','Name')

        context = {'farmerData': farmerData, 'gradingtype':gradingtype,
                   'shrimpItem':shrimpItem, 'shrimpType':shrimpType,'sItemList':sItemList}
        template = 'shrimpapp/FarmerWiseWeightment.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })

def CostDistributionDetailForm(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        disDate = request.GET.get('DistributionDate')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')
        spProductItem = ShrimpProdItem.objects.all().values('Id', 'Name').order_by('Id')

        costDes = CostDistributionMaster.objects.filter(LocDate=str(disDate))
        weDtlDscc = {}
        showForm = ''
        if costDes:
            showForm = 0
        else:
            showForm = 1

        absObjList = Abstraction.objects.filter(IsQcPass='Y', IsProductionUsed='Y', LocDate=str(disDate))
        wegDtlList = WeightmentDetail.objects.filter(AbsId__in=(absObjList)).values('ShrItemId__Id').annotate(
            toalt_item_kg=Sum('MeasurQnty'), total_item_tk=Sum('Price'))
        # weDtlDscc = {}
        total = 0.0
        for wd in wegDtlList:
            pList = list(spProductItem)
            total = Decimal(total) + Decimal(wd['toalt_item_kg'])
            pList.insert(len(spProductItem) + 1, {'toalt_item_kg': wd['toalt_item_kg']})
            pList.insert(len(spProductItem) + 2, {'total_item_tk': wd['total_item_tk']})
            weDtlDscc[wd['ShrItemId__Id']] = pList

        context = {'showForm':showForm,
                   'wegDtlList':weDtlDscc,
                   'spProductItem':spProductItem,
                   'shrimpItem':shrimpItem,
                   'total':total}
        template = 'shrimpapp/CostDistributionDetailForm.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })


def RecordGRNPrint(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        absId = request.GET.get('AbsId')

        print("--XXXX--"+str(absId))

        _datetime = datetime.datetime.now()
        absOb = Abstraction.objects.filter(pk=int(absId)).first()

        collWegDtl = WeightmentDetail.objects.filter(AbsId=absOb).values('MeasurQnty','Price')
        qcWegDtl = QCWeightmentDetail.objects.filter(AbsId=absOb).values('QCMeasurQnty')

        price = 0.0
        measurQnty = 0.0
        qCMeasurQnty = 0.0

        for cq in qcWegDtl:
            print("--=collWegDtl==--" + str(cq['QCMeasurQnty']))
            qCMeasurQnty = Decimal(qCMeasurQnty)+Decimal(cq['QCMeasurQnty'])

        for cw in collWegDtl:
            print("--=collWegDtl==--" + str(cw['Price']))
            price = Decimal(price)+Decimal(cw['Price'])
            measurQnty = Decimal(measurQnty)+Decimal(cw['MeasurQnty'])

        print("--=collWegDtl==--"+str(price))
        print("--=qcWegDtl==--" + str(qCMeasurQnty))
        # totalPrice = collWegDtl[0]['Price']
        # totalAbsMeasur = collWegDtl[0]['MeasurQnty']
        # totalQcMeasur = qcWegDtl[0]['QCMeasurQnty']


        GrnPrint(AbstractionId=absOb,
                 TotalPrice=Decimal(price),
                 TotalAbsMeasur=Decimal(measurQnty),
                 TotalQcMeasur=Decimal(qCMeasurQnty),
                 IsFullPaymentDone='Y',
                 EntryDate=_datetime,
                 EditDate=_datetime,
                 EntryBy=user).save()

        if request.is_ajax():
            #html = render_to_string(template, context)
            return JsonResponse({
                "html": "Success",
                "status": "ok"
            })