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
        #user = UserManager.objects.filter(pk=int(userId)).first()
        #weghtmentList = Weightment.objects.filter(IsQcPass='N').values('Id', 'WgDate', 'FarmerId__FarmerCode', 'SupplierId__SupplierCode', 'IsQcPass').order_by('-Id')

        allAbsValue = Abstraction.objects.all().values('Id', 'LocDate', 'TotalKg', 'TotalLb', 'RcvTypeId__Name','IsQcPass').order_by('-Id')

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        toDate = _datetime.strftime("%Y-%m-%d")

        context = {'PageTitle':'QC List',
                   'farmerList':farmerList,
                   'supplierList':supplierList,
                   'fromDate':fromDate,
                   'toDate':toDate,
                   'allAbsValue':allAbsValue}
        return render(request, 'shrimpapp/QCWeightmentList.html', context)


def ShowDetailForQC(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        #userId = request.session['uid']
        #user = UserManager.objects.filter(pk=int(userId)).first()
        absId = request.GET.get('AbsId')

        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        gradTypeList = GradingType.objects.all().values('Id', 'Name')

        receiveTypeList = ReceiveType.objects.all().values('Id', 'Name')

        absObj = Abstraction.objects.filter(pk=int(absId)).first()
        absObValues = Abstraction.objects.filter(pk=int(absId)).values('Id', 'RcvTypeId__Id', 'LocDate','TotalKg').first()

        wegNwegDetail = {}
        weByAbs = Weightment.objects.filter(AbsId=absObj).values('Id',
                                                                 'FarmerId__Id',
                                                                 'FarmerId__FarmerName',
                                                                 'FarmerId__FarmerMobile',
                                                                 'FarmerId__Address',
                                                                 'GrdTypeId__Id',
                                                                 'GrdTypeId__Name',
                                                                 'Total',
                                                                 'TotalSmpQnty',
                                                                 'MeasurUnit',
                                                                 'AbsId__Id')
        weDtlByAbs = WeightmentDetail.objects.filter(AbsId=absObj).values('AbsId__Id',
                                                                          'Id',
                                                                          'WgId__Id',
                                                                          'WgId__FarmerId__Id',
                                                                          'ShrItemId__Id',
                                                                          'ShrItemId__Name',
                                                                          'CngCount',
                                                                          'SmpQnty',
                                                                          'MeasurQnty',
                                                                          'Remarks')

        for weg in weByAbs:
            tmp = {}

            for wd in weDtlByAbs:
                temp = []
                if weg['Id'] == wd['WgId__Id']:
                    temp = wd
                    tmp[wd['Id']] = temp

            wegNwegDetail[weg['Id']] = tmp

        #print("======"+str(wegNwegDetail))
        context = {'PageTitle': 'Weightment QC',
                   'weightMent': weByAbs,
                   'farmerList': farmerList,
                   'supplierList': supplierList,
                   'gradTypeList': gradTypeList,
                   'receiveTypeList': receiveTypeList,
                   'sItemList': shrimpItem,
                   'shrimpType': shrimpType,
                   'absObValues': absObValues,
                   'wegNwegDetail': wegNwegDetail}
        return render(request, 'shrimpapp/ShowDetailForQC.html', context)

def QCPassOfWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:

        absId = request.POST.get('AbsId')
        totalKg = request.POST.get('TotalKg')
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()


        dt = str(datetime.datetime.now())
        _datetime = datetime.datetime.now()
        entryDate = _datetime.strftime("%Y-%m-%d-%H-%M-%S")

        qcWgEntryDate = datetime.datetime.now()

        Abstraction.objects.filter(pk=int(absId)).update(IsQcPass='Y', EditDate=qcWgEntryDate)
        absObje = Abstraction.objects.filter(pk=int(absId)).first()
        absValue = Abstraction.objects.filter(pk=int(absId)).values('RcvTypeId__Id','LocDate').first()
        rcType = ReceiveType.objects.filter(pk=int(absValue['RcvTypeId__Id'])).first()

        qcAbstraction = QCAbstraction(AbsId=absObje,
                                      RcvTypeId=rcType,
                                      QCDate=qcWgEntryDate,
                                      QCTotalKg=Decimal(totalKg),
                                      QCTotalLb=0.0,
                                      IsProductionUsed='N',
                                      IsQcPass='Y',
                                      LocDate=absValue['LocDate'],
                                      EntryDate=qcWgEntryDate,
                                      EditDate=qcWgEntryDate,
                                      EntryBy=user)
        qcAbstraction.save()
        logQcAbs = LogQCAbstraction(AbsId=absObje,
                                    QCAbsId=qcAbstraction,
                                    RcvTypeId=rcType,
                                    QCDate=qcWgEntryDate,
                                    QCTotalKg=Decimal(totalKg),
                                    QCTotalLb=0.0,
                                    IsProductionUsed='N',
                                    IsQcPass='Y',
                                    LocDate=absValue['LocDate'],
                                    EntryDate=qcWgEntryDate,
                                    EditDate=qcWgEntryDate,
                                    EntryBy=user)

        logQcAbs.save()

        allFarmers = request.POST.getlist('AllFarmers')

        for i in range(len(allFarmers)):
            farmerId = Farmer.objects.filter(pk=int(allFarmers[i])).first()
            gradingTypeName = "GradingType_" + str(allFarmers[i])
            gradingTypeData = request.POST.get(gradingTypeName)
            grdTypeId = GradingType.objects.filter(pk=int(gradingTypeData)).first()
            farmerUnitTypeName = "FarmerUnitType_" + str(allFarmers[i])
            farmerUnitTypeData = request.POST.get(farmerUnitTypeName)

            farmerTotalKgName = "FarmerTotalKg_" + str(allFarmers[i])
            farmerTotalKgData = request.POST.get(farmerTotalKgName)

            farmerShamplingKgName = "FarmerShamplingKg_" + str(allFarmers[i])
            farmerShamplingKgDate = request.POST.get(farmerShamplingKgName)
            if str(farmerShamplingKgDate) == '':
                farmerShamplingKgDate = 0.0

            weightmentName = "Weightment_" + str(allFarmers[i])
            weightmentDetail = request.POST.getlist(str(weightmentName))
            srv = np.reshape(weightmentDetail, (-1, 4))

            wegValue = Weightment.objects.filter(AbsId=absObje, FarmerId=farmerId).values('SupplierId__Id').first()
            supplier = Supplier.objects.filter(pk=int(wegValue['SupplierId__Id'])).first()
            qcWeg = QCWeightment(AbsId=absObje,
                                 QCAbsId=qcAbstraction,
                                 FarmerId=farmerId,
                                 SupplierId=supplier,
                                 GrdTypeId=grdTypeId,
                                 QCDate=qcWgEntryDate,
                                 Total=Decimal(farmerTotalKgData),
                                 TotalSmpQnty=Decimal(farmerShamplingKgDate),
                                 MeasurUnit=str(farmerUnitTypeData),
                                 EntryDate=qcWgEntryDate, EditDate=qcWgEntryDate,
                                 EntryBy=user)
            qcWeg.save()
            logQcWeg = LogQCWeightment(AbsId=absObje,
                                 QCAbsId=qcAbstraction,
                                 LogQcAbsId=logQcAbs,
                                 QCWgId=qcWeg.Id,
                                 FarmerId=farmerId,
                                 SupplierId=supplier,
                                 GrdTypeId=grdTypeId,
                                 QCDate=qcWgEntryDate,
                                 Total=Decimal(farmerTotalKgData),
                                 TotalSmpQnty=Decimal(farmerShamplingKgDate),
                                 MeasurUnit=str(farmerUnitTypeData),
                                 EntryDate=qcWgEntryDate,
                                 EditDate=qcWgEntryDate,
                                 EntryBy=user)
            logQcWeg.save()



            for m in range(len(srv)):
                j = 0
                sMQnty = 0.0
                changeCount = 0.0
                rmk = ''
                for j in range(len(srv[m])):
                    if j == 0:
                        sType = srv[m][j]
                        shrimpItem = ShrimpItem.objects.filter(pk=int(sType)).first()
                    if j == 1:
                        changeCount = srv[m][j]
                    if j == 2:
                        sMQnty = srv[m][j]
                    if j == 3:
                        rmk = srv[m][j]

                if int(gradingTypeData) == 1:
                    realMQnty = Decimal(Decimal(farmerTotalKgData) * Decimal(sMQnty) / Decimal(farmerShamplingKgDate))
                    qCWegD = QCWeightmentDetail(AbsId=absObje,
                                                QCAbsId=qcAbstraction,
                                                QCWgId=qcWeg,
                                                ShrItemId=shrimpItem,
                                                MeasurUnit=str(farmerUnitTypeData),
                                                QCCngCount=changeCount,
                                                QCSmpQnty=Decimal(sMQnty),
                                                QCMeasurQnty=Decimal(realMQnty),
                                                QCRemarks=str(rmk))
                    qCWegD.save()
                    LogQCWeightmentDetail(AbsId=absObje,
                                         QCAbsId=qcAbstraction,
                                         QCWgId=qcWeg.Id,
                                         QcWgDtlId=qCWegD.Id,
                                         LogQcAbsId=logQcAbs,
                                         LogQcWegId=logQcWeg,
                                         ShrItemId=shrimpItem,
                                         MeasurUnit=str(farmerUnitTypeData),
                                         QCCngCount=changeCount,
                                         QCSmpQnty=Decimal(sMQnty),
                                         QCMeasurQnty=Decimal(realMQnty),
                                         QCRemarks=str(rmk)).save()

                if int(gradingTypeData) == 2:
                    qCWegD = QCWeightmentDetail(AbsId=absObje,
                                                QCAbsId=qcAbstraction,
                                                QCWgId=qcWeg,
                                                ShrItemId=shrimpItem,
                                                MeasurUnit=str(farmerUnitTypeData),
                                                QCCngCount=changeCount,
                                                QCSmpQnty=Decimal(sMQnty),
                                                QCMeasurQnty=Decimal(sMQnty),
                                                QCRemarks=str(rmk))
                    qCWegD.save()
                    LogQCWeightmentDetail(AbsId=absObje,
                                          QCAbsId=qcAbstraction,
                                          QCWgId=qcWeg.Id,
                                          QcWgDtlId=qCWegD.Id,
                                          LogQcAbsId=logQcAbs,
                                          LogQcWegId=logQcWeg,
                                          ShrItemId=shrimpItem,
                                          MeasurUnit=str(farmerUnitTypeData),
                                          QCCngCount=changeCount,
                                          QCSmpQnty=Decimal(sMQnty),
                                          QCMeasurQnty=Decimal(sMQnty),
                                          QCRemarks=str(rmk)).save()

        return HttpResponseRedirect('/QCWeightmentList')

def QCSearch(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmer = request.POST.get('Farmer')
        supplier = request.POST.get('Supplier')
        fromDate = request.POST.get('FromDate')
        toDate = request.POST.get('ToDate')
        #print("==="+str(farmer))
        frmObj = ''
        supObj = ''

        if fromDate is None or  toDate is None or supplier is None or farmer is None:
            return HttpResponseRedirect('/QCWeightmentList')
        else:
            if str(supplier) == '0':
                supObj = Supplier.objects.all()
            else:
                supObj = Supplier.objects.filter(pk=int(supplier))

            if str(farmer) == '0':
                frmObj = Farmer.objects.all()
            else:
                frmObj = Farmer.objects.filter(pk=int(farmer))

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

            wegList = Weightment.objects.filter(IsQcPass='N',
                                                      EntryDate__range=(wegFromDate, wegToDate),
                                                      SupplierId__in=supObj,
                                                      FarmerId__in=frmObj).values('AbsId__Id')

            allAbsValue = Abstraction.objects.filter(Id__in=wegList).values('Id', 'LocDate', 'TotalKg', 'TotalLb', 'RcvTypeId__Name', 'IsQcPass')

            context = {'PageTitle': 'QC Weightment List',
                       'farmerList': farmerList,
                       'supplierList': supplierList,
                       'allAbsValue': allAbsValue,
                       'fromDate':fromDate,
                       'toDate':toDate,
                       'farmer': int(farmer),
                       'supplier':int(supplier)
                       }

            return render(request, 'shrimpapp/QCWeightmentList.html', context)