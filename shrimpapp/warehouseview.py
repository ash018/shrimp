from django.shortcuts import render
from django.db import connection, connections
from django.shortcuts import render
from django import template
from django.http import HttpResponse, StreamingHttpResponse
import re
from array import *
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
from django.db.models import F, Sum, Subquery, OuterRef
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import QuerySet
import numpy as np
import datetime
from decimal import Decimal
from collections import defaultdict

from django.db import connection

SESSION_ID = "ABC"

def NewWareHouse(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        #supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        serDayTime = fromDate.split('-')
        toDate = _datetime.strftime("%Y-%m-%d")
        serToDayTime = fromDate.split('-')

        absFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        absToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)
        prodTypeList = ProdType.objects.all().values('Id','Name')
        prodItemList = ProdItem.objects.all().values('Id','Name')
        shrProdItem = ShrimpProdItem.objects.filter(Id__gte=1).values('Id','Name')
        pkgMatList = PackagingMaterial.objects.exclude(Id=1).values('Id','Name','PackSize')
        finProdList = FinishProductCode.objects.all().values('Id','Code')

        context = {'PageTitle': 'New Stock Entry',
                   #'supplierList': supplierList,
                   'fromDate': fromDate,
                   'prodTypeList':prodTypeList,
                   'prodItemList':prodItemList,
                   'shrProdItem':shrProdItem,
                   'pkgMatList':pkgMatList,
                   'finProdList':finProdList
                   }
        return render(request, 'shrimpapp/NewWareHouse.html', context)

def StockList(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        serDayTime = fromDate.split('-')

        context = {'PageTitle': 'Stock List',
                   'fromDate': fromDate,
                   }

        return render(request, 'shrimpapp/StockList.html', context)

def SaveWareHouse(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        serDayTime = fromDate.split('-')

        stockReceiveDate = request.POST.get('StockReceiveDate')
        issueNo = request.POST.get('IssueNo')
        wareHouse = request.POST.getlist('WareHouse')

        prod = Production.objects.filter(LocDate=str(stockReceiveDate), IsFinishGood='N').first()
        cost = CostDistributionMaster.objects.filter(LocDate=str(stockReceiveDate), IsUsed='N').first()
        cstId = CostDistributionMaster.objects.filter(LocDate=str(stockReceiveDate), IsUsed='N').values('Id').first()

        warHouse = WareHouse(ProdId=prod,
                             CstDisId=cost,
                             LocDate=str(stockReceiveDate),
                             IssueNo=str(issueNo),
                             EntryDate=_datetime,
                             EditDate=_datetime,
                             EntryBy=user)

        warHouse.save()

        logWar = LogWareHouse(ProdId=prod,
                              WaHsId=warHouse,
                              CstDisId=cost,
                              IssueNo=str(issueNo),
                              LocDate=str(stockReceiveDate),
                              EntryDate=_datetime,
                              EditDate=_datetime,
                              EntryBy=user)
        logWar.save()
        #weightmentDetail = request.POST.getlist(str(weightmentName))
        srv = np.reshape(wareHouse, (-1, 8))

        for i in range(len(srv)):
            prItm = 0
            smpProd = 0
            pkgMat = 0
            finPC = 0

            inCarton = 0
            inKg = 0

            smpProdId = 0

            rawMaterialValueTK = 0
            avgRateTK = 0
            remarks = ''
            j=0
            for j in range(len(srv[i])):
                if j == 0:
                    print("=="+srv[i][j])
                if j == 1:
                    prItmId = srv[i][j]
                    prItm = ProdItem.objects.filter(pk=int(prItmId)).first()
                if j == 2:
                    smpProdId = srv[i][j]
                    smpProd = ShrimpProdItem.objects.filter(pk=int(smpProdId)).first()
                if j == 3:
                    pkgMatId = srv[i][j]
                    pkgMat = PackagingMaterial.objects.filter(pk=int(pkgMatId)).first()
                if j == 4:
                    finPCId = srv[i][j]
                    finPC = FinishProductCode.objects.filter(pk=int(finPCId)).first()
                if j == 5:
                    inCarton = srv[i][j]
                if j == 6:
                    inKg = srv[i][j]
                if j == 7:
                    remarks = srv[i][j]
            #CostDistributionDetail.objects.filter(CstDisId=cost, ShrimpProdItemId=smpProd).annotate(col_cost_rate=Sum('ColCostOfProdItemRate'))

            cursor = connection.cursor()
            cursor.execute("select Sum(ColCostOfProdItemRate)/count(CstDisDtlId) as AvgRate, count(CstDisDtlId) as Total from CostDistributionDetail where CstDisId = "+str(cstId['Id'])+" and ColCostOfProdItemRate > 0 and ShrimpProdItemId = "+str(smpProdId)+"  group by ShrimpProdItemId")
            row = cursor.fetchone()

            WareHouseDetail(WaHsId=warHouse,
                            PrItmId=prItm,
                            SmpProdId=smpProd,
                            PkgMatId=pkgMat,
                            FinPCId=finPC,
                            InCarton=Decimal(inCarton),
                            InKg=Decimal(inKg),
                            InLb=Decimal(inKg)*Decimal(2.20462),
                            AvgRateTK=Decimal(row[0]),
                            Remarks=str(remarks)).save()

            LogWareHouseDetail(WaHsId=warHouse,
                               LogWaHsId=logWar,
                              PrItmId=prItm,
                              SmpProdId=smpProd,
                              PkgMatId=pkgMat,
                              FinPCId=finPC,
                              InCarton=Decimal(inCarton),
                              InKg=Decimal(inKg),
                              InLb=Decimal(inKg)*Decimal(2.20462),
                              AvgRateTK=Decimal(row[0]),
                              Remarks=str(remarks)).save()
        return HttpResponseRedirect('/NewWareHouse')













