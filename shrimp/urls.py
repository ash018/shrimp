from django.urls import path
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('shrimpapp.urls'))
]
