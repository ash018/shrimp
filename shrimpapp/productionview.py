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

        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        serDayTime = fromDate.split('-')
        toDate = _datetime.strftime("%Y-%m-%d")
        serToDayTime = fromDate.split('-')

        wegFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        wegToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)


        weghtmentList = Abstraction.objects.filter(IsQcPass='Y', IsProductionUsed='N',
                                                   EntryDate__range=(wegFromDate, wegToDate)).values(
            'LocDate').annotate(total_kg=Sum('TotalKg'), total_lb=Sum('TotalLb'))

        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        context = {'PageTitle': 'Production Process',
                   'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem,
                   'farmerList': farmerList,
                   'fromDate':fromDate,
                   'toDate':toDate,
                   'weghtmentList':weghtmentList
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

        #weghtmentList = QCWeightmentDetail.objects.filter(QCWgId__in=(QCWeightment.objects.filter(IsProductionUsed='N', IsQcPass='Y', EntryDate__range=(wegFromDate,wegToDate)))).values('QCWgId','QCWgId__IsProductionUsed','QCWgId__EntryDate' ).annotate(total_count=Sum('QCCngCount'), total_kgs=Sum('QCMeasurQnty'))
        # weghtmentList = QCWeightmentDetail.objects.filter(QCWgId__in=(
        # QCWeightment.objects.filter( IsQcPass='Y',
        #                             EntryDate__range=(wegFromDate, wegToDate)))).values('QCWgId',
        #                                                                                 'QCWgId__IsProductionUsed',
        #                                                                                 'QCWgId__EntryDate').annotate(
        #     total_count=Sum('QCCngCount'), total_kgs=Sum('QCMeasurQnty'))

        weghtmentList = Abstraction.objects.filter(IsQcPass='Y', IsProductionUsed='N',EntryDate__range=(wegFromDate, wegToDate)).values('LocDate').annotate(total_kg=Sum('TotalKg'), total_lb=Sum('TotalLb'))

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
def PkgModalTableUpdate(request):
    from django.shortcuts import render
    from django.template import RequestContext
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        prodDetailId =  request.GET.get('ProdDetailId')
        pkgMat = request.GET.get('PkgMat')

        pItem = ProductionDetail.objects.filter(pk=int(prodDetailId)).values('PrItmId__Name').first()
        pdObj = ProductionDetail.objects.filter(pk=int(prodDetailId)).first()

        liPkgMat = ''
        isPkgDetails = ''
        if str(pkgMat) == 'XXX':
            isPkgDetails = True
            liPkgMat = ProdDtlPkgMaterial.objects.filter(ProDtlId=pdObj).values('Id','PkgMatId__Id','Qnty').exclude(PkgMatId__Id=1)
        else:
            isPkgDetails = False
            liPkgMat = re.split('-', str(pkgMat))

        pakMat = PackagingMaterial.objects.all().exclude(pk=int(1)).values('Id', 'Name', 'PackSize', 'Stock')

        temp = []
        for ts in list(pakMat):
            pakItem = []
            cc = "XXX"
            if isPkgDetails:
                if len(liPkgMat) > 0:
                    for sx in liPkgMat:

                        if sx['PkgMatId__Id'] == ts['Id']:
                            cc = sx['Qnty']
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
                if len(liPkgMat[:-1]) > 0:
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
                    pakItem = []
                    cc = 'XXX'
                    pakItem.append(str(ts['Id']))
                    pakItem.append(ts['Name'])
                    pakItem.append(ts['PackSize'])
                    pakItem.append(ts['Stock'])
                    pakItem.append(cc)
                    temp.append(pakItem)

        #print("=======" + str(temp))
        context = {'pakMat': list(temp)}
        template = 'shrimpapp/ModalTableShow.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok",
                "ProdItem": pItem['PrItmId__Name']
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
        pakMat = PackagingMaterial.objects.all().exclude(pk=int(1)).values('Id', 'Name', 'PackSize', 'Stock')
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
        #userId = request.session['uid']
        #user = UserManager.objects.filter(pk=int(userId)).first()
        wgDate = request.GET.get('WgDate')
        produType = ProdType.objects.all().values('Id', 'Name')

        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')

        weghtmentList = Abstraction.objects.filter(IsQcPass='Y', IsProductionUsed='N',
                                                   LocDate=str(wgDate)).values('LocDate').annotate(total_kg=Sum('TotalKg'), total_lb=Sum('TotalLb'))

        pakMat = PackagingMaterial.objects.all().values('Id','Name','PackSize','Stock')

        context = {'PageTitle': 'New Production',
                   'shrimpType': shrimpType,
                   'shrimpItem': shrimpItem,
                   'produType': produType,
                   'qcWgId':wgDate,
                   'pakMat':pakMat,
                   'weghtmentList':weghtmentList}

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

            absList = Abstraction.objects.filter(LocDate=str(qcWegId), IsProductionUsed='N', IsQcPass='Y')

            #print("===--==="+ str(len(absList)))

            Abstraction.objects.filter(LocDate=str(qcWegId), IsProductionUsed='N', IsQcPass='Y').update(
                IsProductionUsed='Y', EditDate=proDate)


            QCAbstraction.objects.filter(AbsId__in=absList).update(IsProductionUsed='Y', EditDate=proDate)

            #AbstractionId=absList,
            prod = Production(IsFinishGood='N', ProductionDate=prdDate, ReceivDate=_datetime, LocDate=str(qcWegId), EntryDate=_datetime, EditDate=_datetime, EntryBy=user)
            prod.save()

            for ab in absList:
                #print("========="+str(ab))
                ProductionAbstraction(ProductionId=prod, AbstractionId=ab).save()
                #prod.AbstractionId.add(ab)

            #prod.AbstractionId.add(absList)
            #ProductionAbstractionId(ProductionId=prod, AbstractionId=absList).save()
            #prod.save_m2m()

            lgProd = LogProduction(ProdId=prod, IsFinishGood='N', ProductionDate=prdDate, ReceivDate=_datetime, LocDate=str(qcWegId), EntryDate=_datetime, EditDate=_datetime, EntryBy=user)
            lgProd.save()

            proType = ProdType.objects.all().values('Id', 'Name')
            for pt in proType:
                if pt['Name'] in request.POST:
                    if pt['Id'] == 1:
                        proDetail = request.POST.getlist(str(pt['Name']))

                        srv = np.reshape(proDetail, (-1, 21))
                        for i in range(len(srv)):
                            if i != 0:
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

                    elif pt['Id'] == 4 :
                        proDetail = request.POST.getlist(str(pt['Name']))
                        #print("=========="+str(proDetail))
                        srv = np.reshape(proDetail, (-1, 31))
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

                    else:
                        proDetail = request.POST.getlist(str(pt['Name']))
                        #print("=========="+str(proDetail))
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
        _datetime = datetime.datetime.now()
        fromDate = _datetime.strftime("%Y-%m-%d")
        serDayTime = fromDate.split('-')
        toDate = _datetime.strftime("%Y-%m-%d")
        serToDayTime = fromDate.split('-')

        wegFromDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                        int(0), int(0),
                                        int(0), 0)
        wegToDate = datetime.datetime(int(serToDayTime[0]), int(serToDayTime[1]), int(serToDayTime[2]),
                                      int(23), int(59),
                                      int(59), 0)

        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("select PD.ProdId, sum(PD.ProdAmount) as ProdAmount from ProductionDetail PD, Production P where P.ProdId = PD.ProdId and P.EntryDate between '"+str(wegFromDate)+"' and '"+str(wegToDate)+"' and PD.ProdAmount > 0 and P.IsFinishGood = 'N' group by PD.ProdId")
        #row = cursor.fetchone()




        row = cursor.fetchall()

        print("===" + str(row))


        context = {'PageTitle': 'Production List',
                   'fromDate':fromDate,
                   'toDate':toDate,
                   'productionList':row}
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

        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("select PD.ProdId, sum(PD.ProdAmount) as ProdAmount from ProductionDetail PD, Production P where P.ProdId = PD.ProdId and P.EntryDate between '"+str(proFromDate)+"' and '"+str(proToDate)+"' and PD.ProdAmount > 0 and P.IsFinishGood = 'N' group by PD.ProdId")
        # row = cursor.fetchone()
        row = cursor.fetchall()
        #print("--===--"+str(row))
        productionList = Production.objects.filter(IsFinishGood='N', ProductionDate__range=(proFromDate,proToDate)).values('Id','ProductionDate').order_by('-Id')

        context = {'productionList': row}
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

        proItems = ProdItem.objects.filter(PrTyId__in=(ProdType.objects.filter(pk__in=(ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id').distinct())))).values('Id','PrTyId__Id', 'Name', 'PrTyId__Name')

        pTyTiList = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id', 'PrItmId__Id', 'PrTyId__Id','Id')
        sRPrList = ProductionDetail.objects.filter(ProdId=proObje).values('SmpProdId__Id').distinct()

        #pTySrItList = ProductionDetail.objects.filter(ProdId=proObje).values('PrTyId__Id','SmpProdId__Id')

        pkjMatDtl = ProdDtlPkgMaterial.objects.filter(ProdId=proObje).values('PkgMatId__Id', 'Qnty', 'ProDtlId__Id')
        pkgDtlMatLi = ProdDtlPkgMaterial.objects.filter(ProdId=proObje).values('PkgMatId__Id','ProDtlId__Id','ProDtlId__ProdItemPcs', 'ProDtlId__ProdItemUnit', 'ProDtlId__ProdAmount', 'ProDtlId__PrTyId__Id', 'ProDtlId__PrItmId__Id','ProDtlId__SmpProdId__Id')

        prTySrTyPrItDisc = {}
        for sd in semDisItems:
            srTyPrItemDisc = {}
            check = 0
            for pT in sRPrList:
                #valList = list()
                valList = {}
                for pTT in pTyTiList:
                    if pT['SmpProdId__Id'] == pTT['SmpProdId__Id'] and sd['PrTyId__Id'] == pTT['PrTyId__Id']:
                        #pkjMatDtl = ProdDtlPkgMaterial.objects.filter(ProDtlId=ProductionDetail.objects.filter(ProdId=proObje, PrTyId__Id=pTT['PrTyId__Id'], PrItmId__Id=pTT['PrItmId__Id'], SmpProdId__Id=pT['SmpProdId__Id']).first()).values('PkgMatId__Id', 'Qnty')
                        sPkjMat = ''
                        for pj in pkjMatDtl:
                            if pj['ProDtlId__Id'] == pTT['Id']:
                                sPkjMat = sPkjMat + str(pj['PkgMatId__Id'])+'!'+str(pj['Qnty'])+'-'

                        #pkgDtlMatLi = ProdDtlPkgMaterial.objects.filter(ProDtlId=ProductionDetail.objects.filter(ProdId=proObje, PrTyId__Id=pTT['PrTyId__Id'], PrItmId__Id=pTT['PrItmId__Id'], SmpProdId__Id=pT['SmpProdId__Id'] ).first()).values('PkgMatId__Id', 'ProDtlId__Id', 'ProDtlId__ProdItemPcs', 'ProDtlId__ProdItemUnit','ProDtlId__ProdAmount', 'ProDtlId__PrItmId__Id').first()
                        pKgTemp = []
                        for pKg in pkgDtlMatLi:
                            if pKg['ProDtlId__PrTyId__Id']==pTT['PrTyId__Id'] and pKg['ProDtlId__PrItmId__Id']==pTT['PrItmId__Id'] and pKg['ProDtlId__SmpProdId__Id']==pT['SmpProdId__Id']:
                                pKgTemp = pKg
                                break
                        #pkgDtlMatLi['PkgMatId__Id'] = sPkjMat
                        #valList[pTT['PrItmId__Id']] = pkgDtlMatLi


                        pKgTemp['PkgMatId__Id'] = sPkjMat
                        valList[pTT['PrItmId__Id']] = pKgTemp

                        #valList[pTT['PrItmId__Id']] = ProdDtlPkgMaterial.objects.filter(ProDtlId=ProductionDetail.objects.filter(ProdId=proObje, PrTyId__Id=pTT['PrTyId__Id'], PrItmId__Id=pTT['PrItmId__Id'], SmpProdId__Id=pT['SmpProdId__Id'] ).first()).values('PkgMatId__Id', 'ProDtlId__Id', 'ProDtlId__ProdItemPcs', 'ProDtlId__ProdItemUnit','ProDtlId__ProdAmount', 'ProDtlId__PrItmId__Id').first()
                if valList:
                    srTyPrItemDisc[pT['SmpProdId__Id']] = valList
                    check = 1
            if check == 1:
                prTySrTyPrItDisc[sd['PrTyId__Name']] = srTyPrItemDisc

        context = {'PageTitle': 'Edit Production',
                   'sItem' : sItem,
                   'prType' : prType,
                   'proItems': proItems,
                   'semProdItems': semProdItems,
                   'proData' : proData,
                   'semDisItems' : semDisItems,
                   'prTySrTyPrItDisc' : prTySrTyPrItDisc
                   }

        return render(request, 'shrimpapp/EditProduction.html', context)

def UpdateProduction(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        prodId = request.POST.get('ProdId')
        prodctDate = request.POST.get('ProdctDate')

        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()
        proDate = datetime.datetime.now()

        _datetime = datetime.datetime.now()
        entryDate = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
        serDayTime = prodctDate.split('-')
        prdDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                    int(entryDate.split('-')[3]), int(entryDate.split('-')[4]),
                                    int(entryDate.split('-')[5]), 140)

        prod = Production.objects.filter(pk=int(prodId)).first()
        Production.objects.filter(pk=int(prodId)).update(ProductionDate=prdDate, EditDate=_datetime)

        pkgMatUpdate = ProdDtlPkgMaterial.objects.filter(ProdId=prod).values('PkgMatId__Id','Qnty').exclude(PkgMatId__Id=1)

        for uPkMat in pkgMatUpdate:
            PackagingMaterial.objects.filter(pk=int(uPkMat['PkgMatId__Id'])).update(Stock = F('Stock') + int(uPkMat['Qnty']))

        ProdDtlPkgMaterial.objects.filter(ProdId=prod).delete()
        ProductionDetail.objects.filter(ProdId=prod).delete()
        qwId = Production.objects.filter(pk=int(prodId)).values('QCWgId__Id').first()
        qCWgId = QCWeightment.objects.filter(pk=int(qwId['QCWgId__Id'])).first()
        lgProd = LogProduction(ProdId=prod, QCWgId=qCWgId, IsFinishGood='N', ProductionDate=prdDate,
                               ReceivDate=_datetime, EntryDate=_datetime, EditDate=_datetime, EntryBy=user)
        lgProd.save()


        #################  Update Action Execute For Production Details and PkgMaterial #########

        proType = ProdType.objects.all().values('Id', 'Name')
        for pt in proType:
            if pt['Name'] in request.POST:
                if pt['Id'] == 1:
                    proDetail = request.POST.getlist(str(pt['Name']))

                    srv = np.reshape(proDetail, (-1, 21))
                    for i in range(len(srv)):
                        if i != 0:
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
                                        prTyId = ProdType.objects.filter(pk=int(
                                            ProdItem.objects.filter(pk=int(subPr[k][m])).values('PrTyId__Id').first()[
                                                'PrTyId__Id'])).first()

                                    if m == 1:
                                        pCount = subPr[k][m]
                                    if m == 2:
                                        pMunit = subPr[k][m]
                                    if m == 3:
                                        pQty = subPr[k][m]
                                    if m == 4:
                                        pPkMat = re.split('-', str(subPr[k][m]))

                                prodDetail = ProductionDetail(ProdId=prod, SmpProdId=sPrdItem, PrTyId=prTyId,
                                                              PrItmId=pItem, ProdItemPcs=pCount, ProdItemUnit=pMunit,
                                                              ProdAmount=pQty)
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
                elif pt['Id'] == 4:
                    proDetail = request.POST.getlist(str(pt['Name']))
                    # print("=========="+str(proDetail))
                    srv = np.reshape(proDetail, (-1, 31))
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


        return HttpResponseRedirect('/ListProduction')