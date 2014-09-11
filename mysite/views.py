# -*- coding: utf-8 -*-  
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulStoneSoup
import datetime
import requests
import json
import sys
import hashlib
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')
fresh_token = "236873|0.pPOCyjCQV0986bmQJ50Veq6oSSkbA6zR.535115822.1370993528697"
app_id = 236873
key = "c9aaa33d06164264977890ab3f678a9a"
def index(request):
	if request.method == 'POST':
		name = request.POST.get('sound','')
		app_id = 236873
		acc = requests.post("https://graph.renren.com/oauth/token?grant_type=refresh_token&refresh_token=236873|0.pPOCyjCQV0986bmQJ50Veq6oSSkbA6zR.535115822.1370993528697&client_id=236873&client_secret=c9aaa33d06164264977890ab3f678a9a")
		acc_tok  =acc.json()
		access =acc_tok['access_token']	
		if len(name)>5 and len(name)<201:
			r = requests.post('https://api.renren.com/restserver.do', 
		            {
		                    'v': '1.0', 
		                    'access_token':access, 
		                    'format': 'json', 
		                    'method': 'status.set', 
		                    'page_id': 601756739, 
		                    'status': "#树洞#".decode("UTF-8")+name
		            })
			retu = r.json()
			retu = 'success'
			retu2 = 'alert alert-success'
			name = ''
			
		else:
			retu = 'input must between 6 and 200!'
			retu2 = 'alert alert-error'
	else:
		retu = 'waiting'
		retu2 = 'alert alert-info'
	return render_to_response('index.html',{"message":retu,"sta":retu2})
def weixin(request):
	if request.method == 'POST':
		xmlContent = request.body
		soup = BeautifulStoneSoup(xmlContent)
		soupXml = soup.xml
		tousername = soupXml.tousername.contents[0]
		fromusername = soupXml.fromusername.contents[0]
		returnContent = ''
		msgtype = soupXml.msgtype.contents[0]
		if msgtype == "event":
			event = soupXml.event.contents[0]
			# 关注推送消息
			if event == "subscribe":
				returnContent = u"你好，欢迎订阅Ang，输入“#内容”可以发布至人人树洞。"
				return render_to_response('weixin.xml',{"toUser":fromusername,"fromUser":tousername,"content":returnContent})
		#自动回复
		if msgtype == "text":
			getContent = soupXml.content.contents[0]
			if getContent.startswith("#"):
				
				weixinHole = getContent.lstrip("#")
				if len(weixinHole)>5 and len(weixinHole)<201:
					returnContent = u"发布至人人树洞"
					#获取人人access_token
					acc = requests.post("https://graph.renren.com/oauth/token?grant_type=refresh_token&refresh_token=236873|0.pPOCyjCQV0986bmQJ50Veq6oSSkbA6zR.535115822.1370993528697&client_id=236873&client_secret=c9aaa33d06164264977890ab3f678a9a")
					acc_tok  =acc.json()
					access =acc_tok['access_token']
					r = requests.post('https://api.renren.com/restserver.do', 
				            {
				                    'v': '1.0', 
				                    'access_token':access, 
				                    'format': 'json', 
				                    'method': 'status.set', 
				                    'page_id': 601756739, 
				                    'status': u"#微信#"+weixinHole+"http://126.am/TWz9q2"
				            })				
				else:
					returnContent = u"输入内容过长或过短"
			return render_to_response('weixin.xml',{"toUser":fromusername,"fromUser":tousername,"content":returnContent})
		return render_to_response('weixin.xml',{"toUser":fromusername,"fromUser":tousername,"content":returnContent})
	else:
		return HttpResponse("hello")