from django.shortcuts import render
from django.db import connection, connections
from django.shortcuts import render
from django import template
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
from django.db.models import F, Sum, Subquery, OuterRef
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse

import numpy as np
import datetime
from decimal import Decimal
from collections import defaultdict
SESSION_ID = "ABC"


def SearchWgForProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        wegtId = request.GET.get('WeightmentId')


        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        context = {'PageTitle': 'Production Process', 'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem, 'farmerList': farmerList,
                   }
        return render(request, 'shrimpapp/SearchWgForProduction.html', context)

#@csrf_exempt
def AllPassWgForProduction(request):
    from django.shortcuts import render
    from django.template import RequestContext
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        fromDate = request.GET.get('FromDate')
        toDate = request.GET.get('ToDate')
        serDayTime = fromDate.split('-')
        serToDayTime = toDate.split('-')

        wegFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        wegToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)

        weghtmentList = QCWeightmentDetail.objects.filter(QCWgId__in=(QCWeightment.objects.filter(IsProductionUsed='N', IsQcPass='Y', EntryDate__range=(wegFromDate,wegToDate)))).values('QCWgId','QCWgId__IsProductionUsed','QCWgId__EntryDate' ).annotate(total_count=Sum('QCCngCount'), total_kgs=Sum('QCMeasurQnty'))

        html = render_to_string('shrimpapp/AllPassWgForProduction.html', {'weghtmentList': weghtmentList})
        context = {'weghtmentList': weghtmentList}
        template = 'shrimpapp/AllPassWgForProduction.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })

def StartProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        qcWgId = request.GET.get('QcWgId')
        produType = ProdType.objects.all().values('Id', 'Name');

        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        context = {'PageTitle': 'New Production',
                   'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem,
                   'produType': produType,
                   'qcWgId':qcWgId}

        return render(request, 'shrimpapp/StartProduction.html', context)

def PrdItemForm(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        prodType = request.GET.get('ProdType')

        if request.is_ajax():
            template = 'shrimpapp/ProdItem.html'
            pType = ProdType.objects.filter(pk=int(prodType)).first()
            proType = ProdType.objects.filter(pk=int(prodType)).values('Id','Name').first()
            sItem = ShrimpItem.objects.all().values('Id','Name')
            pItem = ProdItem.objects.filter(PrTyId=pType).values('Id','Name')

            listIt = []
            for i in range(0, len(pItem)):
                listIt.append(i)

            context = {'proType': proType, 'pItem':pItem, 'sItem':sItem, 'listIt':listIt}
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok",
                "productionType":proType['Name']
            })

