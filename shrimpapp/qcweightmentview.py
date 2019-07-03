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
        weghtmentList = Weightment.objects.all().values('Id', 'WgDate', 'FarmerId__FarmerCode',
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
        weightmentDetails = WeightmentDetail.objects.filter(WgId=weightment).values('CngCount', 'ShrItemId__Id',
                                                                                    'ShrItemId__ShrimpTypeId__Id',
                                                                                    'MeasurUnit',
                                                                                    'MeasurQnty', 'Rate', 'Remarks')

        weightData = Weightment.objects.filter(pk=int(wegtId), EntryBy=user).values('Id', 'FarmerId__Id',
                                                                                    'SupplierId__Id', 'WgDate').first()
        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        context = {'PageTitle': 'Weightment Edit', 'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem, 'farmerList': farmerList,
                   'supplierList': supplierList, 'weightData': weightData,
                   'weightmentDetails': weightmentDetails,
                   }
        return render(request, 'shrimpapp/ShowDetailForQC.html', context)

def QCPassOfWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        weghtmentList = Weightment.objects.all().values('Id', 'WgDate', 'FarmerId__FarmerCode',
                                                                       'SupplierId__SupplierCode', 'IsQcPass').order_by(
            '-Id')
        context = {'PageTitle': 'Weightment For QC','weghtmentList':weghtmentList,
                   'farmerList':farmerList,'supplierList' : supplierList,}
        return HttpResponseRedirect('/QCWeightmentList')



def QCSearch(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        context = {'PageTitle': 'Home'}
        return render(request, 'shrimpapp/Home.html', context)