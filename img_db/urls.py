# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views  #其中的句点让Python从当前的urls.py模块所在的文件夹中导入视图
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^upload/', views.uploadImg),
    url(r'^show/', views.showImg),
    url(r'^login/$', views.login),
    url(r'^regist/$', views.regist),
    url(r'^regist_success/$', views.regist),
    url(r'^login_success/$', views.login),
    url(r'^index/$', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
