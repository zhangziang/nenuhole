# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, include, url
from mysite.views import index,weixin
import mysite.settings
import os
static_root = os.path.join(os.path.dirname(os.path.realpath(__file__)),'/static')
urlpatterns = patterns('', ('^$|^index/$',index),
	('^weixin$',weixin))