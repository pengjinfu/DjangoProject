#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author:Dreamer
# Time:2018.9.1
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]