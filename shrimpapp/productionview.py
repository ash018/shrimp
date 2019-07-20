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

import numpy as np
import datetime
from decimal import Decimal
from collections import defaultdict
SESSION_ID = "ABC"

#@permission_required('polls.can_vote')
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

@csrf_exempt
def ModalTableShow(request):
    from django.shortcuts import render
    from django.template import RequestContext
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        prodItem = request.GET.get('ProdItem')
        pkgMat = request.GET.get('PkgMat')

        pItem = ProdItem.objects.filter(pk=int(prodItem)).values('Name').first()
        pakMat = PackagingMaterial.objects.all().exclude(pk=int(1)).values('Id','Name','PackSize','Stock')
        liPkgMat = re.split('-', str(pkgMat))
        temp = []
        if len(liPkgMat[:-1])> 0:
            for ts in list(pakMat):
                pakItem = []

                for sx in list(liPkgMat[:-1]):
                    cc = ''
                    if int(re.split('!', str(sx))[0]) == ts['Id']:
                        cc = str((re.split('!', str(sx))[1]))
                        break
                    else:
                        cc = "XXX"
                pakItem.append(str(ts['Id']))
                pakItem.append(ts['Name'])
                pakItem.append(ts['PackSize'])
                pakItem.append(ts['Stock'])
                pakItem.append(cc)

                temp.append(pakItem)
        else:
            for ts in list(pakMat):
                pakItem = []
                cc='XXX'
                pakItem.append(str(ts['Id']))
                pakItem.append(ts['Name'])
                pakItem.append(ts['PackSize'])
                pakItem.append(ts['Stock'])
                pakItem.append(cc)
                temp.append(pakItem)

        context = {'pakMat': list(temp)}
        template = 'shrimpapp/ModalTableShow.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok",
                "ProdItem":pItem['Name']
            })

def StartProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        qcWgId = request.GET.get('QcWgId')
        produType = ProdType.objects.all().values('Id', 'Name')

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

                        srv = np.reshape(proDetail, (-1, 21))
                        for i in range(len(srv)):
                            if i != 0:
                                #print(str(i) + "***" + "----Data Is -----" + str(srv[i][0]))
                                sPrdItem = ShrimpProdItem.objects.filter(pk=int(srv[i][0])).first()
                                subPr = np.reshape(srv[i][1:], (-1, 5))
                                for k in range(len(subPr)):
                                    pItem = ''
                                    pCount = ''
                                    pMunit = ''
                                    pQty = ''
                                    pPkMat = []
                                    pPkQty = ''
                                    prTyId = ''

                                    for m in range(len(subPr[k])):
                                        pPkMat = []
                                        if m == 0:
                                            pItem = ProdItem.objects.filter(pk=int(subPr[k][m])).first()
                                            prTyId = ProdType.objects.filter(pk=int(ProdItem.objects.filter(pk=int(subPr[k][m])).values('PrTyId__Id').first()['PrTyId__Id'])).first()
                                            print("-----Production type---" + str(prTyId))

                                        if m == 1:
                                            pCount = subPr[k][m]
                                        if m == 2:
                                            pMunit = subPr[k][m]
                                        if m == 3:
                                            pQty = subPr[k][m]
                                        if m == 4:
                                            pPkMat = re.split('-', str(subPr[k][m]))

                                    prodDetail = ProductionDetail(ProdId=prod, SmpProdId=sPrdItem, PrTyId=prTyId, PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit, ProdAmount=pQty)
                                    prodDetail.save()
                                    for pg in list(pPkMat):
                                        if str(pg) != '' and len(re.split('!', str(pg))) > 0:
                                            pPgId = PackagingMaterial.objects.filter(pk=int(re.split('!', str(pg))[0])).first()
                                            pPgQty = re.split('!', str(pg))[1]
                                            PackagingMaterial.objects.filter(pk=int(re.split('!', str(pg))[0])).update(Stock=F('Stock') - int(pPgQty))
                                            ProdDtlPkgMaterial(ProdId=prod, ProDtlId=prodDetail, PkgMatId=pPgId, Qnty=int(pPgQty)).save()

                                    LogProductionDetail(LogProdId=lgProd, ProdId=prod, SmpProdId=sPrdItem, PrTyId=prTyId,
                                                     PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                     ProdAmount=pQty).save()
                    else:
                        proDetail = request.POST.getlist(str(pt['Name']))

                        srv = np.reshape(proDetail, (-1, 26))
                        for i in range(len(srv)):
                            if i != 0:
                                sPrdItem = ShrimpProdItem.objects.filter(pk=int(srv[i][0])).first()
                                subPr = np.reshape(srv[i][1:], (-1, 5))
                                for k in range(len(subPr)):
                                    pItem = ''
                                    pCount = ''
                                    pMunit = ''
                                    pQty = ''
                                    prTyId = ''
                                    pPkMat = []

                                    for m in range(len(subPr[k])):
                                        pPkMat = []
                                        if m == 0:
                                            pItem = ProdItem.objects.filter(pk=int(subPr[k][m])).first()
                                            prTyId = ProdType.objects.filter(pk=int(
                                                ProdItem.objects.filter(pk=int(subPr[k][m])).values(
                                                    'PrTyId__Id').first()['PrTyId__Id'])).first()
                                        if m == 1:
                                            pCount = subPr[k][m]
                                        if m == 2:
                                            pMunit = subPr[k][m]
                                        if m == 3:
                                            pQty = subPr[k][m]
                                        if m == 4:
                                            pPkMat = re.split('-', str(subPr[k][m]))

                                    prodDetail = ProductionDetail(ProdId=prod, SmpProdId=sPrdItem, PrTyId=prTyId,
                                                                  PrItmId=pItem, ProdItemPcs=pCount,
                                                                  ProdItemUnit=pMunit, ProdAmount=pQty)
                                    prodDetail.save()
                                    for pg in list(pPkMat):
                                        if str(pg) != '' and len(re.split('!', str(pg))) > 0:
                                            pPgId = PackagingMaterial.objects.filter(
                                                pk=int(re.split('!', str(pg))[0])).first()
                                            pPgQty = re.split('!', str(pg))[1]
                                            PackagingMaterial.objects.filter(pk=int(re.split('!', str(pg))[0])).update(
                                                Stock=F('Stock') - int(pPgQty))
                                            ProdDtlPkgMaterial(ProdId=prod, ProDtlId=prodDetail, PkgMatId=pPgId,
                                                               Qnty=int(pPgQty)).save()

                                    LogProductionDetail(LogProdId=lgProd, ProdId=prod, SmpProdId=sPrdItem, PrTyId=prTyId,
                                                        PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                        ProdAmount=pQty).save()

            return HttpResponseRedirect('/SearchWgForProduction')

def ListProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        context = {'PageTitle': 'Production List'}
        return render(request, 'shrimpapp/ListProduction.html', context)

def AllPrdListForEdit(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        fromDate = request.GET.get('FromDate')
        toDate = request.GET.get('ToDate')
        serDayTime = fromDate.split('-')
        serToDayTime = toDate.split('-')

        proFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        proToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)

        productionList = Production.objects.filter(IsFinishGood='N', ProductionDate__range=(proFromDate,proToDate)).values('Id','ProductionDate','QCWgId__EntryDate','QCWgId__WgId__EntryDate').order_by('-Id')

        context = {'productionList': productionList}
        template = 'shrimpapp/AllPrdListForEdit.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })

def EditProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        prodId = request.GET.get('ProductionId')
        proObje = Production.objects.filter(pk=int(prodId)).first()

        prType =  ProdType.objects.all().values('Id','Name')
        semProdItems = ShrimpProdItem.objects.all().values('Id','Name')
        sItem = ShrimpProdItem.objects.all().values('Id','Name')
        proData = Production.objects.filter(pk=int(prodId)).values('Id', 'ProductionDate').first()
        semDisItems = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id', 'PrTyId__Id', 'PrItmId__Id','PrTyId__Name').distinct()
        proTypes = ProdType.objects.filter(pk__in=(ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id').distinct())).values('Id','Name')

        proItems = ProdItem.objects.filter(PrTyId__in=(ProdType.objects.filter(pk__in=(ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id').distinct())))).values('Id','PrTyId__Id', 'Name', 'PrTyId__Name')
        pRowItems = ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id', 'PrItmId__Id').distinct()

        #ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id','PrItmId__Id')
        pTyTiList = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id', 'PrItmId__Id', 'PrTyId__Id')
        sRPrList = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id').distinct()

        pTySrItList = ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id','SmpProdId__Id')

        #print("***=====***" + str(semDisItems))
        #print("******" + str(sRPrList))
        #srTyPrItemDisc = {}#{}dict((x['PrItmId__Id'], x) for x in ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id', 'PrItmId__Id'))
        prTySrTyPrItDisc = {}
        for sd in semDisItems:
            srTyPrItemDisc = {}
            check = 0
            for pT in sRPrList:
                valList = list()
                for pTT in pTyTiList:
                    if pT['SmpProdId__Id'] == pTT['SmpProdId__Id'] and sd['PrTyId__Id'] == pTT['PrTyId__Id']:
                        valList.append(pTT['PrItmId__Id'])
                if len(valList) > 0:
                    srTyPrItemDisc[pT['SmpProdId__Id']] = valList
                    check = 1
            if check == 1:
                prTySrTyPrItDisc[sd['PrTyId__Name']] = srTyPrItemDisc


        #proItem = ProdType.objects.filter(pk__in=(ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id').distinct())).values('Id','Name')
        proDetails = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id', 'PrTyId__Id', 'PrItmId__Id', 'ProdItemPcs', 'ProdItemUnit', 'ProdAmount')
        print("===semProdItems===" + str(prTySrTyPrItDisc))

        pkgDetails = ProdDtlPkgMaterial.objects.filter(ProdId=proObje).values('ProDtlId__PrTyId__Id','ProDtlId__PrItmId__Id','ProDtlId__Id', 'PkgMatId__Id', 'Qnty')
        context = {'PageTitle': 'Edit Production',
                   'sItem' : sItem,
                   'prType' : prType,
                   'proTypes': proTypes,
                   'proItems': proItems,
                   'semProdItems': semProdItems,
                   'proData' : proData,
                   'proDetails' : proDetails,
                   'pkgDetails' : pkgDetails,
                   'semDisItems' : semDisItems,
                   'pRowItems' : pRowItems,
                   'prTySrTyPrItDisc' : prTySrTyPrItDisc
                   }

        return render(request, 'shrimpapp/EditProduction.html', context)
