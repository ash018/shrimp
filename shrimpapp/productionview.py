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
from django.db.models import F, Sum, Subquery, OuterRef
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

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

        context = {'PageTitle': 'Weightment Edit', 'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem, 'farmerList': farmerList,
                   }
        return render(request, 'shrimpapp/SearchWgForProduction.html', context)

def AllPassWgForProduction(request):
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

        #QCWeightmentDetail.objects.values('',)
        # qry = QCWeightment.objects.filter(IsQcPass='Y',
        #                             IsProductionUsed='N',
        #                             EntryDate__range=(wegFromDate, wegToDate)).values('Id',)\
        #     .annotate(totalcc=Subquery(QCWeightmentDetail.objects.filter(QCWgId=OuterRef('pk')).values(ccCount=sum('QCCngCount'))))


        #qry = QCWeightmentDetail.objects.filter(QCWgId__in=(QCWeightment.objects.filter(EntryDate__range=(wegFromDate,wegToDate)).values('Id'))).aggregate(F('QCCngCount'))#.values('QCWgId__Id', 'sqcct') #QCWeightmentDetail.objects.filter(QCWgId__EntryDate__range=(wegFromDate,wegToDate)).annotate(st = sum('QCCngCount'))

        #qry = QCWeightmentDetail.objects.all().values('QCWgId').annotate(sum('QCCngCount'))
        weghtmentList = QCWeightmentDetail.objects.filter(QCWgId__in=(QCWeightment.objects.filter(IsProductionUsed='N', IsQcPass='Y', EntryDate__range=(wegFromDate,wegToDate)))).values('QCWgId',).annotate(total_count=Sum('QCCngCount'), total_kgs=Sum('QCMeasurQnty'))

        html = render_to_string('shrimpapp/AllPassWgForProduction.html', {'weghtmentList': weghtmentList})

        #print(html)
        #return StreamingHttpResponse(html)
        return HttpResponse(html)
        # print( qry)
        # context = {'PageTitle': 'Weightment Edit',
        #            }
        #return render(request, 'shrimpapp/ShowDetailForQC.html', context)
