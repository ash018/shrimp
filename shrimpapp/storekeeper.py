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

def GrnPrint(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

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
        #from django.db import connection
        cursor = connection.cursor()

        cursor.execute("select AB.AbsId AS AbsId, AB.TotalKg, AB.TotalLb, Ab.LocDate, CASE WHEN GPr.IsFullPaymentDone  IS NULL THEN 'N' ELSE 'Y' END as IsFullPaymentDone, Spp.SupplierName, Spp.SupplierCode from Abstraction AB FULL OUTER JOIN GrnPrint GPr ON AB.AbsId = GPr.AbsId  INNER JOIN Weightment WEg  ON AB.AbsId = WEg.AbsId INNER JOIN Supplier Spp ON Spp.SupId = WEg.SupplierId  where AB.EntryDate between '"+str(absFromDate)+"' and '"+str(absToDate)+"'")
        row = cursor.fetchall()

        #print("--====--"+str(row))

        context = {'PageTitle': 'Print GRN',
                   'supplierList': supplierList,
                   'fromDate':fromDate,
                   'toDate':toDate,
                   'weghtmentList':row
                   }
        return render(request, 'shrimpapp/GrnPrint.html', context)

def GrnbtnDates(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        fromDate = request.GET.get('FromDate')
        toDate = request.GET.get('ToDate')
        serDayTime = fromDate.split('-')
        serToDayTime = toDate.split('-')

        absFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        absToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)
        cursor = connection.cursor()
        cursor.execute("select AB.AbsId AS AbsId, AB.TotalKg, AB.TotalLb, Ab.LocDate, CASE WHEN GPr.IsFullPaymentDone  IS NULL THEN 'N' ELSE 'Y' END as IsFullPaymentDone, Spp.SupplierName, Spp.SupplierCode from Abstraction AB FULL OUTER JOIN GrnPrint GPr ON AB.AbsId = GPr.AbsId  INNER JOIN Weightment WEg  ON AB.AbsId = WEg.AbsId INNER JOIN Supplier Spp ON Spp.SupId = WEg.SupplierId  where AB.EntryDate between '"+str(absFromDate)+"' and '"+str(absToDate)+"'")
        row = cursor.fetchall()
        #print("--====--" + str(row))
        html = render_to_string('shrimpapp/GrnbtnDates.html', {'weghtmentList': row})

        context = {'weghtmentList': row}
        template = 'shrimpapp/GrnbtnDates.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })


def PriceDistributionCreate(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        ShrimpItem.objects.all().values('Id','Name')
        ProdItem.objects.all().values('Id','Name')

        userId = request.session['uid']

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")

        context = {'PageTitle': 'Print GRN',
                   'supplierList': supplierList,
                   'Date': fromDate
                   }
        return render(request, 'shrimpapp/PriceDistributionCreate.html', context)

def ShowPriceDistributionBTNDate(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")


def EditPriceDistribution(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
