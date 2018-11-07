"""MyJumpserver URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from web01 import views

urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^get_code/$', views.get_code),
    url(r'^index/$', views.index),
    url(r'^add_host/$', views.add_host),
    url(r'^add_idc/$', views.add_idc),
    url(r'^add_host_group/$', views.add_host_group),
    url(r'^add_user/', views.add_user),
    url(r'^host_group_list/', views.host_group_list),
    url(r'^idc_list/', views.idc_list),
    url(r'^user_list/', views.user_list),
    url(r'^del_host/', views.del_host),
    url(r'^index/details/(?P<id>\d+)/',views.details),
]

# http://127.0.0.1:8000/login/
# http://127.0.0.1:8000/zhangsan/
# 超级管理员账户，admin     admin123456