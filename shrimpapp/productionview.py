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

        pakMat = PackagingMaterial.objects.all().values('Id','Name','PackSize','Stock')

        context = {'PageTitle': 'New Production',
                   'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem,
                   'produType': produType,
                   'qcWgId':qcWgId,
                   'pakMat':pakMat}

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
            sItem = ShrimpProdItem.objects.all().values('Id','Name')
            pItem = ProdItem.objects.filter(PrTyId=pType).values('Id','Name')

            packMate = PackagingMaterial.objects.all().values('Id','Name')

            # listIt = []
            # for i in range(0, len(pItem)):
            #     listIt.append(i) 'listIt':listIt,

            context = {'proType': proType, 'pItem':pItem, 'sItem':sItem, 'packMate':packMate}
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok",
                "productionType":proType['Name']
            })

def SavPrdDetail(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        if request.method == 'POST':
            prodctDate = request.POST.get('ProdctDate')
            qcWegId = request.POST.get('QcWegId')

            userId = request.session['uid']
            user = UserManager.objects.filter(pk=int(userId)).first()
            proDate = datetime.datetime.now()

            _datetime = datetime.datetime.now()
            entryDate = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
            #print('----entryDate----->' + str(entryDate))
            serDayTime = prodctDate.split('-')
            prdDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                            int(entryDate.split('-')[3]), int(entryDate.split('-')[4]),
                                            int(entryDate.split('-')[5]), 140)


            QCWeightment.objects.filter(pk=int(qcWegId)).update(IsProductionUsed='Y')
            qcWeg = QCWeightment.objects.filter(pk=int(qcWegId)).first()
            prod = Production(QCWgId=qcWeg, IsFinishGood='N', ProductionDate=prdDate, ReceivDate=_datetime, EntryDate=_datetime, EditDate=_datetime, EntryBy=user)
            prod.save()
            lgProd = LogProduction(ProdId=prod, QCWgId=qcWeg, IsFinishGood='N', ProductionDate=prdDate, ReceivDate=_datetime, EntryDate=_datetime, EditDate=_datetime, EntryBy=user)
            lgProd.save()

            proType = ProdType.objects.all().values('Id', 'Name')
            for pt in proType:
                if pt['Name'] in request.POST:
                    if pt['Id'] == 1:
                        proDetail = request.POST.getlist(str(pt['Name']))

                        srv = np.reshape(proDetail, (-1, 17))
                        for i in range(len(srv)):
                            if i != 0:
                                print(str(i) + "***" + "----Data Is -----" + str(srv[i][0]))
                                sPrdItem = ShrimpProdItem.objects.filter(pk=int(srv[i][0])).first()
                                subPr = np.reshape(srv[i][1:], (-1, 4))
                                for k in range(len(subPr)):
                                    pItem = ''
                                    pCount = ''
                                    pMunit = ''
                                    pQty = ''
                                    pPkMat = ''
                                    pPkQty = ''
                                    for m in range(len(subPr[k])):
                                        if m == 0:
                                            pItem = ProdItem.objects.filter(pk=int(subPr[k][m])).first()
                                        if m == 1:
                                            pCount = subPr[k][m]
                                        if m == 2:
                                            pMunit = subPr[k][m]
                                        if m == 3:
                                            pQty = subPr[k][m]
                                        # if m == 4:
                                        #     pPkMat = PackagingMaterial.objects.filter(pk=int(subPr[k][m])).first()
                                        # if m == 5:
                                        #     pPkQty =  subPr[k][m]

                                    ProductionDetail(ProdId=prod, SmpProdId=sPrdItem, PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit, ProdAmount=pQty).save()
                                    LogProductionDetail(LogProdId=lgProd, ProdId=prod, SmpProdId=sPrdItem,
                                                     PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                     ProdAmount=pQty).save()
                    else:
                        proDetail = request.POST.getlist(str(pt['Name']))

                        srv = np.reshape(proDetail, (-1, 21))
                        for i in range(len(srv)):
                            if i != 0:
                                print(str(i) + "***" + "----Data Is -----" + str(srv[i][0]))
                                sPrdItem = ShrimpProdItem.objects.filter(pk=int(srv[i][0])).first()
                                subPr = np.reshape(srv[i][1:], (-1, 4))
                                for k in range(len(subPr)):
                                    pItem = ''
                                    pCount = ''
                                    pMunit = ''
                                    pQty = ''

                                    for m in range(len(subPr[k])):
                                        if m == 0:
                                            pItem = ProdItem.objects.filter(pk=int(subPr[k][m])).first()
                                        if m == 1:
                                            pCount = subPr[k][m]
                                        if m == 2:
                                            pMunit = subPr[k][m]
                                        if m == 3:
                                            pQty = subPr[k][m]
                                        # if m == 4:
                                        #     pPkMat = PackagingMaterial.objects.filter(pk=int(subPr[k][m])).first()
                                        # if m == 5:
                                        #     pPkQty = subPr[k][m]

                                    ProductionDetail(ProdId=prod, SmpProdId=sPrdItem,
                                                     PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                     ProdAmount=pQty).save()
                                    LogProductionDetail(LogProdId=lgProd, ProdId=prod, SmpProdId=sPrdItem,
                                                        PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                        ProdAmount=pQty).save()

            return HttpResponseRedirect('/SearchWgForProduction')


