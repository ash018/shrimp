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
from collections import defaultdict
SESSION_ID = "ABC"


def QCWeightmentList(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        weghtmentList = Weightment.objects.filter(IsQcPass='N').values('Id', 'WgDate', 'FarmerId__FarmerCode',
                                                                       'SupplierId__SupplierCode', 'IsQcPass').order_by(
            '-Id')
        context = {'PageTitle': 'Weightment For QC','weghtmentList':weghtmentList,
                   'farmerList':farmerList,'supplierList' : supplierList,}
        return render(request, 'shrimpapp/QCWeightmentList.html', context)


def ShowDetailForQC(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        wegtId = request.GET.get('WeightmentId')

        weightment = Weightment.objects.filter(pk=int(wegtId), EntryBy=user).first()
        weightmentDetails = WeightmentDetail.objects.filter(WgId=weightment).values('Id', 'CngCount', 'ShrItemId__Id',
                                                                                    'ShrItemId__ShrimpTypeId__Id',
                                                                                    'MeasurUnit','MeasurQnty',
                                                                                    'Rate', 'Remarks')

        weightData = Weightment.objects.filter(pk=int(wegtId), EntryBy=user).values('Id', 'FarmerId__Id',
                                                                                    'SupplierId__Id', 'WgDate').first()
        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        context = {'PageTitle': 'QC', 'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem, 'farmerList': farmerList,
                   'supplierList': supplierList, 'weightData': weightData,
                   'weightmentDetails': weightmentDetails,
                   }
        return render(request, 'shrimpapp/ShowDetailForQC.html', context)

def QCPassOfWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:

        wegId = request.POST.get('WgId')
        weightmentDetail = request.POST.getlist('Weightment')
        srv = np.reshape(weightmentDetail, (-1, 4))

        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        qcWgEntryDate = datetime.datetime.now()

        Weightment.objects.filter(pk=int(wegId)).update(IsQcPass='Y')
        wgObje = Weightment.objects.filter(pk=int(wegId)).first()
        weghtment = Weightment.objects.filter(pk=int(wegId)).values('FarmerId__Id','SupplierId__Id', 'WgDate').first()

        qcWeight = QCWeightment(WgId=wgObje, FarmerId=Farmer.objects.filter(pk=int(weghtment['FarmerId__Id'])).first(),
                                SupplierId=Supplier.objects.filter(pk=int(weghtment['SupplierId__Id'])).first(),
                                WgDate=weghtment['WgDate'],IsQcPass='Y', IsProductionUsed='N',
                                EntryDate=qcWgEntryDate, EditDate=qcWgEntryDate, EntryBy=user)
        qcWeight.save()

        lQcWg = LogQCWeightment(QCWgId=qcWeight, WgId=wgObje,
                                FarmerId=Farmer.objects.filter(pk=int(weghtment['FarmerId__Id'])).first(),
                                SupplierId=Supplier.objects.filter(pk=int(weghtment['SupplierId__Id'])).first(),
                                WgDate=weghtment['WgDate'],IsQcPass='Y', IsProductionUsed='N',
                                EntryDate=qcWgEntryDate, EditDate=qcWgEntryDate, EntryBy=user)
        lQcWg.save()

        wdId = ''
        qcCnty = ''
        qcMQnty = ''
        qcRemark = ''
        wegDetail = ''
        for i in range(len(srv)):
            j = 0
            serviceTypeId = 0
            for j in range(len(srv[i])):
                if j == 0:
                    wdId = srv[i][j]
                    wegDetail = WeightmentDetail.objects.filter(pk=int(wdId)).values('CngCount','ShrItemId__Id',
                                                                                     'MeasurUnit', 'MeasurQnty',
                                                                                     'Rate','Remarks').first()
                if j == 1:
                    qcCnty = srv[i][j]
                if j == 2:
                    qcMQnty = srv[i][j]
                if j == 3:
                    qcRemark = srv[i][j]


            QCWeightmentDetail(WgId=wgObje, QCWgId=qcWeight, GivenCngCount=wegDetail['CngCount'],
                               QCCngCount=Decimal(qcCnty),
                               ShrItemId=ShrimpItem.objects.filter(pk=int(wegDetail['ShrItemId__Id'])).first(),
                               MeasurUnit=wegDetail['MeasurUnit'], MeasurQnty=wegDetail['MeasurQnty'],
                               QCMeasurQnty=Decimal(qcMQnty), Rate=wegDetail['Rate'],
                               Remarks=wegDetail['Remarks'], QCRemarks=str(qcRemark)).save()

            LogQCWeightmentDetail(LogQcId=lQcWg, QCWgId=qcWeight, WgId=wgObje, GivenCngCount=wegDetail['CngCount'],
                                  QCCngCount=Decimal(qcCnty),
                                  ShrItemId=ShrimpItem.objects.filter(pk=int(wegDetail['ShrItemId__Id'])).first(),
                                  MeasurUnit=wegDetail['MeasurUnit'], MeasurQnty=wegDetail['MeasurQnty'],
                                  QCMeasurQnty=Decimal(qcMQnty), Rate=wegDetail['Rate'],
                                  Remarks=wegDetail['Remarks'], QCRemarks=str(qcRemark)).save()


        return HttpResponseRedirect('/QCWeightmentList')

def QCSearch(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmer = request.POST.get('Farmer')
        supplier = request.POST.get('Supplier')
        fromDate = request.POST.get('FromDate')
        toDate = request.POST.get('ToDate')
        userId = request.session['uid']

        frmObj = Farmer.objects.filter(pk=int(farmer)).first()
        supObj = Supplier.objects.filter(pk=int(supplier)).first()
        serDayTime = fromDate.split('-')
        serToDayTime = toDate.split('-')

        wegFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        wegToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)

        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        user = UserManager.objects.filter(pk=int(userId)).first()

        weghtmentList = Weightment.objects.filter(IsQcPass='N', FarmerId=frmObj, SupplierId=supObj,
                                                  EntryDate__range=(wegFromDate, wegToDate)).values('Id', 'WgDate',
                                                                                                    'FarmerId__FarmerCode',
                                                                                                    'SupplierId__SupplierCode',
                                                                                                    'IsQcPass').order_by(
            '-Id')

        context = {'PageTitle': 'Weightment List', 'farmerList': farmerList,
                   'supplierList': supplierList, 'weghtmentList': weghtmentList,
                   'wegFromDate': wegFromDate, 'wegToDate': wegToDate
                   }

        return render(request, 'shrimpapp/QCWeightmentList.html', context)