#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json,urllib,urllib2
import sys
from django.utils import encoding

reload(sys)
sys.setdefaultencoding("utf-8")

COMPANY_KUAIDIWANG = "kuaidiwang"

class ExpressQuery:
	__Kuaidiwang_url = 'http://highapi.kuaidi.com/openapi-querycountordernumber.html'
	__Kuaidiwang_id = '0ab4cf7b89ba0ed32efa09501c164e1b'
	#__Kuaidiwang_id = '03b7fa1414c823c2ff961b096261c132'
	__company = COMPANY_KUAIDIWANG

	__query_company_url = ''
	__express_number = ''
	__register_update = ''
	def __init__(self,number):
		self.__express_number = number
		if self.__company == COMPANY_KUAIDIWANG:
			self.__query_company_url = self.__Kuaidiwang_url+'?id='+self.__Kuaidiwang_id+'&nu='+number+'&order=desc'
		print self.__query_company_url
		
	def getCompanyInfo(self,number):
		response = urllib.urlopen(self.__query_company_url)
		#data  = response.read()
		result = json.loads(response.read().decode())
		_company_code = ''
		_company_name = ''
		_city = ''
		_icon = ''
		_status = 0
		_datalist =[]
		_success=False

		if 'success' in result:
			_success = result['success']

		if ('ico' in result) and (result['ico']!=''):
			_icon = result['ico']

		if ('exname' in result) and (result['exname']!=''):
			_company_code = result['exname']

		if ('status' in result) and (result['status']!=''):
			_status = result['status']

		if ('city' in result) and (result['city']!=''):
			'''
			if isinstance(result['city'], unicode):
				_city=encoding.smart_str(result['city'], encoding='utf-8', strings_only=False, errors='strict')
				print _city
			else:
				_city=result['city']
			'''
			_city = result['city']

		if ('company' in result) and (result['company']!=''):
			_company_name=result['company']

		if ('data' in result) and (result['data']!=''):
			_datalist = result['data']

		data = {'company_name':_company_name, 'company_code':_company_code, 'status':_status, 'icon':_icon, 'data':json.dumps(_datalist), 'success': _success, 'number': number}
		#data = {'company_name': result['company'], 'company_code': result['exname'], 'status': result['status'],'icon': result['ico'], 'data': result['data']}
		#return json.dumps(data)
		return data
