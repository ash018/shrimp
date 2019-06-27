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

        print('--OBject--' + str(userObj))
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

def Home(request):
    if 'uid' not in request.session:
        return render(request, 'shrimpapp/Login.html')
    else:
        context = {'PageTitle': 'Home'}
        return render(request, 'shrimpapp/Home.html',context)

def Logout(self):
    if 'UserId' not in self.session:
        return HttpResponseRedirect('/')
    else:
        self.session.flush()
        self.session.clear()
        del self.session
        return HttpResponseRedirect('/')