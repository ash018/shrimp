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
from django.template.loader import render_to_string
from django.http import JsonResponse
from collections import defaultdict
SESSION_ID = "ABC"

#https://simpleisbetterthancomplex.com/tips/2016/09/27/django-tip-15-cbv-mixins.html
#
# Git catch command
#  git rm -r --cached .
# git add .
# git commit -m "fixed untracked files"


def Login(request):
    if request.method == 'GET':
        if 'uid' not in request.session:
            return render(request, 'shrimpapp/Login.html')
        else:
            UserId = request.session['uid']
            return render(request, 'shrimpapp/Login.html')
    if request.method == 'POST':
        userName = request.POST.get('UserId')
        password = request.POST.get('Password')
        userObj = UserManager.objects.filter(UserId=userName, Password=password).first()


        if userObj is not None:
            if password == str(userObj.Password):
                request.session['uid'] = str(userObj.Id)
                request.session['UserId'] = str(userObj.UserId)
                request.session['Password'] = password
                request.session['UserName'] = str(userObj.UserName)
                request.session['Designation'] = str(userObj.DepartmentId.DepartmentName)
                request.session['Department'] = str(userObj.DepartmentId.Id)

                if not request.session.session_key:
                    request.session.save()
                global SESSION_ID
                print(request.session['UserId'])

                return HttpResponseRedirect('Home')
            else:
                return render(request, 'shrimpapp/Login.html',{'message':'UserName password mismass'})
        else:
            return render(request, 'shrimpapp/Login.html',{'message':'UserName password mismass'})


    return render(request, 'shrimpapp/Login.html')

#@login_required(login_url='/')
def Home(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        context = {'PageTitle': 'Home'}
        return render(request, 'shrimpapp/Home.html',context)

def WeightmentView(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        shrimpType = ShrimpType.objects.all().values('Id','Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        context = {'PageTitle': 'Weightment', 'shrimpType':shrimpType,
                   'shrimpItem':shrimpItem, 'farmerList':farmerList,
                   'supplierList' : supplierList
                   }
        return render(request, 'shrimpapp/Weightment.html',context)

def SaveWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        if request.method == 'POST':

            farmer = request.POST.get('Farmer')
            supplier = request.POST.get('Supplier')
            wgDate = request.POST.get('WgDate')

            userId = request.session['uid']
            user = UserManager.objects.filter(pk=int(userId)).first()

            dt = str(datetime.datetime.now())
            _datetime = datetime.datetime.now()
            entryDate = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
            print('----entryDate----->' + str(entryDate))
            serDayTime = wgDate.split('-')
            wegmentDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]), int(entryDate.split('-')[3]), int(entryDate.split('-')[4]),
                                            int(entryDate.split('-')[5]), 140)

            wgEntryDate = datetime.datetime.now()
            weightmentDetail = request.POST.getlist('Weightment')
            srv = np.reshape(weightmentDetail, (-1, 7))
            farmerId = Farmer.objects.filter(pk=int(farmer)).first()
            supplierId = Supplier.objects.filter(pk=int(supplier)).first()

            weightment = Weightment(FarmerId=farmerId, SupplierId=supplierId, WgDate=wegmentDate, IsQcPass='N', EntryDate=wgEntryDate, EditDate=wgEntryDate, EntryBy=user)
            weightment.save()

            logWeightment = LogWeightment(WgId=weightment, FarmerId=farmerId, SupplierId=supplierId, WgDate=wegmentDate, IsQcPass='N', EntryDate=wgEntryDate, EditDate=wgEntryDate, EntryBy=user)
            logWeightment.save()

            sType = ''
            changeCount = ''
            sItem = ''
            mUnit = ''
            mQnty = ''
            rate = ''
            remark = ''
            for i in range(len(srv)):
                j = 0
                serviceTypeId = 0
                for j in range(len(srv[i])):
                    if j == 0:
                        sType = srv[i][j]
                        #serviceTypeId = ServiceType.objects.filter(pk=int(sty)).first()
                    if j == 1:
                        changeCount = srv[i][j]
                    if j == 2:
                        sItem = srv[i][j]
                    if j == 3:
                        mUnit = srv[i][j]
                    if j == 4:
                        mQnty = srv[i][j]
                    if j == 5:
                        rate = srv[i][j]
                    if j == 6:
                        remark = srv[i][j]
                ShrItemId = ShrimpItem.objects.filter(pk=int(sItem)).first()
                WeightmentDetail(WgId=weightment, CngCount=Decimal(changeCount),ShrItemId=ShrItemId, MeasurUnit=str(mUnit), MeasurQnty=Decimal(mQnty), Rate=Decimal(rate), Remarks=str(remark)).save()
                LogWeightmentDetail(LgWgId=logWeightment, WgId=weightment, CngCount=Decimal(changeCount),ShrItemId=ShrItemId, MeasurUnit=str(mUnit), MeasurQnty=Decimal(mQnty), Rate=Decimal(rate), Remarks=str(remark)).save()
                print("sty-" + str(sType)+ "-com-"+ str(changeCount)+"-sch-"+ str(sItem)+"-mUnit-"+ str(mUnit)+"-mQnty-"+mQnty+"-rate-" + str(rate)+"-remark-"+str(remark))
            return HttpResponseRedirect('/Weightment')


def ListWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmerList = Farmer.objects.all().values('Id', 'FarmerName', 'FarmerCode')
        supplierList = Supplier.objects.all().values('Id', 'SupplierName', 'SupplierCode')

        userId = request.session['uid']
        user = UserManager.objects.filter(pk=int(userId)).first()

        weghtmentList = Weightment.objects.filter(EntryBy=user).values('Id','WgDate','FarmerId__FarmerCode', 'SupplierId__SupplierCode', 'IsQcPass').order_by('-Id')


        context = {'PageTitle': 'Weightment List', 'farmerList':farmerList,
                   'supplierList' : supplierList, 'weghtmentList':weghtmentList
                   }
        return render(request, 'shrimpapp/WeightmentList.html',context)



def EditWeightment(request):
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
                                                                                    'ShrItemId__ShrimpTypeId__Id', 'MeasurUnit',
                                                                                    'MeasurQnty', 'Rate', 'Remarks')

        #print("===BBB==="+str(weightmentDetails))

        weightData = Weightment.objects.filter(pk=int(wegtId), EntryBy=user).values('Id', 'FarmerId__Id', 'SupplierId__Id', 'IsQcPass', 'WgDate').first()
        shrimpType = ShrimpType.objects.all().values('Id', 'Name')
        shrimpItem = ShrimpItem.objects.all().values('Id', 'Name')
        page = ''
        if weightData['IsQcPass']=='Y':
            page = 'Weightment View'
        else:
            page = 'Weightment Edit'

        context = {'PageTitle': page, 'shrimpType':shrimpType,
                   'shrimpItem':shrimpItem, 'farmerList':farmerList,
                   'supplierList' : supplierList, 'weightData':weightData,
                   'weightmentDetails':weightmentDetails,
                   }
        return render(request, 'shrimpapp/EditWeightment.html',context)


def UpdateWeightment(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        if request.method == 'POST':
            wegId = request.POST.get('WgId')
            farmer = request.POST.get('Farmer')
            supplier = request.POST.get('Supplier')
            wgDate = request.POST.get('WgDate')

            userId = request.session['uid']
            user = UserManager.objects.filter(pk=int(userId)).first()
            weightment = Weightment.objects.filter(pk=int(wegId)).first()
            weightmentDetail = request.POST.getlist('Weightment')

            dt = str(datetime.datetime.now())
            _datetime = datetime.datetime.now()
            entryDate = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
            print('----entryDate----->' + str(entryDate))
            serDayTime = wgDate.split('-')
            wegmentDate = datetime.datetime(int(serDayTime[0]), int(serDayTime[1]), int(serDayTime[2]),
                                            int(entryDate.split('-')[3]), int(entryDate.split('-')[4]),
                                            int(entryDate.split('-')[5]), 140)

            wgEntryDate = datetime.datetime.now()

            srv = np.reshape(weightmentDetail, (-1, 7))
            farmerId = Farmer.objects.filter(pk=int(farmer)).first()
            supplierId = Supplier.objects.filter(pk=int(supplier)).first()

            WeightmentDetail.objects.filter(WgId=weightment).delete()
            Weightment.objects.filter(pk=int(wegId), EntryBy=user).update(FarmerId=farmerId, SupplierId=supplierId,WgDate=wegmentDate, EditDate=wgEntryDate)


            logWeightment = LogWeightment(WgId=weightment, FarmerId=farmerId, SupplierId=supplierId, WgDate=wegmentDate,
                                          IsQcPass='N', EntryDate=wgEntryDate, EditDate=wgEntryDate, EntryBy=user)
            logWeightment.save()

            sType = ''
            changeCount = ''
            sItem = ''
            mUnit = ''
            mQnty = ''
            rate = ''
            remark = ''
            for i in range(len(srv)):
                j = 0
                serviceTypeId = 0
                for j in range(len(srv[i])):
                    if j == 0:
                        sType = srv[i][j]
                        # serviceTypeId = ServiceType.objects.filter(pk=int(sty)).first()
                    if j == 1:
                        changeCount = srv[i][j]
                    if j == 2:
                        sItem = srv[i][j]
                    if j == 3:
                        mUnit = srv[i][j]
                    if j == 4:
                        mQnty = srv[i][j]
                    if j == 5:
                        rate = srv[i][j]
                    if j == 6:
                        remark = srv[i][j]
                ShrItemId = ShrimpItem.objects.filter(pk=int(sItem)).first()
                WeightmentDetail(WgId=weightment, CngCount=Decimal(changeCount), ShrItemId=ShrItemId,
                                 MeasurUnit=str(mUnit), MeasurQnty=Decimal(mQnty), Rate=Decimal(rate),
                                 Remarks=str(remark)).save()
                LogWeightmentDetail(LgWgId=logWeightment, WgId=weightment, CngCount=Decimal(changeCount),
                                    ShrItemId=ShrItemId, MeasurUnit=str(mUnit), MeasurQnty=Decimal(mQnty),
                                    Rate=Decimal(rate), Remarks=str(remark)).save()
                # print("sty-" + str(sType) + "-com-" + str(changeCount) + "-sch-" + str(sItem) + "-mUnit-" + str(
                #     mUnit) + "-mQnty-" + mQnty + "-rate-" + str(rate) + "-remark-" + str(remark))

        return HttpResponseRedirect('/ListWeightment')


def ListSearchWeightment(request):
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

        weghtmentList = Weightment.objects.filter(EntryBy=user, FarmerId=frmObj, SupplierId=supObj, EntryDate__range=(wegFromDate, wegToDate)).values('Id', 'WgDate', 'FarmerId__FarmerCode',
                                                                       'SupplierId__SupplierCode', 'IsQcPass').order_by(
            '-Id')

        context = {'PageTitle': 'Weightment List', 'farmerList': farmerList,
                   'supplierList': supplierList, 'weghtmentList': weghtmentList,
                   'wegFromDate':wegFromDate, 'wegToDate':wegToDate }
        return render(request, 'shrimpapp/WeightmentList.html', context)

#@csrf_exempt
def SupplyerListByFarmer(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        farmer = request.GET.get('Farmer')

        frObj = Farmer.objects.filter(pk=int(farmer)).first()
        supplierList = Supplier.objects.filter(FarmerId=frObj).values('Id', 'SupplierName', 'SupplierCode')

        context = {'supplierList': supplierList}
        template = 'shrimpapp/Suppliers.html'

        if request.is_ajax():
            html = render_to_string(template, context)
            return JsonResponse({
                "html": render_to_string(template, context),
                "status": "ok"
            })


def Logout(self):
    if 'UserId' not in self.session:
        return HttpResponseRedirect('/')
    else:
        self.session.flush()
        self.session.clear()
        del self.session
        return HttpResponseRedirect('/')