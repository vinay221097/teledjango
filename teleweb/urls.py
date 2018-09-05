"""teleweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url,path
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     path('telegram-auth/', include('django_telethon_authorization.urls')),
# ]

from django.conf.urls import url
from teleapp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^login/$', login, name="login"),
    url(r'^login1/$', login1, name="login1"),
    url(r'^otp/$', otp, name="otp"),
    url(r'^main/$', main, name="main"),
    url(r'^abc/$', abc, name="abc"),
    url(r'^getmembers/$', getmembers, name="getmembers"),
    url(r'^bcd/$', bcd, name="bcd"),
    url(r'^addmembers/$', addmembers, name="addmembers"),
    url(r'^cde/$', cde, name="cde"),
    url(r'^custommembers/$', custommembers, name="custommembers"),
    url(r'^signout/$',signout,name="signout"),    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)