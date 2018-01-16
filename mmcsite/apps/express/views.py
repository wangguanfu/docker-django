# -*- coding: utf-8 -*-

import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.shortcuts import render
from datetime import *
from django.utils import encoding

from utils.views import HttpResponseMessage, HttpResponseMessageWithData,dateFormat
from utils.libs.express_query import ExpressQuery
from express.models import IotExpress,PAY_QUERY_OK, PAY_QUERY_FAIL,vendorcompany

def t_to_dict(t):
    if t.company is not None:
        t_dict = {
            "id":t.pk,
            "number": t.number,
            "company_code": t.company.company_code,
            "company_name": t.company.company_name,
            "status": t.status,
            "icon": t.company.icon,
            "data": json.loads(t.data),
            "time": t.time.strftime(dateFormat),
            "description": t.description,
            "pay_status": t.pay_status
        }
    else:
        t_dict = {
            "id": t.pk,
            "number": t.number,
            "company_code": '',
            "company_name": '',
            "status": t.status,
            "icon": '',
            "data": json.loads(t.data),
            "time": t.time.strftime(dateFormat),
            "description": t.description,
            "pay_status": t.pay_status,
        }
    return t_dict

#mmc APIs for express
@csrf_exempt
def register(request):
    json_data = None
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'number' in json_data:
        _number = json_data['number']
    else:
        return HttpResponseMessage(1, 'no express number in request')

    try:
        express = IotExpress.objects.get(number=_number)
        print "already in db"
        if express.pay_status==0:
            # update the express info, only update company
            print "query fail last time, update"
            p = ExpressQuery(_number)
            response = p.getCompanyInfo(_number)
            _company_code = ''
            _company_name = ''
            _icon = ''
            vendor_com = None

            if 'success' in response and response['success']:
                print "query OK, update"
                _pay_status = PAY_QUERY_OK
                vendor_com = express.company
                _pay_status = PAY_QUERY_OK
                express.pay_status = _pay_status
                if 'company_code' in response:
                    _company_code = response['company_code']

                if 'icon' in response:
                    _icon = response['icon']

                if 'company_name' in response:
                    _company_name = response['company_name']

                vendor_company = express.company
                if vendor_company is None:
                    print "create a new company"
                    vendor_company = vendorcompany.objects.create(
                        company_code=_company_code,
                        company_name=_company_name,
                        icon=_icon,
                    )
                else:
                    vendor_company.company_name = _company_name
                    vendor_company.company_code = _company_code
                    vendor_company.icon = _icon
                    vendor_company.save()

                express.company = vendor_company
                express.pay_status = _pay_status
                express.save()

        return HttpResponseMessageWithData(0, 'success', "express", t_to_dict(express))

    except:
        #return HttpResponseMessageWithData(0, 'not find', "express", _number)
        p = ExpressQuery(_number)
        response = p.getCompanyInfo(_number)
        #return HttpResponseMessageWithData(0, 'success', "express", response)

        _company_code = ''
        _company_name = ''
        _data = ''
        _icon = ''
        _pay_status = PAY_QUERY_FAIL
        vendor_com = None

        if 'company_code' in response and response['company_code']!='':
            _company_code = response['company_code']
            if 'icon' in response:
                _icon = response['icon']

            if 'company_name' in response:
                _company_name = response['company_name']
            #create comanpy item
            try:
                print "the company could be found"
                vendor_com = vendorcompany.objects.get(company_code=_company_code, vendor='W')
            except:
                print "create a new company"
                vendor_com = vendorcompany.objects.create(
                    company_code=_company_code,
                    company_name=_company_name,
                    icon=_icon,
                )
            print vendor_com.company_name

        if 'status' in response:
            _status = response['status']

        if 'data' in response:
            _data = response['data']

        if 'success' in response:
            _success = response['success']
            if _success:
                _pay_status = PAY_QUERY_OK

        print "create a new express"
        if vendor_com is not None:
            print "company exist"
            express = IotExpress.objects.create(
                number=_number,
                company=vendor_com,
                status=_status,
                pay_status=_pay_status,
                data=_data,
            )
        else:
            print "company not exist"
            express = IotExpress.objects.create(
                number=_number,
                status=_status,
                data=_data,
            )
        return HttpResponseMessageWithData(0, 'success', "express", t_to_dict(express))


@csrf_exempt
def change(request):
    #str = encoding.smart_unicode(u'好')
    str = u'顺丰快递'
    if isinstance(str, unicode):
        data = {"unicode": str, "utf8": str.encode("utf-8")}
        return HttpResponseMessageWithData("test1", str, "test", data)
    else:
        return HttpResponseMessage(1, str)

@csrf_exempt
def get_latest(request):
    _number = request.GET.get('number')
    print "register/get"
    print _number
    try:
        express = IotExpress.objects.get(number=_number)
        p = ExpressQuery(_number)
        response = p.getCompanyInfo(_number)
        _company_code = ''
        _company_name = ''
        _status = ''
        _data = ''
        _icon = ''
        _des = ''
        changed=False

        if 'status' in response:
            _status = response['status']
            if express.status != _status:
                express.status = _status
                changed=True

        if 'data' in response:
            _data = response['data']
            if _data!=express.data:
                express.data=_data
                changed=True

        if express.pay_status==PAY_QUERY_FAIL:
            if 'success' in response and response['success']:
                _pay_status = PAY_QUERY_OK
                express.pay_status = _pay_status
                changed=True
                if 'company_code' in response:
                    _company_code = response['company_code']

                if 'icon' in response:
                    _icon = response['icon']

                if 'company_name' in response:
                    _company_name = response['company_name']

                vendor_company = express.company
                if vendor_company is None:
                    vendor_company = vendorcompany.objects.create(
                        company_code=_company_code,
                        company_name=_company_name,
                        icon=_icon,
                    )
                else:
                    vendor_company.company_name = _company_name
                    vendor_company.company_code = _company_code
                    vendor_company.icon = _icon
                    vendor_company.save()

                express.company = vendor_company


        if changed:
            express.save()

        print changed

        return HttpResponseMessageWithData(0, 'success', "express", t_to_dict(express))
    except:
        return HttpResponseMessage(3, 'the number is not in database')

@csrf_exempt
def get_count_bymonth(request):
    _month = int(request.GET.get('month'))
    print _month
    #start = datetime.time(datetime.utcnow().year, _month, 1, 0, 0, 0, 0)
    #start = time.struct_time(tm_year=datetime.utcnow().year, tm_mon=_month, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0)
    print datetime.utcnow().year
    start = datetime(datetime.utcnow().year, _month, 1, 0, 0, 0, 0)
    #start = datetime(2016, _month, 1, 0, 0, 0, 0)
    #start = date(2016, 11, 1)
    print start
    if (_month==12):
        end = datetime(datetime.utcnow().year+1, 1, 1, 0, 0, 0, 0)
    else:
        end = datetime(datetime.utcnow().year + 1, _month + 1, 1, 0, 0, 0, 0)
    print end
    express_list = IotExpress.objects.filter(time__gte=start, time__lte=end)
    failed=0
    succeed=0
    if len(express_list) > 0:
        for t in express_list:
            if t.pay_status == 0:
                failed += 1
            else:
                succeed += 1
    data = {"OK": succeed, "fail": failed}
    return HttpResponseMessageWithData(0, 'success', "data", data)

#def get_express_list(request):

